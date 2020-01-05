### High Level Steps


1. [Open Google Developer Console](https://console.developers.google.com/)

2. Select/Create a Project

3. Enable Google Sheet API

4. Create credential + server account

5. Download service account credential file in JSON format and update `server_account.json`

6. Copy `client_email` from credential and share google sheet with this email

7. Run build script, following will be output --

    a. `aws-googlesheet-lambda-layer.zip` - Lambda Layer for googlesheet package

    b. `aws-tag-fetch-lambda.zip` - Lambda function

```
./build.sh
```

8. [Create Lambda function](https://console.aws.amazon.com/lambda/home)

9. Upload Layer (`aws-googlesheet-lambda-layer.zip`) [ Runtime => Python 3.x ]

10. Create Lambda function - `aws-tag-fetch-lambda`

    a. IAM Role access requirement -

      - Service: CloudWatch Logs

        Limited: Write

        Resource: `arn:aws:logs:us-east-1:<aws-account-id>:log-group:/aws/lambda/aws-tag-fetch-lambda:*`

      - Service: EC2

        Limited: `Full: List, Read`

        Resource: `All resources`

    b. Environment Variables -

      ```
      SHEET_ID
      SHEET_NAME
      SHEET_RANGE
      CUSTOM_TAGS
      ```

    c. Resource requirement -
       - Memory = 256 MB
       - Timeout = 30 sec
