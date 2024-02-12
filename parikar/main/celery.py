from celery import Celery

app = Celery('parikar',
             broker = 'redis://127.0.0.1:6379/0',
             backend='rpc://',
             include=['parikar.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
