from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import os
from parser import parse_bank_statement

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "https://*.railway.app", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload-statement")
async def upload_statement(statement: UploadFile = File(...)):
    """
    Upload and parse a bank statement file.
    
    Args:
        statement: The uploaded file (Excel or CSV)
        
    Returns:
        JSON array of parsed transactions
    """
    # Validate file extension
    allowed_extensions = ['.xls', '.xlsx', '.csv']
    file_extension = os.path.splitext(statement.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Save uploaded file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            # Write uploaded content to temp file
            content = await statement.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Parse the bank statement
        try:
            transactions = parse_bank_statement(temp_path)
            return JSONResponse(content=transactions)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")
        
    finally:
        # Clean up temp file
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)

@app.get("/")
async def root():
    return {"message": "Bank Statement Parser API"}