import boto3
import json
import os
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Initialize S3 and Polly clients
    s3 = boto3.client('s3')
    polly = boto3.client('polly')

    # Get the bucket names from environment variables
    source_bucket = os.environ.get('SOURCE_BUCKET', '')
    destination_bucket = os.environ.get('DESTINATION_BUCKET', '')

    text_file_key = None  # Initialize the variable to avoid UnboundLocalError

    try:
        # Validate event structure
        if 'Records' not in event or not event['Records']:
            raise ValueError("Invalid event structure: 'Records' key missing or empty.")

        text_file_key = event['Records'][0]['s3']['object']['key']
        audio_key = text_file_key.replace('.txt', '.mp3')

        logger.info(f"Retrieving text file from bucket: {source_bucket}, key: {text_file_key}")
        text_file = s3.get_object(Bucket=source_bucket, Key=text_file_key)
        text = text_file['Body'].read().decode('utf-8')

        # Send text to Polly
        logger.info(f"Sending text to Polly for synthesis")
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Joanna'
        )

        # Save the audio file to the destination S3 bucket
        if 'AudioStream' in response:
            temp_audio_path = '/tmp/audio.mp3'
            with open(temp_audio_path, 'wb') as file:
                file.write(response['AudioStream'].read())

            logger.info(f"Uploading audio file to bucket: {destination_bucket}, key: {audio_key}")
            s3.upload_file(temp_audio_path, destination_bucket, audio_key)

        logger.info(f"Text-to-Speech conversion completed successfully for file: {text_file_key}")

        return {
            'statusCode': 200,
            'body': json.dumps('Text-to-Speech conversion completed successfully!')
        }

    except Exception as e:
        error_msg = f"Error processing file {text_file_key if text_file_key else '[UNKNOWN]'} from bucket {source_bucket}: {str(e)}"
        logger.error(error_msg)
        return {
            'statusCode': 500,
            'body': json.dumps(error_msg)
        }
