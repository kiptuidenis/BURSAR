from celery.schedules import crontab

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
timezone = 'Africa/Nairobi'

beat_schedule = {
    'process-daily-transfers': {
        'task': 'app.tasks.scheduled_tasks.process_daily_transfers',
        'schedule': crontab(minute='*/15'),  # Run every 15 minutes
    },
    'check-pending-transactions': {
        'task': 'app.tasks.scheduled_tasks.check_pending_transactions',
        'schedule': crontab(minute='*/5'),  # Run every 5 minutes
    }
}