import threading
import time
from functools import wraps
import pprint
import json
# Capture program start time
start_time = time.perf_counter()

thread_pool = list()                  # container to hold threads
total_delay = 0
thread_time_map = dict()
duration_from_decorator = 0


# container with random int (5, 20)
delay_index = [8, 15, 18, 12, 19, 7, 14, 8, 16, 16]


def thread_time_decorator(thread):
    @wraps(thread)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        thread(*args, **kwargs)
        end = time.perf_counter()
        threading.current_thread().thread_duration = end - start
    return wrapper


def worker(delay: int) -> None:
    # Do something
    time.sleep(delay)  # int -> emulates time for random tasks
    print(f"Worker_{delay} took {delay} secs to complete")


for i in range(len(delay_index)):
    _delay = delay_index[i]
    total_delay += _delay
    wrapped_worker = thread_time_decorator(worker)
    t = threading.Thread(target=wrapped_worker, args=(_delay,), name=f'Worker_{_delay}')
    thread_pool.append(t)

for _thread in thread_pool:
    _thread.start()
    print(f'--- Started {_thread.name}')

for _thread in thread_pool:
    _thread.join()
    print(f'--- Completed {_thread.name}')
    print(f'{_thread.name} took {_thread.thread_duration} secs ')
    duration_from_decorator += _thread.thread_duration
    thread_time_map[_thread.name] = _thread.thread_duration
thread_time_map['Total sum'] = sum(thread_time_map.values())
thread_time_map['Total No of threads'] = len(thread_pool)
thread_time_map['Average thread time'] = thread_time_map['Total No of threads'] / len(thread_pool)
# dump stats to file
with open('/tmp/program_stats.json', 'w') as file_obj:
    time.sleep(4)
    json.dump(thread_time_map, file_obj, indent=4)
# Capture program end time
end_time = time.perf_counter()
execution_time = end_time - start_time


print(f'Total execution time: {execution_time} secs')
print(f'Total no of threads: {len(thread_pool)}')
print(f'Average time: {execution_time / len(thread_pool)}')
print(f'Decorated Threads total duration: {duration_from_decorator}')
print(f'Decorated Average: {duration_from_decorator / len(thread_pool)}')
pprint.pprint(thread_time_map)