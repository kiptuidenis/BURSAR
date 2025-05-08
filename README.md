# Bursar - Smart Financial Management App

Bursar is a Flask-based web application that helps users manage their daily spending through automated MPESA transfers and budget tracking. The application allows users to set monthly budgets, receive daily allocations, and track their spending patterns.

## Features

- **Automated Daily Transfers**: Receive your daily budget automatically through MPESA at your preferred time
- **Budget Categories**: Create and manage custom budget categories with daily allocation limits
- **Transaction Tracking**: Monitor all your transactions with detailed history
- **MPESA Integration**: Seamless integration with MPESA for automated payments
- **Two-Factor Authentication**: Optional SMS-based 2FA for enhanced security
- **Responsive Dashboard**: Real-time overview of your budget and spending

## Tech Stack

- **Backend**: Python/Flask
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Task Queue**: Celery with Redis
- **Frontend**: Bootstrap 5, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Database Migrations**: Flask-Migrate

## Prerequisites

- Python 3.10+
- Redis Server
- MPESA Developer Account
- Virtual Environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd finance_mvp_app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a .env file with the following variables:
```
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///instance/app.db
SECRET_KEY=your-secret-key-replace-in-production
MPESA_CONSUMER_KEY=your-mpesa-key
MPESA_CONSUMER_SECRET=your-mpesa-secret
BASE_URL=http://localhost:5000
```

5. Initialize the database:
```bash
flask db upgrade
```

## Running the Application

1. Start Redis Server:
```bash
redis-server
```

2. Start Celery worker:
```bash
celery -A app.tasks.scheduled_tasks worker --loglevel=info
```

3. Start Celery beat for scheduled tasks:
```bash
celery -A app.tasks.scheduled_tasks beat --loglevel=info
```

4. Run the Flask application:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Project Structure

```
finance_mvp_app/
├── app/
│   ├── routes/          # Route definitions
│   ├── models/          # Database models
│   ├── services/        # External service integrations
│   ├── tasks/           # Celery tasks
│   ├── templates/       # HTML templates
│   └── static/          # Static files (CSS, JS)
├── migrations/          # Database migrations
├── instance/           # Instance-specific files
├── requirements.txt    # Project dependencies
└── run.py             # Application entry point
```

## Key Components

- **User Management**: Complete authentication system with phone number-based registration
- **Budget Management**: Create and track budget categories with daily limits
- **MPESA Integration**: Automated B2C transfers for daily budget allocation
- **Transaction Tracking**: Complete history of all MPESA transfers
- **Scheduled Tasks**: Automated daily transfers and transaction status updates
- **Security Features**: Password hashing, CSRF protection, and optional 2FA

## Configuration

The application uses a configuration class in `app/config.py`. Key configurations include:

- Database settings
- MPESA API credentials
- Security settings
- Redis configuration for Celery

## Development

1. Make sure to run tests before submitting changes:
```bash
python -m pytest
```

2. Format code according to PEP 8:
```bash
black .
```

3. Check for linting errors:
```bash
flake8
```

## Security Features

- Password hashing using Werkzeug
- CSRF protection on all forms
- Optional two-factor authentication
- Secure session management
- Input validation and sanitization

## Production Deployment

For production deployment:

1. Use a production-grade server (e.g., Gunicorn)
2. Configure a proper database (PostgreSQL recommended)
3. Set up proper SSL/TLS certificates
4. Configure proper logging
5. Use environment variables for sensitive data
6. Set up proper monitoring and error tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the repository or contact the development team.