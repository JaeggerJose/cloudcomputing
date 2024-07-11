# monitoring all job, with status(pending, computing, and completed), and name of the job at /share/input
import os

job_status = {}
def check_current_tasks():
    tasks = os.listdir('/share/input')
    print(tasks)
    for task in tasks:
        if os.path.exists(f'/share/input/{task}/completed'):
            job_status.update({task: 'completed'})
        elif os.path.exists(f'/share/input/{task}/computing'):
            job_status.update({task: 'computing'})
        else:
            job_status.update({task: 'pending'})
    return job_status

# write the job status to /share/job.txt
def write_job_status(job_status):
    # revmove the file if exists
    if os.path.exists('/share/job.txt'):
        os.remove('/share/job.txt')
    with open('/share/job.txt', 'w') as f:
        for job in job_status:
            f.write(f'{job} {job_status[job]}\n')
        f.close()
    os.chmod(f'/share/job.txt', 0o777)
        
job_status = check_current_tasks()
write_job_status(job_status)
print(job_status)

            
        
    
