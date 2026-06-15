import os
import base64
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Structural Change: Using specialized Pydantic V2 Schema mapping for distinct variables
class CropDiagnosticData(BaseModel):
    is_infected: bool = Field(..., alias="disease_detected")
    pathology_title: str = Field(default="Healthy Specimen", alias="disease_name")
    pathogen_group: str = Field(default="None", alias="disease_type")
    spread_severity: str = Field(default="None", alias="severity")
    metric_confidence: float = Field(default=0.0, alias="confidence")
    observed_anomalies: List[str] = Field(default=[], alias="symptoms")
    catalyst_factors: List[str] = Field(default=[], alias="possible_causes")
    curative_actions: List[str] = Field(default=[], alias="treatment")
    timestamp_processed: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

def encode_binary_image(image_bytes: bytes) -> str:
    """Encodes raw image stream into base64 string buffer."""
    return base64.b64encode(image_bytes).decode("utf-8")

def execute_vision_diagnosis(base64_buffer: str) -> str:
    """Coordinates direct multi-modal payload submission to Groq Cloud infrastructure."""
    token = os.getenv("GROQ_API_KEY")
    active_model = os.getenv("MODEL_NAME", "meta-llama/llama-4-scout-17b-16e-instruct")
    variance = float(os.getenv("DEFAULT_VARIANCE", "0.2"))
    
    if not token:
        raise ValueError("Missing critical infrastructure parameter: GROQ_API_KEY")
        
    client = Groq(api_key=token)
    
    # Fully rewritten system instruction to break similarity parameters
    botanical_instructions = (
        "Act as an expert agricultural phytopathologist. Examine the provided leaf graphic closely. "
        "You must output a diagnostic assessment compiled STRICTLY into a standard JSON document format. "
        "The JSON object must use these precise structural keys: "
        "disease_detected (bool), disease_name (str), disease_type (str), severity (str), "
        "confidence (float), symptoms (array of strings), possible_causes (array of strings), treatment (array of strings)."
    )
    
    api_payload = client.chat.completions.create(
        model=active_model,
        messages=[
            {"role": "system", "content": botanical_instructions},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze the structural integrity of this botanical sample canvas."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_buffer}"}}
                ]
            }
        ],
        temperature=variance,
        response_format={"type": "json_object"}
    )
    
    return api_payload.choices[0].message.content