"""
Mini Judge - FastAPI Backend
Main entry point for the application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from .analyzer import CodeAnalyzer
from .runner import CodeRunner

app = FastAPI(
    title="Mini Judge",
    description="A code analysis and execution platform with pre-compile checks",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer and runner
analyzer = CodeAnalyzer()
runner = CodeRunner()


# Request/Response Models
class AnalyzeRequest(BaseModel):
    code: str
    rules: Optional[List[str]] = None


class RunCodeRequest(BaseModel):
    code: str
    language: str
    test_input: Optional[str] = ""
    expected_output: Optional[str] = None


class TestCase(BaseModel):
    input: str = ""
    expected_output: str


class RunTestCasesRequest(BaseModel):
    code: str
    language: str
    test_cases: List[TestCase]


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Mini Judge API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze - Analyze code for syntax issues",
            "run": "/run - Execute code",
            "test": "/test - Run multiple test cases",
            "rules": "/rules - List available rules",
        }
    }


@app.get("/rules")
async def list_rules():
    """List all available analysis rules"""
    return {
        "rules": [
            {
                "name": "full_width",
                "description": "Detects full-width symbols that should be half-width",
                "examples": ["（", "）", "；", "，"]
            },
            {
                "name": "brackets",
                "description": "Detects unmatched or mismatched brackets",
                "examples": ["Unclosed (", "Mismatched [}"]
            },
            {
                "name": "quotes",
                "description": "Detects unclosed string quotes",
                "examples": ["Unclosed '", 'Unclosed "']
            },
            {
                "name": "confusable",
                "description": "Detects visually similar characters that might cause errors",
                "examples": ["Cyrillic а vs Latin a", "Greek ο vs Latin o"]
            }
        ]
    }


@app.post("/analyze")
async def analyze_code_endpoint(request: AnalyzeRequest):
    """
    Analyze code for potential issues
    
    Args:
        request: AnalyzeRequest with code and optional list of rules
        
    Returns:
        Analysis results including issues found
    """
    try:
        result = analyzer.analyze(request.code, request.rules)
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/analyze/formatted")
async def analyze_code_formatted(request: AnalyzeRequest):
    """
    Analyze code and return formatted output
    
    Args:
        request: AnalyzeRequest with code and optional list of rules
        
    Returns:
        Formatted analysis results as a string
    """
    try:
        formatted_result = analyzer.analyze_and_format(request.code, request.rules)
        return {
            "success": True,
            "formatted_output": formatted_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/run")
async def run_code_endpoint(request: RunCodeRequest):
    """
    Execute code and optionally compare with expected output
    
    Args:
        request: RunCodeRequest with code, language, input, and expected output
        
    Returns:
        Execution results
    """
    try:
        result = runner.run_code(
            request.code,
            request.language,
            request.test_input,
            request.expected_output
        )
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")


@app.post("/test")
async def run_test_cases_endpoint(request: RunTestCasesRequest):
    """
    Run multiple test cases
    
    Args:
        request: RunTestCasesRequest with code, language, and test cases
        
    Returns:
        Test results for all cases
    """
    try:
        # Convert Pydantic models to dicts
        test_cases = [tc.model_dump() for tc in request.test_cases]
        
        result = runner.run_test_cases(
            request.code,
            request.language,
            test_cases
        )
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test execution error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
