# get CPU and memory usage from 3 docker containers

import docker
import time

# cmpNode3 cmpNode2 cmpNode1

client = docker.from_env()
container1 = client.containers.get('cmpNode1')
container2 = client.containers.get('cmpNode2')
container3 = client.containers.get('cmpNode3')

with open('resource.txt', 'w') as f:
    cpu1 = container1.stats(stream=False)['cpu_stats']['cpu_usage']['total_usage']
    cpu2 = container2.stats(stream=False)['cpu_stats']['cpu_usage']['total_usage']
    cpu3 = container3.stats(stream=False)['cpu_stats']['cpu_usage']['total_usage']

    mem1 = container1.stats(stream=False)['memory_stats']['usage']
    mem2 = container2.stats(stream=False)['memory_stats']['usage']
    mem3 = container3.stats(stream=False)['memory_stats']['usage']

    f.write(f'cmpNode1: CPU: {cpu1}, Memory: {mem1}\n')
    f.write(f'cmpNode2: CPU: {cpu2}, Memory: {mem2}\n')
    f.write(f'cmpNode3: CPU: {cpu3}, Memory: {mem3}\n\n')

    
    # break after 10 seconds
    f.close()
    os.chmod(f'resource.txt',  0o777)    
