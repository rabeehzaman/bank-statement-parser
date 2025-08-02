import React, { useState } from 'react';

const BankStatementUploader = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const allowedTypes = ['.xls', '.xlsx', '.csv'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      
      if (!allowedTypes.includes(fileExtension)) {
        setError(`Invalid file type. Please upload ${allowedTypes.join(', ')} files only.`);
        setSelectedFile(null);
        return;
      }
      
      setSelectedFile(file);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file to upload');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('statement', selectedFile);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/upload-statement`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to upload file');
      }

      const data = await response.json();
      
      // Add category field to each transaction
      const transactionsWithCategory = data.map(transaction => ({
        ...transaction,
        category: 'Uncategorized'
      }));
      
      setTransactions(transactionsWithCategory);
      setSelectedFile(null);
      // Clear file input
      document.getElementById('file-input').value = '';
    } catch (err) {
      setError(err.message || 'Error uploading file');
    } finally {
      setLoading(false);
    }
  };

  const formatAmount = (amount) => {
    const absAmount = Math.abs(amount);
    const formatted = absAmount.toFixed(2);
    return amount < 0 ? `-${formatted}` : formatted;
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Bank Statement Uploader</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <input
          id="file-input"
          type="file"
          accept=".xls,.xlsx,.csv"
          onChange={handleFileChange}
          style={{ marginRight: '10px' }}
        />
        <button 
          onClick={handleUpload} 
          disabled={loading || !selectedFile}
          style={{
            padding: '8px 16px',
            backgroundColor: loading || !selectedFile ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading || !selectedFile ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </div>

      {error && (
        <div style={{
          padding: '10px',
          backgroundColor: '#fee',
          color: '#c00',
          borderRadius: '4px',
          marginBottom: '20px'
        }}>
          Error: {error}
        </div>
      )}

      {transactions.length > 0 && (
        <div>
          <h2>Transactions</h2>
          <table style={{
            width: '100%',
            borderCollapse: 'collapse',
            marginTop: '10px'
          }}>
            <thead>
              <tr style={{ backgroundColor: '#f8f9fa' }}>
                <th style={{ padding: '10px', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Date</th>
                <th style={{ padding: '10px', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Description</th>
                <th style={{ padding: '10px', textAlign: 'right', borderBottom: '2px solid #dee2e6' }}>Amount</th>
                <th style={{ padding: '10px', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>Category</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((transaction, index) => (
                <tr key={index} style={{ borderBottom: '1px solid #dee2e6' }}>
                  <td style={{ padding: '10px' }}>{transaction.date}</td>
                  <td style={{ padding: '10px' }}>{transaction.description}</td>
                  <td style={{ 
                    padding: '10px', 
                    textAlign: 'right',
                    color: transaction.amount < 0 ? '#dc3545' : '#28a745',
                    fontWeight: 'bold'
                  }}>
                    {formatAmount(transaction.amount)}
                  </td>
                  <td style={{ padding: '10px' }}>{transaction.category}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default BankStatementUploader;