# Vercel Deployment Guide for BURSAR

## Fixed Issues

1. **Removed JSON Comments**: We've removed all comments from JSON files that were causing parsing errors:
   - package.json
   - vercel.json
   - now.json

2. **Simplified Configuration**: We've consolidated the deployment configuration:
   - Removed conflicting files like `now.json` and `vercel.config`
   - Created a single `vercel.json` with all necessary configuration
   - Updated package.json to be minimal and without any errors

3. **Improved Error Handling**: Added better error handling in:
   - API handler (api/index.py)
   - Static file collection scripts
   - Database initialization code

4. **Session Management**: Properly configured sessions for both:
   - Local development environment
   - Vercel serverless environment

## Deployment Process

1. Make sure your code is committed to your Git repository

2. Connect your repository to Vercel:
   - Create a new project on Vercel
   - Link your Git repository
   - Select the BURSAR repository/directory

3. Configure the deployment:
   - Framework Preset: Other
   - Build Command: Leave as default
   - Output Directory: Leave as default
   - Install Command: Leave as default

4. Set environment variables (if needed):
   - Add any sensitive variables like API keys, etc.

5. Deploy!

## Troubleshooting

If you encounter issues:

1. Check the Vercel build logs for specific errors
2. Make sure your Python version is correct (3.9)
3. Verify all dependencies in requirements.txt are compatible with Vercel
4. Check if any files have comments that should be removed

## Local Testing

To test locally before deploying:

```bash
python run_local.py
```

This will run your application with the same configuration as the development environment.

## Vercel Limitations

Be aware of Vercel's serverless limitations:
- In-memory SQLite database is recreated for each request
- Session data is stored in /tmp but may not persist between requests
- File system operations are limited

For a more robust production environment, consider:
- Using a proper database service like PostgreSQL
- Implementing a Redis or other external session store
- Deploying to a traditional hosting platform
