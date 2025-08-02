# Railway Setup Instructions

Since this is a monorepo with both backend and frontend, you need to create TWO separate services in Railway:

## Step 1: Create Backend Service

1. In Railway dashboard, click **"New Service"**
2. Select **"Deploy from GitHub repo"**
3. Choose `rabeehzaman/bank-statement-parser`
4. **IMPORTANT**: Set the following in Settings:
   - **Root Directory**: `/backend`
   - **Start Command**: Leave empty (will use Procfile)
5. Deploy - Railway will auto-detect Python and use the Procfile

## Step 2: Create Frontend Service

1. Click **"New Service"** again
2. Select **"Deploy from GitHub repo"** 
3. Choose the same repo: `rabeehzaman/bank-statement-parser`
4. **IMPORTANT**: Set the following in Settings:
   - **Root Directory**: `/frontend`
   - **Build Command**: `npm install && npm install -g serve && npm run build`
   - **Start Command**: `serve -s build -l $PORT`
5. Add environment variable:
   - Click on **Variables** tab
   - Add: `REACT_APP_API_URL` = `https://[your-backend-service].railway.app`
   - Replace `[your-backend-service]` with your actual backend service URL
6. Deploy

## Alternative: Use Dockerfile

If the above doesn't work, I can create Dockerfiles for each service which Railway will automatically detect and use.

## Troubleshooting

- Make sure Root Directory is set correctly for each service
- Backend should auto-detect as Python and use Procfile
- Frontend needs the build and start commands specified
- Don't forget to set `REACT_APP_API_URL` in frontend service