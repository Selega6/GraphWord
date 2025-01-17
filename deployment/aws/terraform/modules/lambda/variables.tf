variable "lambda_name" {
  description = "Nombre de la función Lambda"
  type        = string
}
variable "lambda_name_for_graph" {
  description = "Nombre de la función Lambda"
  type        = string
}

variable "lambda_package" {
  description = "Ruta al paquete ZIP de la Lambda"
  type        = string
  default     = "package.zip"
}

variable "lambda_package_for_graph" {
  description = "Ruta al paquete ZIP de la Lambda"
  type        = string
  default     = "package_graph.zip"
}

variable "bucket_name" {
  description = "Nombre del bucket S3 para la Lambda"
  type        = string
  default     = "graphword-bucket"
}

variable "download_folder" {
  description = "Carpeta de descargas para la Lambda"
  type        = string
  default     = "downloads"
}

variable "output_file" {
  description = "Ruta del archivo de salida procesado"
  type        = string
  default     = "processed/word_counts.txt"
}

variable "output_file_for_graph" {
  description = "Ruta del archivo de salida procesado"
  type        = string
  default     = "graphs/graph.pkl"
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
