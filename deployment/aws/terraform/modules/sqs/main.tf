resource "aws_sqs_queue" "graph_update_queue" {
  name                      = "graph-update-queue"
  visibility_timeout_seconds = 300
  message_retention_seconds  = 86400
  sqs_managed_sse_enabled    = true
}

resource "aws_sqs_queue" "graph_queue" {
  name                      = "graph-queue"
  visibility_timeout_seconds = 300
  message_retention_seconds  = 86400
  sqs_managed_sse_enabled    = true
}