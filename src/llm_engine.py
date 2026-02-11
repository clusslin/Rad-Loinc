
import os
import torch
import gc
from typing import List, Dict, Optional, Generator
import threading
import time

# Try to import vllm; if not available, fallback might be needed or just error out
try:
    from vllm import LLM, SamplingParams
    VLLM_AVAILABLE = True
except ImportError:
    VLLM_AVAILABLE = False
    print("Warning: vllm not installed. LLM features will be disabled.")

class MedicalLLMEngine:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(MedicalLLMEngine, cls).__new__(cls)
                    cls._instance.model = None
                    cls._instance.model_name = "aaditya/OpenBioLLM-Llama3-8B"
                    cls._instance.is_loading = False
        return cls._instance

    def is_loaded(self) -> bool:
        return self.model is not None

    def load_model(self, model_name: str = None) -> Dict:
        """
        Load the LLM model into memory.
        This is a heavy operation and should be called explicitly.
        """
        if self.is_loaded():
            return {"status": "already_loaded", "model": self.model_name}
        
        if self.is_loading:
             return {"status": "loading_in_progress"}

        if not VLLM_AVAILABLE:
            raise ImportError("vllm python package is not installed. Please install it to use AI features.")

        if model_name:
            self.model_name = model_name

        self.is_loading = True
        try: 
            print(f"Loading LLM: {self.model_name}...")
            # Detect hardware constraints
            gpu_memory_utilization = 0.6  # Conservative default for Mac/Low VRAM
            if torch.cuda.is_available():
                # Nvidia GPU logic
                gpu_memory_utilization = 0.8
            elif torch.backends.mps.is_available():
                # Apple Silicon (MPS)
                # vLLM support on MPS is experimental/limited in some versions
                # Check documentation or try standard load
                pass 
            
            # Initialize vLLM
            self.model = LLM(
                model=self.model_name,
                trust_remote_code=True,
                dtype="float16", # or "half"
                gpu_memory_utilization=gpu_memory_utilization,
                max_model_len=4096 # Limit context window to save memory
            )
            print("LLM Loaded successfully.")
            return {"status": "loaded", "model": self.model_name}
            
        except Exception as e:
            print(f"Failed to load LLM: {e}")
            self.model = None
            raise e
        finally:
            self.is_loading = False

    def unload_model(self):
        """Free up memory"""
        if self.model:
            del self.model
            self.model = None
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()
            print("LLM Unloaded.")
            return {"status": "unloaded"}
        return {"status": "not_loaded"}

    def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        """
        Generate a response for a single turn or a prompt.
        For conversational, the 'prompt' should include the chat history formatted.
        """
        if not self.is_loaded():
            raise RuntimeError("Model is not loaded. Please load the model first.")

        # Default system prompt for Radiology if not provided
        if not system_prompt:
            system_prompt = (
                "You are an expert radiologist and medical coder AI. "
                "Your task is to analyze radiology reports and assist with LOINC and ICD-10-PCS coding. "
                "Provide clear, professional, and medically accurate explanations."
            )

        # Construct full prompt with chat template format (Llama 3 style)
        # Llama 3 format:
        # <|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n
        
        full_prompt = (
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|>"
            f"<|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|>"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )

        sampling_params = SamplingParams(
            temperature=0.2, # Low temp for factual accuracy
            max_tokens=1024,
            stop=["<|eot_id|>"]
        )

        outputs = self.model.generate([full_prompt], sampling_params)
        generated_text = outputs[0].outputs[0].text
        return generated_text.strip()

# Create a global instance
llm_engine = MedicalLLMEngine()
