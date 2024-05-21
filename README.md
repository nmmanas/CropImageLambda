# CropImageLambda
Crops images added to a source bucket in s3 and saves to a target bucket

## Trigger
Lambda is triggered when adding a new item to a s3 bucket (need to configure on aws s3)

## Deployment
Lambda can be deployed via github action. Currently its set to manual deployment but can be changed to deploy on `push`

## Variables
### Environment
Make sure to configure `TARGET_BUCKET_NAME` as environment variable on the lambda configuration
### Secrets
Add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in github repository secrets to be used when pushing the lambda code to aws
