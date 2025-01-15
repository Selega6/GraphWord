output "lambda_function_name" {
  description = "Nombre de la función Lambda creada"
  value       = aws_lambda_function.crawler_lambda.function_name
}

output "lambda_role_arn" {
  description = "ARN del rol de ejecución de Lambda"
  value       = aws_iam_role.lambda_exec_role.arn
}

output "crawler_lambda_arn" {
  description = "ARN de la función Lambda de procesamiento"
  value       = aws_lambda_function.crawler_lambda.arn
}
