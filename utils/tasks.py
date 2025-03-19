from celery_main import celery_app


class BackGroundTask:

    def __init__(self, celery_task: str, *args, **kwargs):
        self.task = celery_task
        self.args = args
        self.kwargs = kwargs

    def publish(self):
        celery_app.send_task(f'tasks.{self.task}', self.args, self.kwargs)
