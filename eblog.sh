#!/usr/bin/env bash

# E2 인스턴스에서 실행 중인 도커 컨테이너 속 장고 로그파일 가져오기

# using your profile name
EB_ENV=$(eb list --profile fc-8th-eb)  # Add your profile name

# get docker container id
EB_DOCKER_ID=$(eb ssh ${EB_ENV##* } --command "sudo docker ps -q")

# django error dir
EB_ERRORS_DIR=/var/log/django/

# copy log file from docker container
eb ssh ${EB_ENV##* } -c "sudo docker cp ${EB_DOCKER_ID:0:4}:/var/log/django/error.log ."

# get log file from EC2 instance
mkdir ./.log
scp -i ~/.ssh/fc-8th.pem -r ec2-user@52.79.144.201:/home/ec2-user/error.log ./.log/error.log

# delete log file in EC2
eb ssh ${EB_ENV##* } -c "rm -rf error.log"

# display log file
tail -10 ./.log/error.log