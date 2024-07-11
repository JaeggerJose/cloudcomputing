import subprocess
import os
import time
import random
import sys
def sleep_random_microseconds(min_microseconds, max_microseconds):
    # Convert microseconds to seconds
    min_seconds = min_microseconds / 1_000_000
    max_seconds = max_microseconds / 1_000_000
    
    # Generate a random sleep time in seconds
    random_sleep_time = random.uniform(min_seconds, max_seconds)
    
    # Sleep for the random duration
    time.sleep(random_sleep_time)

# Example usage: Sleep for a random time between 100 microseconds and 2000 microseconds


# using /share/input to for loop all the tasks
# check current task from /share/input/{task_id}/computing exists or not, if exists, donot run the task and 
def check_current_task():
    # get all the task's directory from /share/input/
    tasks = os.listdir('/share/input')
    print(tasks)
    # loop all the tasks
    for task in tasks:
        print(f'Checking task {task}')
        # check if the task is completed , computing or not
        if os.path.exists(f'/share/input/{task}/completed') or os.path.exists(f'/share/input/{task}/computing'):
            print(f'Task {task} is already completed or computing')
            continue
        else:
            print(f'Task {task} is not completed or computing')
            return task
        return None
# get the task id
def check_process_and_exit(process_name):
    # Run 'ps aux' to get a list of all running processes
    result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, text=True)

    # Check if the process_name is in the output
    if process_name in result.stdout:
        print(f"Process {process_name} is running.")
        sys.exit(0)  # Exit if the process is found
    else:
        print(f"Process {process_name} is not running.")
sleep_random_microseconds(100, 2000)

task_id = check_current_task()
check_process_and_exit("/usr/local/bin/svc")
if task_id is None:
    print('No task to run')
else:
    print(f'Running task {task_id}')
    model = ""
    wav = ""
    # from this task get info(input wav, model)
    with open(f'/share/input/{task_id}/info.txt', 'r') as f:
        info = f.read()
        # parse the info, split with space
        info = info.split(' ')
        wav = info[0]
        model = info[1].strip()
    if model == "" or wav == "":
        print(f'Invalid info in task {task_id}')
        exit(1)
    # try to get the model(.pth) and config(.json) from /share/model
    
    os.listdir('/share/model')
    # check if the model exists
    if not os.path.exists(f'/share/model/{model}'):
        print(f'Model {model} does not exist')
        exit(1)
    # get a .pth and a .json file in the model directory 
    model_path = ""
    config_path = ""
    for file in os.listdir(f'/share/model/{model}'):
        if file.endswith('.pth'):
            model_path = f'/share/model/{model}/{file}'
        if file.endswith('.json'):
            config_path = f'/share/model/{model}/{file}'
    # run the task
    # add a computing file to the task
    with open(f'/share/input/{task_id}/computing', 'w') as f:
        f.write('')
        f.close()
        os.chmod(f'/share/input/{task_id}/computing', 0o777)
    os.chown(f'/share/input/{task_id}/computing', 33, 33)
    # run the task
    # create a directory to store the output
    os.makedirs(f'/share/output/{task_id}', exist_ok=True)
    log = subprocess.run(['/usr/local/bin/svc', 'infer', '-m', model_path, '-c', config_path, '-o', f'/share/output/{task_id}/output.wav', f'/share/input/{task_id}/{wav}'])
    # change the output permission to 777
    os.chmod(f'/share/output/{task_id}/output.wav', 0o777)
    os.chmod(f'/share/output/{task_id}', 0o777)
    # remove the computing file and add a completed file
    with open(f'/share/input/{task_id}/completed', 'w') as f:
        f.write('')
        f.close()
        os.chmod(f'/share/input/{task_id}/completed', 0o777)
    os.chown(f'/share/input/{task_id}/completed', 33, 33) 
    os.remove(f'/share/input/{task_id}/computing')


