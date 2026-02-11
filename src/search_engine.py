
import pandas as pd
import numpy as np
import os
import pickle
from typing import List, Dict, Optional, Tuple, Union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import time

class UnifiedSearchEngine:
    """
    Unified search engine supporting both Keyword (TF-IDF) and Semantic (Vector) search.
    Implements a hybrid approach or selectable strategy as requested.
    """
    
    def __init__(self, data_path: str = "data"):
        self.data_path = data_path
        self.loinc_df = None
        self.icd_df = None
        
        # Search components
        self.tfidf_vectorizer_loinc = None
        self.tfidf_matrix_loinc = None
        self.tfidf_vectorizer_icd = None
        self.tfidf_matrix_icd = None
        
        self.embedding_model = None
        self.loinc_embeddings = None
        self.icd_embeddings = None
        
        # Load data
        self.load_data()
        
    def load_data(self):
        """Load LOINC and ICD-10-PCS data from CSVs"""
        print("Loading coding dictionaries...")
        try:
            # Load LOINC
            # Prioritize full dataset if available
            loinc_path = os.path.join(self.data_path, "LoincTableCore.csv")
            if not os.path.exists(loinc_path):
                 loinc_path = os.path.join(self.data_path, "loinc_sample.csv")
            
            if os.path.exists(loinc_path):
                print(f"Loading LOINC data from {loinc_path}...")
                self.loinc_df = pd.read_csv(loinc_path, low_memory=False)
                # Filter for Radiology related codes to optimize if needed, but keeping all for now allows broader search
                # self.loinc_df = self.loinc_df[self.loinc_df['CLASS'] == 'RAD'] 
                
                # Create a searchable text column
                self.loinc_df['search_text'] = self.loinc_df.apply(
                    lambda x: f"{x.get('LONG_COMMON_NAME', '')} {x.get('COMPONENT', '')} {x.get('METHOD_TYP', '')} {x.get('SYSTEM', '')}", 
                    axis=1
                ).str.lower()
                print(f"Loaded {len(self.loinc_df)} LOINC codes")
            else:
                print(f"Warning: LOINC file not found at {loinc_path}")
                self.loinc_df = pd.DataFrame()

            # Load ICD-10-PCS
            icd_path = os.path.join(self.data_path, "icd10pcs_sample.csv")
            if os.path.exists(icd_path):
                self.icd_df = pd.read_csv(icd_path)
                # Create a searchable text column
                self.icd_df['search_text'] = self.icd_df.apply(
                    lambda x: f"{x.get('DESCRIPTION', '')} {x.get('BODY_PART', '')}", 
                    axis=1
                ).str.lower()
                print(f"Loaded {len(self.icd_df)} ICD-10-PCS codes")
            else:
                print(f"Warning: ICD-10-PCS file not found at {icd_path}")
                self.icd_df = pd.DataFrame()
                
        except Exception as e:
            print(f"Error loading data: {e}")

    def initialize_keyword_search(self):
        """Initialize TF-IDF vectorizers"""
        if self.loinc_df is not None and not self.loinc_df.empty:
            print("Initializing LOINC keyword search...")
            self.tfidf_vectorizer_loinc = TfidfVectorizer(analyzer='word', stop_words='english', ngram_range=(1, 2))
            self.tfidf_matrix_loinc = self.tfidf_vectorizer_loinc.fit_transform(self.loinc_df['search_text'])
            
        if self.icd_df is not None and not self.icd_df.empty:
            print("Initializing ICD keyword search...")
            self.tfidf_vectorizer_icd = TfidfVectorizer(analyzer='word', stop_words='english', ngram_range=(1, 2))
            self.tfidf_matrix_icd = self.tfidf_vectorizer_icd.fit_transform(self.icd_df['search_text'])

    def initialize_semantic_search(self, model_name='pritamdeka/S-PubMedBert-MS-MARCO'):
        """Initialize Sentence Transformer model and embeddings with Biomedical Model"""
        print(f"Initializing semantic search with biomedical model {model_name}...")
        try:
            self.embedding_model = SentenceTransformer(model_name)
            
            if self.loinc_df is not None and not self.loinc_df.empty:
                print("Generating LOINC embeddings...")
                # Check for cached embeddings
                cache_path = os.path.join(self.data_path, "loinc_embeddings.pkl")
                if os.path.exists(cache_path):
                    with open(cache_path, 'rb') as f:
                        self.loinc_embeddings = pickle.load(f)
                else:
                    self.loinc_embeddings = self.embedding_model.encode(
                        self.loinc_df['search_text'].tolist(), 
                        show_progress_bar=True
                    )
                    with open(cache_path, 'wb') as f:
                        pickle.dump(self.loinc_embeddings, f)
            
            if self.icd_df is not None and not self.icd_df.empty:
                print("Generating ICD embeddings...")
                cache_path = os.path.join(self.data_path, "icd_embeddings.pkl")
                if os.path.exists(cache_path):
                    with open(cache_path, 'rb') as f:
                        self.icd_embeddings = pickle.load(f)
                else:
                    self.icd_embeddings = self.embedding_model.encode(
                        self.icd_df['search_text'].tolist(),
                        show_progress_bar=True
                    )
                    with open(cache_path, 'wb') as f:
                        pickle.dump(self.icd_embeddings, f)
                        
        except Exception as e:
            print(f"Error initializing semantic search: {e}")

    def search_keyword(self, query: str, code_type: str = 'both', top_k: int = 5) -> Dict:
        """
        Perform keyword (TF-IDF) search
        """
        results = {'loinc': [], 'icd': []}
        query = query.lower()
        
        if code_type in ['loinc', 'both'] and self.tfidf_vectorizer_loinc:
            query_vec = self.tfidf_vectorizer_loinc.transform([query])
            cosine_sims = cosine_similarity(query_vec, self.tfidf_matrix_loinc).flatten()
            top_indices = cosine_sims.argsort()[-top_k:][::-1]
            
            for idx in top_indices:
                score = cosine_sims[idx]
                if score > 0.1:  # Threshold
                    record = self.loinc_df.iloc[idx].to_dict()
                    record['score'] = float(score)
                    results['loinc'].append(record)
                    
        if code_type in ['icd', 'both'] and self.tfidf_vectorizer_icd:
            query_vec = self.tfidf_vectorizer_icd.transform([query])
            cosine_sims = cosine_similarity(query_vec, self.tfidf_matrix_icd).flatten()
            top_indices = cosine_sims.argsort()[-top_k:][::-1]
            
            for idx in top_indices:
                score = cosine_sims[idx]
                if score > 0.1:
                    record = self.icd_df.iloc[idx].to_dict()
                    record['score'] = float(score)
                    results['icd'].append(record)
                    
        return results

    def search_semantic(self, query: str, code_type: str = 'both', top_k: int = 5) -> Dict:
        """
        Perform semantic (Vector) search
        """
        results = {'loinc': [], 'icd': []}
        if not self.embedding_model:
            return results
            
        query_embedding = self.embedding_model.encode([query])
        
        if code_type in ['loinc', 'both'] and self.loinc_embeddings is not None:
            cosine_sims = cosine_similarity(query_embedding, self.loinc_embeddings).flatten()
            top_indices = cosine_sims.argsort()[-top_k:][::-1]
            
            for idx in top_indices:
                score = cosine_sims[idx]
                if score > 0.3:  # Higher threshold for semantic
                    record = self.loinc_df.iloc[idx].to_dict()
                    record['score'] = float(score)
                    results['loinc'].append(record)
                    
        if code_type in ['icd', 'both'] and self.icd_embeddings is not None:
            cosine_sims = cosine_similarity(query_embedding, self.icd_embeddings).flatten()
            top_indices = cosine_sims.argsort()[-top_k:][::-1]
            
            for idx in top_indices:
                score = cosine_sims[idx]
                if score > 0.3:
                    record = self.icd_df.iloc[idx].to_dict()
                    record['score'] = float(score)
                    results['icd'].append(record)
                    
        return results
        
    def search(self, query: str, strategy: str = 'hybrid', code_type: str = 'both', top_k: int = 5) -> Dict:
        """
        Unified search method supporting multiple strategies
        Strategies: 'keyword', 'semantic', 'hybrid'
        """
        if strategy == 'keyword':
            if not self.tfidf_vectorizer_loinc:
                self.initialize_keyword_search()
            return self.search_keyword(query, code_type, top_k)
            
        elif strategy == 'semantic':
            if not self.embedding_model:
                self.initialize_semantic_search()
            return self.search_semantic(query, code_type, top_k)
            
        else: # Hybrid (Simple merge for now, could be re-rank)
            # Ensure initialized
            if not self.tfidf_vectorizer_loinc:
                self.initialize_keyword_search()
            if not self.embedding_model:
                self.initialize_semantic_search()
                
            kw_results = self.search_keyword(query, code_type, top_k)
            sem_results = self.search_semantic(query, code_type, top_k)
            
            # Simple blending: take unique results, prioritize semantic score? 
            # Or just return both sections for frontend to display?
            # Let's return a structured object distinguishing them for now, or merge them.
            
            # Merging strategy: Dictionary by code to deduplicate
            merged = {'loinc': {}, 'icd': {}}
            
            # Process LOINC
            for res in kw_results['loinc']:
                res['strategy'] = 'keyword'
                merged['loinc'][res['LOINC_NUM']] = res
            for res in sem_results['loinc']:
                code = res['LOINC_NUM']
                if code in merged['loinc']:
                    # Boost score if found in both
                    merged['loinc'][code]['score'] = max(merged['loinc'][code]['score'], res['score'])
                    merged['loinc'][code]['strategy'] = 'hybrid'
                else:
                    res['strategy'] = 'semantic'
                    merged['loinc'][code] = res
                    
            # Process ICD
            for res in kw_results['icd']:
                res['strategy'] = 'keyword'
                merged['icd'][res['ICD10PCS_CODE']] = res
            for res in sem_results['icd']:
                code = res['ICD10PCS_CODE']
                if code in merged['icd']:
                    merged['icd'][code]['score'] = max(merged['icd'][code]['score'], res['score'])
                    merged['icd'][code]['strategy'] = 'hybrid'
                else:
                    res['strategy'] = 'semantic'
                    merged['icd'][code] = res
            
            # Convert back to list and sort
            final_results = {
                'loinc': sorted(merged['loinc'].values(), key=lambda x: x['score'], reverse=True)[:top_k],
                'icd': sorted(merged['icd'].values(), key=lambda x: x['score'], reverse=True)[:top_k]
            }
            
            return final_results
