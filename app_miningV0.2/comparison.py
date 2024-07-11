
# open 1.txt and print to 100.txt
import datetime

start_time = datetime.datetime.now()
for i in range(100):
    with open('1.txt', 'r') as f:
        with open('100.txt', 'a') as f2:
            f2.write(f.read())
            
# calculate the time
print(datetime.datetime.now() - start_time)