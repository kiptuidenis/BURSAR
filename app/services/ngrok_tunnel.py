"""
Optional ngrok tunnel service for development environments
Helps expose local server for M-Pesa callbacks
"""
import requests
import json
from flask import current_app

def get_public_url():
    """
    Get the public URL from ngrok for callbacks
    Only use in development environment
    """
    try:
        # Check if ngrok is running locally (default port 4040)
        response = requests.get("http://localhost:4040/api/tunnels")
        data = response.json()
        
        # Extract the public HTTPS URL
        for tunnel in data["tunnels"]:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
        
        current_app.logger.warning("No HTTPS ngrok tunnel found")
        return None
    except Exception as e:
        current_app.logger.warning(f"Could not get ngrok URL: {str(e)}")
        return None
