#!/bin/bash

CUR_PWD=$(pwd)

# Build docker image for table generator
cd ./1_tableGenerator
./build_image.sh
cd $CUR_PWD


# Build docker image for matrix multiplication
cd ./2_matrixMultiplication
./build_image.sh
cd $CUR_PWD