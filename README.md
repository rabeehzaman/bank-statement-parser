# Bank Statement Parser

A minimal full-stack web application for uploading and parsing bank statements with automatic header detection.

## Features

- Automatic header row detection (scans first 20 rows)
- Parses Excel (.xls, .xlsx) and CSV files
- Normalizes transactions with date, description, and amount
- Displays transactions sorted newest-first
- Tags all records with account name "Rajhi_Ghadeer"

## Project Structure

```
.
├── backend/
│   ├── parser.py      # Core parsing logic with header detection
│   ├── main.py        # FastAPI server with upload endpoint
│   └── requirements.txt
└── frontend/
    └── src/
        ├── BankStatementUploader.jsx  # React component
        └── App.js
```

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
   
   The API will be available at http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm start
   ```
   
   The app will open at http://localhost:3000

## Usage

1. Make sure both backend and frontend servers are running
2. Open http://localhost:3000 in your browser
3. Click "Choose File" and select an Excel/CSV bank statement
4. Click "Upload" to process the file
5. View parsed transactions in the table

## API Endpoint

- `POST /api/upload-statement` - Upload and parse bank statement
  - Accepts: multipart/form-data with file field named "statement"
  - Returns: JSON array of transaction objects

## Transaction Format

Each transaction contains:
```json
{
  "date": "02-08-2025",
  "description": "Transaction details",
  "amount": 1234.56,
  "account_name": "Rajhi_Ghadeer"
}
```

## Error Handling

- Invalid file types return 400 error
- Missing header columns return descriptive error message
- Failed date parsing rows are automatically skipped