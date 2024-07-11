!/bin/bash

# for loop to run the command "docker run -d lms025187/app_mining" 10 times
for i in {1..10}
do
  docker run -d lms025187/app_mining
done

