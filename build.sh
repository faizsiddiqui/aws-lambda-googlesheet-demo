#!/bin/bash

rm -f aws-*.zip
echo 'Building lambda function...'
zip -r aws-tag-fetch-lambda.zip . -x build.sh -x README.md -x ".*" -x "aws-*"

echo 'Building googlesheet lambda python layer...'
mkdir -p aws-googlesheet-lambda-layer/python
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib -t aws-googlesheet-lambda-layer/python
rm -r aws-googlesheet-lambda-layer/python/*.dist-info __pycache__
cd aws-googlesheet-lambda-layer && zip -r ../aws-googlesheet-lambda-layer.zip python && cd ../ && rm -rf aws-googlesheet-lambda-layer/
