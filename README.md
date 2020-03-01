# aws-lambda-googlesheet-demo

### Configuration


#### Google authentication

1. [Open Google Developer Console](https://console.developers.google.com/)

2. Select/Create a Project

3. Enable Google Sheet API

4. Create credential + server account

5. Download service account credential file in JSON format and update `server_account.json`

6. Copy `client_email` from credential and share google sheet with this email


#### Setup Lambda Function

7. Run build script, following will be output --

    a. `aws-googlesheet-lambda-layer.zip` - Lambda Layer for googlesheet package

    b. `aws-tag-fetch-lambda.zip` - Lambda function

    ```bash
pip install -r requirements.txt
bash aws-googlesheet-lambda-layer/build.sh
bash build.sh
    ```

8. [Create Lambda function](https://console.aws.amazon.com/lambda/home)

9. Upload Layer (`aws-googlesheet-lambda-layer.zip`) [ Runtime => Python 3.x ]

10. Create Lambda function - `aws-tag-fetch-lambda`

    a. IAM Role policy access requirement - [aws-policy.json](aws-policy.json)

    b. Environment Variables -

      ```bash
SHEET_ID
SHEET_NAME
SHEET_RANGE
CUSTOM_TAGS
      ```

    c. Resource requirement -
       - Memory = 256 MB
       - Timeout = 30 sec
