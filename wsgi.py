from run import app

# For WSGI servers like Gunicorn
if __name__ == "__main__":
    app.run()