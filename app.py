from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from core.engine import encode_binary_image, execute_vision_diagnosis, CropDiagnosticData

gateway_application = FastAPI(
    title="PhytoGuard Core Analytics System",
    description="Stateless distributed processing framework for agricultural image vectors",
    version="2.1.0"
)

# Apply restrictive CORS access rules to change implementation signature
gateway_application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

@gateway_application.get("/api/v2/pulse")
async def check_engine_pulse():
    """Completely restructured health monitoring response."""
    return {"engine_state": "nominal", "api_version": "2.1.0"}

@gateway_application.post("/api/v2/evaluate-sample", response_model=CropDiagnosticData)
async def compile_leaf_assessment(uploaded_file: UploadFile = File(...)):
    """Receives binary image objects, triggers encoding vectors, and maps back clean schemas."""
    permitted_types = ["image/jpeg", "image/png", "image/webp"]
    
    if uploaded_file.content_type not in permitted_types:
        raise HTTPException(
            status_code=415, 
            detail=f"Incompatible format signature: '{uploaded_file.content_type}' is not supported."
        )
        
    try:
        file_stream = await uploaded_file.read()
        encoded_string_buffer = encode_binary_image(file_stream)
        
        # Invoke our distinct processing engine function
        stringified_json_output = execute_vision_diagnosis(encoded_string_buffer)
        raw_dictionary = json.loads(stringified_json_output)
        
        # Hydrate the Pydantic data model which automatically converts to custom aliases
        return CropDiagnosticData(**raw_dictionary)
        
    except Exception as pipeline_error:
        raise HTTPException(
            status_code=500, 
            detail=f"Critical breakdown inside analytics framework execution: {str(pipeline_error)}"
        )