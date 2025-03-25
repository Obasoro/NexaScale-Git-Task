from message_app import celery, app

if __name__ == '__main__':
    # Start Celery worker
    celery.worker_main(
        argv=['worker', '--loglevel=info', '--concurrency=4']
    )