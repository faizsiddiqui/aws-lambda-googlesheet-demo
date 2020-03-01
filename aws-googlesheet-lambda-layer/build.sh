# Download required packages
echo 'Building googlesheet lambda python layer...'
cd "$(dirname $0)" || exit
rm -vf aws-*.zip
mkdir -p aws-googlesheet-lambda-layer/python
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib -t aws-googlesheet-lambda-layer/python

# Removing unnecessary directories from the artifact
find "$(pwd)" \( -name '*.dist-info' -o -name '*__pycache__' \) -prune -exec rm -rf {} +

# Create lambda layer zip
cd aws-googlesheet-lambda-layer || exit
zip -r ../aws-googlesheet-lambda-layer.zip python

# Remove the installed python packages directory
rm -rf ../aws-googlesheet-lambda-layer/
