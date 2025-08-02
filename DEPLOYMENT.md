# Deployment Guide

## GitHub Setup

1. Create a new repository on GitHub
2. Add the remote origin:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/bank-statement-parser.git
   git branch -M main
   git push -u origin main
   ```

## Railway Deployment

### Method 1: Deploy from GitHub (Recommended)

1. Go to [Railway](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will detect the monorepo structure and create two services
5. Configure environment variables:
   - For the backend service, Railway will auto-set `PORT`
   - For the frontend service, update `REACT_APP_API_URL` to point to your backend URL

### Method 2: Manual Setup

1. Create two services in Railway:
   - Backend service
   - Frontend service

2. For Backend:
   - Connect to GitHub repo
   - Set root directory to `/backend`
   - Railway will auto-detect Python and use Procfile
   - No environment variables needed (PORT is auto-set)

3. For Frontend:
   - Connect to GitHub repo
   - Set root directory to `/frontend`
   - Add environment variable:
     ```
     REACT_APP_API_URL=https://your-backend-service.railway.app
     ```
   - Set build command: `npm install && npm run build`
   - Set start command: `npx serve -s build`

### Post-Deployment

1. Update frontend's `.env.production` with actual backend URL
2. Commit and push the change
3. Railway will auto-deploy

## Testing the Deployment

1. Access your frontend URL
2. Upload a sample Excel bank statement
3. Verify transactions are parsed and displayed correctly

## Troubleshooting

### Backend Issues
- Check logs: `railway logs`
- Verify Python version in runtime.txt
- Ensure all dependencies are in requirements.txt

### Frontend Issues
- Verify REACT_APP_API_URL is set correctly
- Check browser console for CORS errors
- Ensure backend URL doesn't have trailing slash

### CORS Issues
- Backend is configured to accept all origins (`*`)
- For production, update to specific domains

## Local Development

Start both servers:
```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm install
npm start
```