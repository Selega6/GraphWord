# GraphWord App
GraphWord is an application that allows users to find paths between words (currently supporting English words with lengths between 3 and 5 characters). This project is built on a distributed infrastructure simulated with LocalStack to mimic AWS resources.
## Deployment Instructions:
### Start LocalStack with Docker
Maintaining the container name is important. Run the following command:
- docker run --rm -it --name localstack-container -p 4566:4566 -p 4510-4559:4510-4559 -v /var/run/docker.sock:/var/run/docker.sock localstack/localstack
### Navigate to the terraform directory and initialize Terraform with tflcoal
- Initialize Terraform:
  tflocal init
- Generate the infrastructure plan:
  tflocal plan -var-file="envs/prod.tfvars"
- Apply the plan:
- tflocal apply -var-file="envs/prod.tfvars" -auto-approve

### Trigger the Workflow
To start the full process, including downloading and processing, run: 
- aws events put-events --entries file://event.json --endpoint-url http://localhost:4566

To clean up and destroy the infrastructure, run:
- tflocal destroy -var-file="envs/prod.tfvars" -auto-approve

### Important Notes
Since the project uses the LocalStack Community Docker image, a simulated EC2 instance was created. This EC2 instance is currently designed to run on Windows.

### Documentation
For more information, refer to the documentation located in the /docs folder.
