from fastapi import FastAPI, HTTPException
import boto3
import threading
import time
import os
from endpoints.nx_graph_path_finder import NxGraphPathFinder
from local_graph_loader import LocalGraphLoader
from s3_graph_loader import S3GraphLoader
from controller import Controller

app = FastAPI()

def get_boto3_client(service_name):
    """
    Configura el cliente de boto3 para conectar con LocalStack usando la IP correcta.
    """
    return boto3.client(
        service_name,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        endpoint_url=f"http://172.20.0.2:4566"
    )

def listen_sqs_messages(controller, queue_url):
    """
    Escucha mensajes de SQS y actualiza el grafo cuando llega un mensaje.
    """
    sqs = get_boto3_client("sqs")
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10
            )
            messages = response.get("Messages", [])
            for message in messages:
                print(f"Received SQS message: {message['Body']}")
                controller.reload_graph_for_webservice()

                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message["ReceiptHandle"]
                )
                print("Message processed and deleted.")
        except Exception as e:
            print(f"Error receiving SQS message: {e}")
        time.sleep(5)

def validate_graph_exists(bucket_name, file_key):
    """
    Valida que el archivo del grafo exista en el bucket de S3.
    """
    s3_client = get_boto3_client("s3")
    try:
        s3_client.head_object(Bucket=bucket_name, Key=file_key)
        print(f"Graph file '{file_key}' found in bucket '{bucket_name}'.")
    except s3_client.exceptions.NoSuchKey:
        raise FileNotFoundError(f"Graph file '{file_key}' not found in bucket '{bucket_name}'.")
    except Exception as e:
        raise RuntimeError(f"Error accessing S3: {e}")

@app.get("/health")
def health_check():
    """
    Endpoint de verificación de estado.
    """
    return {"status": "running"}

@app.post("/reload-graph")
def reload_graph():
    """
    Endpoint manual para recargar el grafo.
    """
    try:
        controller.reload_graph_for_webservice()
        return {"message": "Graph reloaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reloading graph: {str(e)}")

def main():
    """
    Función principal que inicia el controlador y escucha mensajes de SQS.
    """
    bucket_name = os.getenv("BUCKET_NAME", "graphword-bucket")
    file_key = os.getenv("FILE_KEY", "graphs/graph.pkl")
    queue_url = os.getenv("QUEUE_URL", "http://172.20.0.2:4566/000000000000/graph-update-queue")
    # Validar que el grafo existe
    validate_graph_exists(bucket_name, file_key)

    # Inicializar el cargador de grafo
    graph_loader = S3GraphLoader(s3_bucket=bucket_name)
    global controller
    controller = Controller(graph_loader=graph_loader, graph_filename=file_key)

    controller.execute()

    # Iniciar escucha de SQS en un hilo separado
    threading.Thread(target=listen_sqs_messages, args=(controller, queue_url), daemon=True).start()

    # Ejecutar FastAPI
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
