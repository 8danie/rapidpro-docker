#!/bin/bash

awslocal s3 mb s3://temba-default
awslocal s3 mb s3://temba-attachments
awslocal s3api put-bucket-acl --bucket temba-attachments --acl public-read
awslocal s3 mb s3://temba-sessions
awslocal s3 mb s3://temba-logs
awslocal s3 mb s3://temba-archives
