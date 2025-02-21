# Exposes HTTP endpoint for model inference

import os
import logging
from typing import Optional, List, Dict, Any
import json

import torch
import torch.nn.functional as F
from transformers import PreTrainedTokenizerBase
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from model import IndieGOConfig, IndieGOForCausalLM

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

app = FastAPI(title="IndieGO AI Service")

class GenerationConfig(BaseModel):
    """Configuration for text generation"""
    prompt: str
    max_length: int = 1024
    min_length: int = 0
    do_sample: bool = True
    early_stopping: bool = False
    num_beams: int = 1
    temperature: float = 1.0
    top_k: int = 50
    top_p: float = 1.0
    repetition_penalty: float = 1.0
    length_penalty: float = 1.0
    no_repeat_ngram_size: int = 0
    num_return_sequences: int = 1

class CodeAnalysisConfig(BaseModel):
    """Configuration for code analysis"""
    code: str
    max_length: int = 1024
    analysis_type: str = "all"  # One of: all, security, performance, style

class ModelResponse(BaseModel):
    """Model response format"""
    generated_text: Optional[str] = None
    analysis_results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class ModelServer:
    def __init__(
        self,
        model_path: str,
        tokenizer_path: Optional[str] = None,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
    ):
        self.device = device
        
        # Load model
        logger.info(f"Loading model from {model_path}")
        self.model = IndieGOForCausalLM.from_pretrained(model_path)
        self.model.to(device)
        self.model.eval()
        
        # Load tokenizer
        tokenizer_path = tokenizer_path or model_path
        logger.info(f"Loading tokenizer from {tokenizer_path}")
        self.tokenizer = PreTrainedTokenizerBase.from_pretrained(tokenizer_path)
    
    @torch.no_grad()
    def generate(self, config: GenerationConfig) -> ModelResponse:
        try:
            # Tokenize input
            inputs = self.tokenizer(
                config.prompt,
                return_tensors="pt",
                truncation=True,
                max_length=config.max_length,
            ).to(self.device)
            
            # Generate
            outputs = self.model.generate(
                **inputs,
                max_length=config.max_length,
                min_length=config.min_length,
                do_sample=config.do_sample,
                early_stopping=config.early_stopping,
                num_beams=config.num_beams,
                temperature=config.temperature,
                top_k=config.top_k,
                top_p=config.top_p,
                repetition_penalty=config.repetition_penalty,
                length_penalty=config.length_penalty,
                no_repeat_ngram_size=config.no_repeat_ngram_size,
                num_return_sequences=config.num_return_sequences,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
            
            # Decode output
            generated_text = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True,
            )
            
            return ModelResponse(generated_text=generated_text)
        
        except Exception as e:
            logger.error(f"Generation error: {str(e)}")
            return ModelResponse(error=str(e))
    
    @torch.no_grad()
    def analyze_code(self, config: CodeAnalysisConfig) -> ModelResponse:
        try:
            # Prepare prompt for code analysis
            if config.analysis_type == "security":
                prompt = f"Analyze this code for security issues:\n\n{config.code}\n\nSecurity Analysis:"
            elif config.analysis_type == "performance":
                prompt = f"Analyze this code for performance improvements:\n\n{config.code}\n\nPerformance Analysis:"
            elif config.analysis_type == "style":
                prompt = f"Analyze this code for style and best practices:\n\n{config.code}\n\nStyle Analysis:"
            else:
                prompt = f"Analyze this code comprehensively:\n\n{config.code}\n\nAnalysis:"
            
            # Generate analysis
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=config.max_length,
            ).to(self.device)
            
            outputs = self.model.generate(
                **inputs,
                max_length=config.max_length,
                min_length=0,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
            
            # Parse and structure the analysis
            analysis_text = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True,
            )
            
            # Extract insights from the generated analysis
            analysis_results = {
                "type": config.analysis_type,
                "summary": analysis_text.split("\n")[0],
                "details": analysis_text.split("\n")[1:],
            }
            
            if config.analysis_type == "all":
                # Try to categorize insights
                security_issues = []
                performance_tips = []
                style_suggestions = []
                
                for line in analysis_text.split("\n"):
                    if "security" in line.lower():
                        security_issues.append(line)
                    elif "performance" in line.lower():
                        performance_tips.append(line)
                    elif "style" in line.lower():
                        style_suggestions.append(line)
                
                analysis_results.update({
                    "security_issues": security_issues,
                    "performance_tips": performance_tips,
                    "style_suggestions": style_suggestions,
                })
            
            return ModelResponse(analysis_results=analysis_results)
        
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            return ModelResponse(error=str(e))

# Initialize model server
model_server = None

@app.on_event("startup")
async def startup_event():
    global model_server
    model_path = os.getenv("MODEL_PATH", "checkpoints/best")
    tokenizer_path = os.getenv("TOKENIZER_PATH")
    
    model_server = ModelServer(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
    )
    logger.info("Model server initialized")

@app.post("/generate", response_model=ModelResponse)
async def generate(config: GenerationConfig):
    if model_server is None:
        raise HTTPException(status_code=503, detail="Model server not initialized")
    return model_server.generate(config)

@app.post("/analyze", response_model=ModelResponse)
async def analyze_code(config: CodeAnalysisConfig):
    if model_server is None:
        raise HTTPException(status_code=503, detail="Model server not initialized")
    return model_server.analyze_code(config)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "serve:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )