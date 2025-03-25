from celery import Celery

def create_celery(app=None):
    celery = Celery(
        __name__,
        broker='amqp://localhost//',
        backend='rpc://',
        include=['tasks']
    )
    
    if app:
        celery.conf.update(app.config)
    
    return celery

celery = create_celery()