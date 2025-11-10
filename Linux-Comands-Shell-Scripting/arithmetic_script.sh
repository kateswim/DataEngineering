#!/bin/bash

echo -n "Please enter two integers "

echo -n "first one\: "
read integer1

echo -n "second one\: "
read integer2

sum=$(($integer1+$integer2))
product=$(($integer1*$integer2))


echo "The sum is $sum"
echo "The product is $product"

if [ $sum -lt $product ]
then
   echo "The sum is less than the product."
elif [ $sum -eq $product ]
then
   echo "The sum is equal to the product."
elif [ $sum -gt $product ]
then
   echo "The sum is greater than the product."
fi