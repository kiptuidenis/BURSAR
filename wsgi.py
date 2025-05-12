from app import create_app

# Create app instance
app = create_app()

# For WSGI servers
if __name__ == "__main__":
    app.run()