terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.23.0"
    }
  }
}

provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}

resource "docker_network" "localstack_network" {
  name = "localstack-network"
  ipam_config {
    subnet = "172.20.0.0/16"
  }
}


resource "docker_image" "ec2_simulator" {
  name = "ubuntu:latest"
}

resource "docker_container" "simulated_ec2" {
  name  = "simulated-ec2"
  image = docker_image.ec2_simulator.name

  command = ["sh", "-c", "apt-get update && apt-get install -y python3-pip python3-venv curl unzip && python3 -m venv /home/ubuntu/venv && . /home/ubuntu/venv/bin/activate && curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o 'awscliv2.zip' && unzip awscliv2.zip && ./aws/install && export PATH=$PATH:/usr/local/bin && aws --version && aws --endpoint-url=http://172.20.0.2:4566 s3 ls && aws --endpoint-url=http://172.20.0.2:4566 s3 cp s3://graphword-bucket/api_code.zip /home/ubuntu/api_code.zip && unzip /home/ubuntu/api_code.zip -d /home/ubuntu/api_code && /home/ubuntu/venv/bin/pip install -r /home/ubuntu/api_code/requirements.txt && python3 /home/ubuntu/api_code/main.py && tail -f /dev/null"]


  env = [
    "QUEUE_URL=${var.graph_update_queue_url}",
    "AWS_ACCESS_KEY_ID=test",
    "AWS_SECRET_ACCESS_KEY=test",
    "AWS_DEFAULT_REGION=us-east-1",
    "BUCKET_NAME=${var.bucket_name}",
    "S3_ENDPOINT=http://172.20.0.2:4566",
    "FILE_KEY=graphs/graph.pkl"
  ]

  networks_advanced {
    name         = docker_network.localstack_network.name
    ipv4_address = "172.20.0.10"
  }

ports {
  internal = 8000
  external = 8000
}
}

resource "null_resource" "connect_localstack_network" {
  provisioner "local-exec" {
    command = <<EOT
      docker network connect localstack-network localstack-container || echo "LocalStack ya está conectado."
    EOT
  }

  depends_on = [docker_network.localstack_network]
}

resource "null_resource" "connect_ec2_network" {
  provisioner "local-exec" {
    command = "docker network connect localstack-network simulated-ec2 || echo 'EC2 ya está conectada.'"
  }

  depends_on = [docker_container.simulated_ec2]
}