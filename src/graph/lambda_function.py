import os
import json
import boto3
from botocore.exceptions import ClientError
from controller import Controller
from data_loader import DataLoader
from nx_graph_builder import NxGraphBuilder
from s3_graph_uploader import S3GraphUploader

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    sqs_client = boto3.client('sqs')  
    
    queue_url = os.getenv("SEND_QUEUE_URL")
    
    try:
        print(f"Received event: {json.dumps(event)}")

        if 'Records' not in event or not event['Records']:
            return {
                'statusCode': 400,
                'body': json.dumps("Error: No records found in the event.")
            }

        for record in event['Records']:
            if 'body' in record:
                message_body = json.loads(record['body'])
            else:
                message_body = record

            output_file = message_body.get('output_file', 'processed/word_counts.txt')

            s3_bucket = os.getenv("BUCKET_NAME", "graphword-bucket").rstrip("/")
            word_counts_key = output_file.lstrip("/")
            s3_key = os.getenv("OUTPUT_FILE", "graphs/graph.pkl").lstrip("/")

            local_word_counts_path = f"/tmp/{os.path.basename(word_counts_key)}"
            s3_client.download_file(s3_bucket, word_counts_key, local_word_counts_path)

            data_loader = DataLoader(local_word_counts_path, s3_bucket, s3_key)
            graph_builder = NxGraphBuilder(data_loader=data_loader)
            graph_uploader = S3GraphUploader(
                bucket_name=s3_bucket,
                region_name="us-east-1",
                folder_name="graphs",
                graph_file="graph.pkl",
                graph=None
            )

            controller = Controller(data_loader, graph_builder, graph_uploader)
            existing_graph = "graph.pkl"
            new_graph = "graph.pkl"
            controller.execute(existing_graph, new_graph)

        sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({
                'status': 'completed',
                'message': 'graph generated successfully.',
                's3_bucket': s3_bucket,
                's3_key': s3_key
            })
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Graph generated and uploaded to S3 successfully.')
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Client error S3/SQS: {e}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'General error: {e}')
        }
