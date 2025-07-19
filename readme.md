# Account Creation API (Serverless)

This is a simplified serverless application that exposes an HTTP POST endpoint to create customer accounts. It is built using AWS Lambda, DynamoDB, SNS, and API Gateway.

## Features

- ? Create new accounts via HTTP POST
- ? Store accounts in DynamoDB
- ? Emit audit events to SNS
- ? Publish event format suitable for downstream systems
- ? Environment-based configuration

## Stack

- AWS Lambda (Python)
- Amazon API Gateway
- DynamoDB
- SNS (Simple Notification Service)

## Endpoint

**POST** /accounts

### Headers:
- x-user-id: the ID of the user performing the action

### Body:
```json
{
  "name": "Empresa X",
  "parent_id": null,
  "metadata": {
    "sector": "Retail"
  }
}
```

### Response:
```json
{
  "message": "Account created",
  "account": {
    "account_id": "...",
    "name": "Empresa X",
    "parent_id": null,
    "metadata": {
      "sector": "Retail"
    },
    "version": 1
  }
}
```

## Environment Variables

- AUDIT_SNS_TOPIC_ARN � SNS topic ARN for publishing audit events
