variable "bucket_name" {
  description = "Nombre del bucket S3"
  type        = string
  default     = "graphword-bucket"
}

variable "graph_update_queue_url" {
  description = "Nombre de la cola SQS"
  type        = string
}