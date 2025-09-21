# enhanced_api.py - Corrected version with Image Analysis

# FIX #2: Added UploadFile and File to the imports
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from enhanced_ai import SuperPoweredNewsVerificationAI as NewsVerificationAI
import uvicorn
import datetime # FIX #3: Added datetime import

# Initialize FastAPI app
app = FastAPI(
    title="Enhanced News Verification AI - Day 2+",
    description="AI-powered news verification with URL, Text, and NEW Image analysis",
    version="2.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🚀 Loading Day 2+ Enhanced AI System...")
# NOTE: Ensure the class name here matches the one in your enhanced_ai.py file
analyzer = NewsVerificationAI() 
print("✅ Enhanced API ready to serve requests!")

# Request models
class URLAnalysisRequest(BaseModel):
    url: str

class TextAnalysisRequest(BaseModel):
    text: str

# API endpoints
@app.get("/")
async def home():
    """Welcome endpoint with API information"""
    return {
        "message": "🤖 Enhanced News Verification AI - Day 2+",
        "version": "2.1.0",
        "features": [
            "URL analysis with article extraction",
            "Direct text analysis",
            "Image-to-Text (OCR) analysis (NEW!)",
            "Comprehensive scoring system"
        ],
        "endpoints": {
            "analyze_url": "/analyze-url",
            "analyze_text": "/analyze-text",
            "analyze_image": "/analyze-image (NEW!)"
        }
    }

@app.post("/analyze-url")
async def analyze_url(request: URLAnalysisRequest):
    """Analyze a complete news article from a URL"""
    try:
        if not request.url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Invalid URL format.")
        
        result = analyzer.analyze_url_complete(request.url)
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        return {"success": True, "result": result}
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# This new endpoint is correct as you had it.
@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze text from an uploaded image"""
    try:
        image_bytes = await file.read()
        result = analyzer.analyze_image_complete(image_bytes)
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        return {"success": True, "analysis_type": "image_analysis", "result": result}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during image analysis: {str(e)}")


# FIX #1: This is the single, correct, refactored version of the endpoint.
# The duplicate, longer version has been removed.
@app.post("/analyze-text")
async def analyze_text(request: TextAnalysisRequest):
    """Analyze text content directly"""
    try:
        if not request.text or len(request.text) < 10:
            raise HTTPException(status_code=400, detail="Text is too short for meaningful analysis.")
        
        result = analyzer.analyze_text_comprehensive(request.text)
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])

        return {"success": True, "analysis_type": "text_analysis", "result": result}
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during text analysis: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "ai_models": "loaded"}


@app.get("/test")
async def comprehensive_test():
    """Comprehensive test of all features"""
    return {
        "overall_status": "operational",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# The rest of the file (demo examples and server start) is okay.
# ... (you can keep your existing /demo-examples and start_enhanced_server code)
def start_enhanced_server():
    print("🌐 Starting Enhanced News Verification API (Day 2+)...")
    print("📚 API documentation: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_enhanced_server()