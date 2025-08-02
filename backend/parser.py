import pandas as pd
from typing import List, Dict
import json
from datetime import datetime


def parse_bank_statement(path: str) -> List[Dict]:
    """
    Parse an Excel bank statement with automatic header detection.
    
    Args:
        path: Path to the Excel file
        
    Returns:
        List of transaction dictionaries with date, description, amount, and account_name
        
    Raises:
        ValueError: If header row cannot be detected
    """
    # Step 1: Header Detection
    # Read first 20 rows without header
    df_preview = pd.read_excel(path, header=None, nrows=20)
    
    # Define expected column names
    expected_columns = ["Date", "Credit", "Debit", "Transaction Details"]
    
    # Find header row
    header_row = None
    for idx in range(20):
        row_values = df_preview.iloc[idx].astype(str).str.strip()
        matches = sum(1 for col in expected_columns if any(col.lower() in val.lower() for val in row_values))
        if matches >= 3:
            header_row = idx
            break
    
    if header_row is None:
        raise ValueError(
            f"Could not detect header row. Expected at least 3 of these columns: {', '.join(expected_columns)}"
        )
    
    # Step 2: Data Loading & Cleaning
    # Reload with detected header
    df = pd.read_excel(path, header=header_row)
    
    # Reset index to preserve original order
    df.reset_index(drop=True, inplace=True)
    df['orig_idx'] = df.index
    
    # Parse dates with dayfirst=True
    df['parsed_date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    
    # Drop rows with invalid dates
    df = df.dropna(subset=['parsed_date'])
    
    # Step 3: Field Transformation
    # Combine Transaction Details columns
    if 'Transaction Details' in df.columns and 'Transaction Details.1' in df.columns:
        df['Transaction Details'] = df['Transaction Details'].fillna('')
        df['Transaction Details.1'] = df['Transaction Details.1'].fillna('')
        df['description'] = df['Transaction Details'].astype(str) + ' - ' + df['Transaction Details.1'].astype(str)
        # Clean up double spaces and trailing separators
        df['description'] = df['description'].str.strip().str.replace(' - $', '', regex=True)
    elif 'Transaction Details' in df.columns:
        df['description'] = df['Transaction Details'].fillna('').astype(str)
    else:
        df['description'] = ''
    
    # Calculate amount (credits positive, debits negative)
    df['Credit'] = pd.to_numeric(df.get('Credit', 0), errors='coerce').fillna(0)
    df['Debit'] = pd.to_numeric(df.get('Debit', 0), errors='coerce').fillna(0)
    df['amount'] = df['Credit'] - df['Debit']
    
    # Format date as dd-mm-YYYY
    df['date'] = df['parsed_date'].dt.strftime('%d-%m-%Y')
    
    # Add account name
    df['account_name'] = 'Rajhi_Ghadeer'
    
    # Step 4: Sorting
    # Sort by date descending, then by original index descending
    df = df.sort_values(['parsed_date', 'orig_idx'], ascending=[False, False])
    
    # Step 5: Output
    # Create list of dictionaries with only required fields
    transactions = []
    for _, row in df.iterrows():
        transactions.append({
            'date': row['date'],
            'description': row['description'],
            'amount': float(row['amount']),
            'account_name': row['account_name']
        })
    
    return transactions