# Design Decisions

## Why Serverless?

Serverless allows us to reduce infrastructure maintenance and scale automatically with usage. This is especially suitable for bursty, unpredictable traffic like account creation.

## Why SNS for Events?

Publishing domain events like `ACCOUNT_CREATED` to SNS decouples the services. Any downstream service (e.g., audit logs, analytics, fraud detection) can subscribe to the topic independently.

## DynamoDB over RDS?

DynamoDB offers lower latency and effortless scaling. For write-heavy, key-based access like account creation, it's a better fit than relational databases.

## API Gateway Proxy Integration

API Gateway is configured in Lambda Proxy mode to preserve full request context (headers, path, body) with minimal mapping logic.

## Separation of Concerns

The Lambda responsible for account creation only creates the account and publishes an event. It does not log to S3 or process the event. This promotes loose coupling and better testability.
