#!/bin/bash

echo 'Are you enjoying this course so far?'
echo "Enter \"y\" for yes, \"n\" for no: "

read response

if [ "$response" = "y" ]
then 
    echo "I am enjoying too"

elif [ "$response" = "n" ]
then    
    echo "Sad to hear!"

else
    echo "Answer is not defined"

fi