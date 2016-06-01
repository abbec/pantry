from pantry import create_celery

celery = create_celery('pantry.cfg')


@celery.task()
def assign_targets():
    return None
