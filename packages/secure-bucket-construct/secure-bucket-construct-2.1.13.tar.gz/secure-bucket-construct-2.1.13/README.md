[![npm version](https://badge.fury.io/js/enterprise-secure-bucket.svg)](https://badge.fury.io/js/enterprise-secure-bucket)
[![release](https://github.com/yvthepief/secure_bucket_construct/actions/workflows/release.yml/badge.svg)](https://github.com/yvthepief/secure_bucket_construct/actions/workflows/release.yml)

# Secure Bucket Construcs

Blog: https://yvovanzee.nl/secure-s3-bucket-construct-with-cdk-version-2

This Secure Bucket construcs extends the S3 Bucket construct. When using this construct, you will create a S3 bucket with default security best practises enabled. These are:

* Block public access
* Enabled versioning
* Enable enforce SSL to connect to bucket
* Enabled Bucket access logging
* Encryption of the bucket with a customer managed KMS key with enabled key rotation and trusted account identities.

These best practises are enforced. When creating a SecureBucket with for example versioning disabled, it will be overwritten to enabled.

# Usage

## install package

```bash
npm install @enterprise_secure_bucket
```

## Import the secure bucket construct in your code.

```python
// Import necessary packages
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { SecureBucket } from 'enterprise-secure-bucket';

export class SecureBucketStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    new SecureBucket(this, 'myEnterpriseLevelSecureBucket',{});
  }
}
```
