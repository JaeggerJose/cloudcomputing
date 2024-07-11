#!/bin/bash

# Loop from 1 to 10
for i in {1..99}
do
  # Execute the command with the current value of i
  ./app_transaction angel "b08290${i}" $i
done
