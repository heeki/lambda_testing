## Testing, Coverage, Signing
This is a sample repository to demo unit testing, code coverage, and code signing for deployment safety.

## Testing Notes
The `unittest` module is used for conducting unit tests. Tests are under the test directory. Tests can be executed with the following command: `make unittest`.

## Coverage Notes
The `coverage` module is used for evaluating code coverage. Code coverage reports can be generated with the following command: `make coverage`. An HTML report is generated at reports/index.html.

## Signing Notes
The AWS Signer service is used to sign code artifacts for both Lambda functions and layers to ensure that these artifacts are only deployed if they match the original signature.

[Documentation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-codesigning.html) shows that governance controls can be enforced to ensure that functions are created only with code signing configurations.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowReferencingCodeSigningConfig",
      "Effect": "Allow",
      "Action": [
          "lambda:CreateFunction",
        ],
      "Resource": "*",
      "Condition": {
          "StringEquals": {
              "lambda:CodeSigningConfigArn": "arn:aws:lambda:us-west-2:123456789012:code-signing-config:csc-0d4518bd353a0a7c6"
          }
      }
    }
  ]
} 
```