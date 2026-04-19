# Facebook Login Automation Backend

Complete backend for the Facebook Login Automation system.

## Project Structure

```
backend_project/
├── api/                    # Vercel serverless functions
│   ├── _common.py         # Shared utilities (MongoDB, auth, etc.)
│   ├── index.py           # Root endpoint
│   ├── health.py          # MongoDB health check
│   ├── login.py           # User login/authentication
│   ├── users.py           # User management (CRUD)
│   ├── record.py          # Login records
│   └── renew.py           # Subscription renewal
├── .env                    # Environment variables (MONGO_URI, credentials)
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel deployment config
└── README.md              # This file
```

## Local Development

### 1. Install dependencies

```powershell
pip install -r requirements.txt
```

### 2. Set up environment

The `.env` file is already configured with MongoDB Atlas URI.

### 3. Test locally with Vercel CLI

```powershell
pip install vercel
vercel dev
```

API will be available at `http://localhost:3000/api/*`

### 4. Test endpoints

```bash
# Health check
curl http://localhost:3000/api/health

# See all endpoints
curl http://localhost:3000/
```

## Deployment to Vercel

### 1. Create a GitHub repo for this folder

```powershell
cd backend_project
git init
git add .
git commit -m "Initial backend setup"
git remote add origin https://github.com/yourusername/fb-automation-backend
git push -u origin main
```

### 2. Deploy to Vercel

- Go to https://vercel.com
- Click "New Project"
- Import the GitHub repo
- Add Environment Variables (from `.env` file):
  - `MONGO_URI`
  - `MONGO_DB`
  - `ADMIN_EMAIL`
  - `ADMIN_PASSWORD`
- Deploy

Your backend will be live at `https://your-project.vercel.app/`

## API Endpoints

| Method | Endpoint      | Description                     |
| ------ | ------------- | ------------------------------- |
| GET    | `/api/health` | Check MongoDB connection        |
| POST   | `/api/login`  | Authenticate user               |
| GET    | `/api/users`  | List all users                  |
| POST   | `/api/users`  | Create new user (admin only)    |
| POST   | `/api/record` | Record login attempt            |
| POST   | `/api/renew`  | Renew subscription (admin only) |

## Notes

- This backend is completely separate and self-contained
- The desktop GUI (script.py) and backend are independent
- Deploy this folder to Vercel for production
- Keep `.env` secure - never commit credentials to git
