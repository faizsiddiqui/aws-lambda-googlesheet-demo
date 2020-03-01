#!/bin/bash

rm -f aws-*.zip
echo 'Building lambda function...'
zip -r aws-tag-fetch-lambda.zip . -x build.sh -x README.md -x ".*" -x "aws-*" -x LICENSE -x requirements.txt
