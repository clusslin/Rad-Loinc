from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import io
import os
from pathlib import Path
from datetime import datetime

# Local imports
from .loinc_mapper import LOINCMapper
from .icd10pcs_mapper import ICD10PCSMapper
from .excel_processor import ExcelProcessor
from .search_engine import UnifiedSearchEngine
# LLM Engine is imported conditionally inside endpoints or here? 
# To avoid heavy imports just for checking status, let's import the wrapper
try:
    from .llm_engine import llm_engine
except ImportError:
    llm_engine = None

app = FastAPI(title="Rad-LOINC Mapper API")

# Initialize mappers and search engine
loinc_mapper = LOINCMapper()
icd10pcs_mapper = ICD10PCSMapper()
excel_processor = ExcelProcessor()
search_engine = UnifiedSearchEngine(data_path="data")

# Models
class MappingRequest(BaseModel):
    modality: str
    study_desc: str
    chinese_desc: Optional[str] = ""
    contrast: Optional[str] = "N"

class SearchRequest(BaseModel):
    query: str
    strategy: str = "hybrid" # keyword, semantic, hybrid
    code_type: str = "both" # loinc, icd, both
    top_k: int = 10

class ChatRequest(BaseModel):
    prompt: str
    system_prompt: Optional[str] = None
    
# Static files
PROJECT_ROOT = Path(__file__).resolve().parent.parent
WEB_DIR = PROJECT_ROOT / "web"
EXAMPLES_DIR = PROJECT_ROOT / "examples"

app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")

@app.get("/")
async def read_index():
    return FileResponse(str(WEB_DIR / "index.html"))

import math

