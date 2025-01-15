variable "bucket_name" {
  description = "Nombre del bucket S3"
  type        = string
}

variable "lambda_name" {
  description = "Nombre de la función Lambda"
  type        = string
}

variable "lambda_package" {
  description = "Ruta al paquete ZIP de la Lambda"
  type        = string
}

variable "lambda_name_for_graph" {
  description = "Nombre de la Lambda para generación de grafos"
  type        = string
}

variable "lambda_package_for_graph" {
  description = "Paquete ZIP de la Lambda de grafos"
  type        = string
}

variable "output_file_for_graph" {
  description = "Ruta del archivo de salida del grafo"
  type        = string
}

variable "download_folder" {
  description = "Carpeta de descargas de la Lambda"
  type        = string
}

variable "output_file" {
  description = "Ruta del archivo de salida procesado"
  type        = string
}

variable "daily_trigger_expression" {
  description = "Expresión CRON para la ejecución diaria"
  type        = string
  default     = "cron(0 3 * * ? *)"
}

variable "graph_queue_arn" {
  description = "ARN de la cola SQS"
  type        = string
}

variable "graph_queue_url" {
  description = "URL de la cola SQS"
  type        = string
}

variable "graph_queue_name" {
  description = "Nombre de la cola SQS"
  type        = string
}

variable manual_trigger_expression {
  description = "Fuente de eventos para disparar la Lambda"
  type        = string
  default     = "value"
}

variable "graph_update_queue_arn" {
  description = "ARN de la cola SQS"
  type        = string
}

variable "graph_update_queue_url" {
  description = "URL de la cola SQS"
  type        = string
}

variable "graph_update_queue_name" {
  description = "Nombre de la cola SQS"
  type        = string
}
