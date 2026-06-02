import base64
import binascii
import html
import json
import re
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

app = FastAPI(
    title="Text Encoding Converter API",
    description="Convert text between common encodings: base64, hex, URL encoding, HTML entities",
    version="1.0.0"
)

# Demo key for free tier
DEMO_KEY = "free-demo-key"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(key: str = Security(api_key_header)):
    if key is None or key != DEMO_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return key

class TextRequest(BaseModel):
    text: str = Field(..., description="Text to encode/decode")

class Base64Request(TextRequest):
    pass

class HexRequest(TextRequest):
    encoding: str = Field("utf-8", description="Encoding for text input (utf-8 by default)")

class UrlRequest(TextRequest):
    pass

class HtmlRequest(TextRequest):
    mode: str = Field("encode", description="encode or decode")

class ConvertResponse(BaseModel):
    input: str
    output: str
    success: bool = True

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/base64/decode", dependencies=[Depends(verify_api_key)])
async def base64_decode(req: Base64Request):
    """Decode base64 string to plain text"""
    try:
        decoded = base64.b64decode(req.text).decode("utf-8")
        return ConvertResponse(input=req.text, output=decoded)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 input: {str(e)}")

@app.post("/base64/encode", dependencies=[Depends(verify_api_key)])
async def base64_encode(req: Base64Request):
    """Encode plain text to base64 string"""
    try:
        encoded = base64.b64encode(req.text.encode("utf-8")).decode("utf-8")
        return ConvertResponse(input=req.text, output=encoded)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/hex/decode", dependencies=[Depends(verify_api_key)])
async def hex_decode(req: HexRequest):
    """Decode hex string to plain text"""
    try:
        # Handle both with and without 0x prefix
        hex_str = req.text.replace("0x", "").replace("0X", "")
        decoded = bytes.fromhex(hex_str).decode(req.encoding)
        return ConvertResponse(input=req.text, output=decoded)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid hex input: {str(e)}")

@app.post("/hex/encode", dependencies=[Depends(verify_api_key)])
async def hex_encode(req: HexRequest):
    """Encode plain text to hex string"""
    try:
        encoded = req.text.encode(req.encoding).hex()
        return ConvertResponse(input=req.text, output=encoded)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/url/encode", dependencies=[Depends(verify_api_key)])
async def url_encode(req: UrlRequest):
    """URL encode (percent-encode) a string"""
    from urllib.parse import quote
    try:
        encoded = quote(req.text, safe="")
        return ConvertResponse(input=req.text, output=encoded)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/url/decode", dependencies=[Depends(verify_api_key)])
async def url_decode(req: UrlRequest):
    """URL decode a percent-encoded string"""
    from urllib.parse import unquote
    try:
        decoded = unquote(req.text)
        return ConvertResponse(input=req.text, output=decoded)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/html/encode", dependencies=[Depends(verify_api_key)])
async def html_encode(req: HtmlRequest):
    """Convert special characters to HTML entities"""
    if req.mode != "encode":
        raise HTTPException(status_code=400, detail="Use mode='encode' for this endpoint")
    encoded = html.escape(req.text)
    return ConvertResponse(input=req.text, output=encoded)

@app.post("/html/decode", dependencies=[Depends(verify_api_key)])
async def html_decode(req: HtmlRequest):
    """Convert HTML entities back to characters"""
    if req.mode != "decode":
        raise HTTPException(status_code=400, detail="Use mode='decode' for this endpoint")
    decoded = html.unescape(req.text)
    return ConvertResponse(input=req.text, output=decoded)

@app.post("/json/validate", dependencies=[Depends(verify_api_key)])
async def json_validate(req: TextRequest):
    """Validate JSON and return formatted version"""
    try:
        parsed = json.loads(req.text)
        formatted = json.dumps(parsed, indent=2)
        return {"input": req.text, "output": formatted, "valid": True, "success": True}
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")

@app.post("/json/minify", dependencies=[Depends(verify_api_key)])
async def json_minify(req: TextRequest):
    """Minify JSON string"""
    try:
        parsed = json.loads(req.text)
        minified = json.dumps(parsed, separators=(",", ":"))
        return ConvertResponse(input=req.text, output=minified)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")

try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except ImportError:
    pass