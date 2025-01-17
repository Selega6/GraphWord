module "s3" {
  source      = "./modules/s3"
  bucket_name = var.bucket_name
}

module "eventbridge" {
  source                 = "./modules/eventbridge"
  daily_trigger_expression = var.daily_trigger_expression
  manual_trigger_expression = var.manual_trigger_expression
  crawler_lambda_arn     = module.lambda.crawler_lambda_arn
}

module "sqs" {
  source = "./modules/sqs"
}

module "lambda" {
  source                  = "./modules/lambda"
  lambda_name             = var.lambda_name
  lambda_package          = var.lambda_package
  lambda_name_for_graph   = var.lambda_name_for_graph
  lambda_package_for_graph = var.lambda_package_for_graph
  bucket_name             = module.s3.bucket_name
  graph_queue_arn = var.graph_queue_arn
  graph_queue_url = var.graph_queue_url
  graph_queue_name = var.graph_queue_name
  graph_update_queue_arn = var.graph_update_queue_arn
  graph_update_queue_url = var.graph_update_queue_url
  graph_update_queue_name = var.graph_update_queue_name 
}

module "simulated_ec2" {
  source = "./modules/simulated_ec2"
  bucket_name = module.s3.bucket_name
  graph_update_queue_url = var.graph_update_queue_url
}
