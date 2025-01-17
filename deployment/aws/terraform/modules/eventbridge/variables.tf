variable "startup_event_pattern" {
  description = "Patrón de eventos para iniciar procesos al arrancar EC2"
  type        = string
  default     = <<EOF
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
EOF
}

variable "daily_trigger_expression" {
  description = "Expresión CRON para la ejecución diaria"
  type        = string
  default     = "cron(0 3 * * ? *)"
}

variable "crawler_lambda_arn" {
  description = "ARN de la Lambda que será disparada por EventBridge"
  type        = string
}

variable "manual_trigger_expression" {
  description = "Fuente de eventos para disparar la Lambda"
  type        = string
  default = "value"
}

