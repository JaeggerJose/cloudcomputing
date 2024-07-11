# for loop to run the command "docker run -d lms025187/app_mining" 10 times
for i in {1..300}
do
  ./app_transaction b0929054 angel3 3bc5848f77e347dccad85c5f24f85c366698661bbb32c9783c8b 0.001
  sleep 1
done

