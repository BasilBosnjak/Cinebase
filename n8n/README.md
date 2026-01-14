# n8n Deployment on Render

This directory contains files for deploying n8n to Render.

## Deployment Steps

### 1. Create New Web Service on Render

1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Use these settings:
   - **Name**: `cinebase-n8n` (or your choice)
   - **Region**: Same as your backend (for lower latency)
   - **Branch**: `main`
   - **Root Directory**: `n8n`
   - **Runtime**: Docker
   - **Instance Type**: Free

### 2. Set Environment Variables

In Render dashboard, add these environment variables:

**Required:**
- `N8N_ENCRYPTION_KEY`: Generate with: `openssl rand -hex 32`
- `COHERE_API_KEY`: Your Cohere API key (same as backend)
- `DATABASE_URL`: Your PostgreSQL connection string (same as backend)

**Optional (for persistence):**
- `N8N_BASIC_AUTH_ACTIVE`: `true` (recommended for security)
- `N8N_BASIC_AUTH_USER`: Your username
- `N8N_BASIC_AUTH_PASSWORD`: Your password

**Important:**
- `WEBHOOK_URL`: Will be `https://your-n8n-instance.onrender.com/` (update after deployment)

### 3. Deploy

1. Click "Create Web Service"
2. Wait for deployment to complete (~5 minutes)
3. Note your n8n URL: `https://cinebase-n8n.onrender.com`
4. Update `WEBHOOK_URL` environment variable with your actual URL

### 4. Access n8n

1. Go to your n8n URL
2. Create your first workflow
3. If you enabled basic auth, enter credentials

## Render Free Tier Limitations

- **Sleep after 15 min inactivity**: n8n will sleep when not in use
- **Spin-up time**: ~30 seconds to wake up when webhook is triggered
- **750 hours/month**: Should be sufficient for this use case

## Next Steps

After deployment:
1. Import the embedding workflow (see `workflow.json`)
2. Configure webhook URL in backend
3. Test by uploading a PDF
