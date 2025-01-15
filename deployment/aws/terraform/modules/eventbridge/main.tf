resource "aws_cloudwatch_event_rule" "daily_trigger" {
  name                = "daily-trigger"
  schedule_expression = var.daily_trigger_expression
}

resource "aws_cloudwatch_event_target" "daily_event_target" {
  rule      = aws_cloudwatch_event_rule.daily_trigger.name
  target_id = "dailyDownloadTrigger"
  arn       = var.crawler_lambda_arn
  role_arn  = aws_iam_role.eventbridge_role.arn
}

resource "aws_cloudwatch_event_rule" "manual_trigger" {
  name = "manual-crawler-trigger"

  event_pattern = jsonencode({
    "source": ["custom.trigger"],
    "detail-type": ["manual-invoke"]
  })
}

resource "aws_iam_role" "eventbridge_role" {
  name = "eventbridge-invoke-lambda"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "events.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_lambda_permission" "allow_eventbridge_crawler" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = var.crawler_lambda_arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_trigger.arn
}

resource "aws_cloudwatch_event_target" "manual_event_target" {
  rule      = aws_cloudwatch_event_rule.manual_trigger.name
  target_id = "manualDownloadTrigger"
  arn       = var.crawler_lambda_arn
  role_arn  = aws_iam_role.eventbridge_role.arn
}

resource "aws_lambda_permission" "allow_eventbridge_manual" {
  statement_id  = "AllowManualExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = var.crawler_lambda_arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.manual_trigger.arn
}
