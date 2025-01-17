output "graph_queue_arn" {
  value = aws_sqs_queue.graph_queue.arn
}

output graph_queue_url {
  value = aws_sqs_queue.graph_queue.url
}

output graph_queue_name {
  value = aws_sqs_queue.graph_queue.name
}

output graph_update_queue_arn {
  value = aws_sqs_queue.graph_update_queue.arn
}

output graph_update_queue_url {
  value = aws_sqs_queue.graph_update_queue.url
}

output graph_update_queue_name {
  value = aws_sqs_queue.graph_update_queue.name
}