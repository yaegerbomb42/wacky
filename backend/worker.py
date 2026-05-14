from rq import Worker
from app.worker.queue import redis_conn

if __name__ == "__main__":
    w = Worker(["tasks"], connection=redis_conn)
    w.work()
