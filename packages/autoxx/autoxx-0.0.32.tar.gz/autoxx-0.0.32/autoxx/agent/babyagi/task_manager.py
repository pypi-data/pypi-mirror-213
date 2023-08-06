import threading
import queue
from uuid import uuid4
from typing import List, Dict, Optional
from autoxx.agent.babyagi.agi import AGIExecutor
  
class TaskManager:  
    def __init__(self, max_queue_length: int = 3):
        self.tasks = {}
        self.task_queue = queue.Queue(maxsize=max_queue_length)
        self.max_queue_length = max_queue_length
        self.processing_thread = None
  
    def create_task(self, objective: str, max_tasks_count: Optional[int] = 3):
        if self.task_queue.full():
            raise ValueError("Task queue is full. Please try again later.")

        # check whether objective already in tasks
        for task_id, task_info in self.tasks.items():
            if task_info.objective == objective:
               return task_id

        new_task_id = str(uuid4())
        cancel_event = threading.Event()
        new_task = AGIExecutor(objective, max_tasks_count, cancel_event)
        self.tasks[new_task_id] = new_task

        self.task_queue.put(new_task_id)
        if self.processing_thread is None or not self.processing_thread.is_alive():
            self.processing_thread = threading.Thread(target=self.process_task_queue)
            self.processing_thread.start()

        return new_task_id

    def process_task_queue(self):
        while not self.task_queue.empty():
            task_id = self.task_queue.get()
            task_info = self.tasks[task_id]
            task_thread = threading.Thread(target=task_info.execute)
            task_thread.start()
            task_thread.join()  # wait for the task to complete
            self.task_queue.task_done()

    def resume_task(self, task_id: str):
        if task_id not in self.tasks:
            raise ValueError(f"No task found with id: {task_id}")
        
        task_info = self.tasks[task_id]

        if task_info.status in ('error', 'cancelled') and task_id not in self.task_queue.queue:
            print(f"Resume task {task_id}")
            task_info.cancel_event.clear()
            self.task_queue.put(task_id)
            if self.processing_thread is None or not self.processing_thread.is_alive():
                self.processing_thread = threading.Thread(target=self.process_task_queue)
                self.processing_thread.start()
        else:
            raise ValueError(f"Cannot resume task {task_id} with status {task_info.status} or in queue {task_id in self.task_queue.queue}")

    def cancel_task(self, task_id: str):
        if task_id not in self.tasks:
            raise ValueError(f"No task found with id: {task_id}")

        task_info = self.tasks[task_id]
        if task_info.status == 'running':
            print(f"Cancel task {task_id}")
            task_info.cancel_event.set()
        elif task_info.status == 'pending':
            # Remove task from queue
            print(f"Remove task {task_id} from queue")
            with self.task_queue.mutex:
                self.task_queue.queue.remove(task_id)
                del self.tasks[task_id]
        else:
            raise ValueError(f"Cannot cancel task {task_id} with status {task_info.status}")

    def get_task_stat(self, task_id: str) -> Dict:
        if task_id not in self.tasks:
            raise ValueError(f"No task found with id: {task_id}")
  
        return self.tasks[task_id].stat()

    def get_task_list(self) -> List:
        # Return a list of tasks [{task_id,objectivbe,status}, ...]
        task_list = []
        for task_id, task_info in self.tasks.items():
            task_list.append({'id': task_id, 'objective': task_info.objective, 'status': task_info.status})
        return task_list