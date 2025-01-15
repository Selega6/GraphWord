resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda-exec-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy_attachment" "lambda_basic_execution" {
  name       = "lambda-basic-execution"
  roles      = [aws_iam_role.lambda_exec_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "lambda_crawler_sqs_policy" {
  name        = "LambdaCrawlerSQSPolicy"
  description = "Enables Lambda to send messages to the crawler-to-graph queue"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = "sqs:SendMessage",
        Effect   = "Allow",
        Resource = var.graph_queue_arn
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_graph_sqs_policy" {
  name        = "LambdaGraphSQSPolicy"
  description = "Enables Lambda to send messages to the graph-update queue"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = "sqs:SendMessage",
        Effect   = "Allow",
        Resource = var.graph_update_queue_arn
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "crawler_lambda_sqs_access" {
  name       = "crawler-lambda-sqs-access"
  roles      = [aws_iam_role.lambda_exec_role.name]
  policy_arn = aws_iam_policy.lambda_crawler_sqs_policy.arn
}

resource "aws_iam_policy_attachment" "graph_lambda_sqs_access" {
  name       = "graph-lambda-sqs-access"
  roles      = [aws_iam_role.lambda_exec_role.name]
  policy_arn = aws_iam_policy.lambda_graph_sqs_policy.arn
}

resource "aws_iam_policy_attachment" "lambda_s3_access" {
  name       = "lambda-s3-access"
  roles      = [aws_iam_role.lambda_exec_role.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_lambda_function" "crawler_lambda" {
  function_name = var.lambda_name
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "aws_lambda.lambda_handler"
  runtime       = "python3.9"
  filename      = var.lambda_package
  timeout       = 900
  environment {
    variables = {
      BUCKET_NAME     = var.bucket_name
      DOWNLOAD_FOLDER = var.download_folder
      OUTPUT_FILE     = var.output_file
      QUEUE_URL       = var.graph_queue_url
    }
  }
}

resource "aws_lambda_function" "graph_lambda" {
  function_name = var.lambda_name_for_graph
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  filename      = var.lambda_package_for_graph
  timeout       = 900
  environment {
    variables = {
      BUCKET_NAME     = var.bucket_name
      WORD_COUNTS_KEY = var.output_file
      OUTPUT_FILE     = var.output_file_for_graph
      QUEUE_URL       = var.graph_queue_url
      SEND_QUEUE_URL = var.graph_update_queue_url
    }
  }
}


resource "aws_lambda_event_source_mapping" "sqs_trigger_graph_lambda" {
  event_source_arn = var.graph_queue_arn 
  function_name    = aws_lambda_function.graph_lambda.arn     
  batch_size       = 1                                         
  enabled          = true                                      
}

resource "aws_lambda_permission" "allow_sqs_graph_lambda" {
  statement_id  = "AllowExecutionFromSQS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.graph_lambda.function_name
  principal     = "sqs.amazonaws.com"
  source_arn    = var.graph_queue_arn
}