def clean_nans(data):
    """Recursively replace NaN and Infinity with None for JSON compliance"""
    if isinstance(data, dict):
        return {k: clean_nans(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_nans(v) for v in data]
    elif isinstance(data, float):
        if math.isnan(data) or math.isinf(data):
            return None
    return data

# LLM Endpoints
@app.get("/api/llm/status")
async def get_llm_status():
    if not llm_engine:
        return {"status": "unavailable", "message": "LLM Engine not initialized correctly."}
    return {"status": "loaded" if llm_engine.is_loaded() else "unloaded", "model": llm_engine.model_name}

@app.post("/api/llm/load")
async def load_llm():
    if not llm_engine:
         raise HTTPException(status_code=500, detail="LLM Engine unavailable")
    try:
        # This is a heavy blocking operation, ideally run in threadpool
        # But vLLM might not like threading. Let's try direct call for now or use run_in_executor
        import asyncio
        loop = asyncio.get_event_loop()
        # Creating a wrapper because load_model doesn't take args in run_in_executor easily
        await loop.run_in_executor(None, llm_engine.load_model)
        return {"status": "loaded", "model": llm_engine.model_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/llm/unload")
async def unload_llm():
    if not llm_engine:
         raise HTTPException(status_code=500, detail="LLM Engine unavailable")
    try:
        llm_engine.unload_model()
        return {"status": "unloaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/llm/chat")
async def chat_with_llm(request: ChatRequest):
    if not llm_engine or not llm_engine.is_loaded():
         raise HTTPException(status_code=400, detail="Model not loaded. Please load the model first.")
    try:
        # Run generation in thread to avoid blocking event loop
        import asyncio
        loop = asyncio.get_event_loop()
        
        response_text = await loop.run_in_executor(
            None, 
            llm_engine.generate_response, 
            request.prompt, 
            request.system_prompt
        )
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search")
async def search_codes(request: SearchRequest):
    """
    Search for LOINC or ICD-10-PCS codes using specified strategy.
    Strategies: 'keyword' (TF-IDF), 'semantic' (Embeddings), 'hybrid' (Combined)
    """
    try:
        results = search_engine.search(
            query=request.query, 
            strategy=request.strategy, 
            code_type=request.code_type,
            top_k=request.top_k
        )
        return clean_nans(results)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/map")
async def map_single_study(request: MappingRequest):
    try:
        # 1. Map LOINC
        loinc_result = loinc_mapper.map_study_to_loinc(
            value_code="REQ",
            modality=request.modality,
            study_desc=request.study_desc,
            chinese_desc=request.chinese_desc,
            contrast=request.contrast
        )
        
        # 2. Map ICD-10-PCS
        icd_result = icd10pcs_mapper.map_study_to_icd10pcs(
            value_code="REQ",
            modality=request.modality,
            study_desc=request.study_desc,
            chinese_desc=request.chinese_desc,
            contrast=request.contrast
        )
        
        # Merge results for frontend
        response = {
            **loinc_result,
            "icd10pcs_code": icd_result.get("icd10pcs_code"),
            "icd10pcs_description": icd_result.get("icd10pcs_description"),
            "icd10pcs_section": icd_result.get("icd10pcs_section"),
            "icd10pcs_mapping_confidence": icd_result.get("mapping_confidence"),
            # Combine issues
            "all_issues": list(set(loinc_result.get("issues", []) + icd_result.get("issues", []))),
            "has_issues": loinc_result.get("has_issues") or icd_result.get("has_issues")
        }
        
        return clean_nans(response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process_file")
async def process_batch_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload Excel or CSV.")
    
    try:
        contents = await file.read()
        file_bytes = io.BytesIO(contents)
        
        # Load DataFrame
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_bytes)
        else:
            df = pd.read_excel(file_bytes)
            
        # Validate columns
        required_cols = ['modality', 'Study Description']
        missing = [col for col in required_cols if col not in df.columns]
        
        # If value_code is missing, generate one
        if 'value_code' not in df.columns:
             df['value_code'] = [f'ROW_{i+1}' for i in range(len(df))]
             
        if missing:
             raise HTTPException(status_code=400, detail=f"Missing required columns: {', '.join(missing)}")

        # Convert to studies dict list
        studies = df.to_dict('records')
        
        # Run mapping
        loinc_results = loinc_mapper.map_batch(studies)
        icd_results = icd10pcs_mapper.map_batch(studies)
        
        output_data = []
        for l_res, i_res in zip(loinc_results, icd_results):
            # Combine issues
            all_issues = set()
            if l_res.get('issues'):
                all_issues.update([f"LOINC: {issue}" for issue in l_res['issues']])
            if i_res.get('issues'):
                all_issues.update([f"ICD-10-PCS: {issue}" for issue in i_res['issues']])

            has_any_issues = l_res.get('has_issues') or i_res.get('has_issues')

            row = {
                'value_code': l_res.get('value_code', ''),
                'modality': l_res.get('modality', ''),
                'Study Description': l_res.get('study_description', ''),
                'Chinese Study Description': l_res.get('chinese_description', ''),
                'Contrast': l_res.get('contrast', ''),
                'Combine Modality': l_res.get('combine_modality', ''),
                'Primary Modality': l_res.get('primary_modality', ''),
                'Expanded Description': l_res.get('expanded_description', ''),
                'Body Parts': ', '.join(l_res.get('body_parts', [])),
                'Laterality': l_res.get('laterality', '') or '',

                # LOINC columns
                'LOINC Code': l_res.get('loinc_code', '') or '',
                'LOINC Name': l_res.get('loinc_long_name', '') or '',
                'LOINC Component': l_res.get('loinc_component', '') or '',
                'LOINC Method': l_res.get('loinc_method', '') or '',
                'LOINC Confidence': l_res.get('mapping_confidence', ''),

                # ICD-10-PCS columns
                'ICD-10-PCS Code': i_res.get('icd10pcs_code', '') or '',
                'ICD-10-PCS Description': i_res.get('icd10pcs_description', '') or '',
                'ICD-10-PCS Section': i_res.get('icd10pcs_section', '') or '',
                'ICD-10-PCS Body System': i_res.get('icd10pcs_body_system', '') or '',
                'ICD-10-PCS Root Type': i_res.get('icd10pcs_root_type', '') or '',
                'ICD-10-PCS Confidence': i_res.get('mapping_confidence', ''),

                # Combined issues
                'Has Issues': 'Yes' if has_any_issues else 'No',
                'Issues': '; '.join(sorted(all_issues)) if all_issues else ''
            }
            output_data.append(row)
            
        result_df = pd.DataFrame(output_data)
        
        # Write to BytesIO
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            result_df.to_excel(writer, index=False, sheet_name='Mapped Results')
        
        output.seek(0)
        
        filename = f"mapped_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        from fastapi.responses import StreamingResponse
        
        # Reset pointer for reading
        output.seek(0)
        
        return StreamingResponse(
            output, 
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': f'attachment; filename="{filename}"'}
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{filename}")
async def download_example(filename: str):
    # Try to find file in examples dir
    if filename == "sample_input":
        path = EXAMPLES_DIR / "sample_input.csv"
    elif filename == "rad_template":
        path = EXAMPLES_DIR / "rad.xlsx"
        if not path.exists():
            # If template doesn't exist, try to generate one or check prepared
            path = EXAMPLES_DIR / "rad_prepared.xlsx"
    else:
        # Generic try
        path = EXAMPLES_DIR / filename
        if not path.exists():
             path = EXAMPLES_DIR / (filename + ".xlsx")
        if not path.exists():
             path = EXAMPLES_DIR / (filename + ".csv")
    
    if path and path.exists():
        return FileResponse(str(path), filename=path.name)
        
    raise HTTPException(status_code=404, detail="File not found")
