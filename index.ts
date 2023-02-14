import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const cfg = new pulumi.Config()

const role = new aws.iam.Role("lambda_role", {
    assumeRolePolicy: JSON.stringify({
        Version: "2012-10-17",
        Statement: [
            {
                Action: "sts:AssumeRole",
                Principal: {
                    Service: "lambda.amazonaws.com",
                },
                Effect: "Allow",
                Sid: "",
            },
        ],
    }),
});

const lambdaFunction = new aws.lambda.Function("openai_lambda_chat", {
    runtime: "python3.9",
    handler: "chat.handler",
    code: new pulumi.asset.FileArchive("dist"),
    environment: {
      variables: {
        OPENAI_API_KEY: cfg.requireSecret("openai-api-key"),
      },
    },
    role: role.arn,
    timeout: 60,
    memorySize: 512,
    layers: [
      "arn:aws:lambda:eu-west-1:336392948345:layer:AWSSDKPandas-Python39:3"
    ], 
});
