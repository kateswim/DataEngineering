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