**Blog/Book Audio Converter using AWS Polly!**
I’ve been working on a project that converts text-based content (like blogs, articles, and books) into speech using AWS Polly. This tool makes written content more accessible, especially for users who prefer audio over text.

**Key Features:**
Converts text files to audio for easier consumption.
Ideal for content accessibility, learning, and engagement.
Perfect for multitasking, whether commuting or working out.

## Use Cases:
- **Content Accessibility**: Audio versions of written content for visually impaired users.
- **Learning**: Enabling users to listen to educational materials.
- **Content Distribution**: Offers a new medium for content consumption.
- **Convenience**: Allows users to listen while performing other tasks.

## Architecture

This project leverages the following AWS services:
- **Amazon S3**: To store the source text files and output audio files.
- **AWS Lambda**: To trigger the conversion process.
- **AWS Polly**: To synthesize speech from text.

## Prerequisites

- **AWS Account**: Create an AWS account at [AWS Console](https://aws.amazon.com/).
- **IAM Permissions**: Ensure you have the appropriate IAM permissions to access S3 and Polly services.
- **AWS CLI**: Optionally, set up the AWS CLI for managing resources from the terminal.

## Steps to Build

1. Create Two S3 Buckets
Create two S3 buckets:
- **Source Bucket** (`amc-polly-source-bucket`): To store the input `.txt` files.
- **Destination Bucket** (`amc-polly-destination-bucket`): To store the output audio files.

2. Create an IAM Policy

Create an IAM policy (`amc-polly-lambda-policy`) with the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::amc-polly-source-bucket/*",
        "arn:aws:s3:::amc-polly-destination-bucket/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "polly:SynthesizeSpeech"
      ],
      "Resource": "*"
    }
  ]
}

3. Create and Configure Lambda Function
Runtime: Python 3.8
Execution Role: Use the IAM role created in
Environment Variables:
SOURCE_BUCKET: Name of your source S3 bucket.
DESTINATION_BUCKET: Name of your destination S3 bucket.

4. Set Up S3 Event Notification
Configure an event notification on the source S3 bucket to trigger the Lambda function when new .txt files are uploaded.

5. Write Lambda Function Code
Write the Lambda function to:

Retrieve the uploaded .txt file from the source bucket.
Use AWS Polly to convert the text to speech.
Save the resulting audio file to the destination S3 bucket.

6. Test the System
Upload a sample .txt file to the source bucket and verify that the Lambda function triggers correctly and stores the audio output in the destination bucket
