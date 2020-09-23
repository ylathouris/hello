# 7. Secrets

Date: 2020-09-21

## Status

Accepted

## Context

We need a way to store secrets that are used by our application.

## Decision

We are going to use AWS SSM. We will store our secrets as Secure Strings.

## Consequences

**Pros:**

* Can store secrets safely
* Can store other variables if needed
* Cost Effective

**Cons:**

* Not as feature rich as AWS Secrets Manager
