# No longer maintained

Now that Terraform has built-in support for multiple environments starting in version 0.9.0 this utility is no longer needed.


# Terraflow

Terraflow is a python utility that makes it easy to manage multiple environments with Terraform. This tool is ideal for running the following Terraform commands `plan, apply, output, destroy`. It does not intend to be the penultimate terraform wrapper. It specifically aims just makes managing multiple environments easier.

## Prerequisites

- **Terraform**: You can download the [latest version here](https://releases.hashicorp.com/terraform/).
- **S3 Bucket**: You will need an S3 bucket to store your state files.
- **awscli**: You will need the AWS CLI and credentials configured. `pip install awscli && aws configure`.

## Installation

```
pip install terraflow
```

## Terms

- **stack**: A collection of cloud resources that are configured to achieve a broad, but unified goal. For example, consider groups of machines that are dedicated to grabbing, storing, transforming, anaylzing, and displaying logs. Not every machine is able to perform every task, but they work with each other to achieve a common goal. Together, they form a logging stack.
- **environment**: An instantiation of a stack. Environments usually represent different SLA's for a stack. For example, a stack may have infrastructure testing, integration, staging, and production environments. Each environment has different uptime guarantees, but all should have the same types of deployed resoures.


## Directory Structure

This tool relies on a very specific folder structure to work. That structure is as follows:

```
├── stacks
│   └── stack_name
│   |   ├── envs
│   |   │   ├── env_name.tfvars
│   |   ├── main.tf
├── .tfconfig
```

- `stacks`: Stacks that can be instatiated multiple times fall under here.
  - `stacks/stack_name`: Each stack will have it's own subfolder along with a `main.tf` file. This folder will serve as the root for where the terraform commands will be run.
  - `stacks/stack_name/envs/env_name.tfvars`: Each environment must have it's own `.tfvars` file to provide environment specific variable overrides when instatiating a stack.

## Configuration

Every project needs to have a `.tfconfig` file in the root of the project. This will allow the tool to determine where the root of the project is as well as provide project specific configuration.

```
{
  "aws": {
    "profile": "mgmt"
  },
  "backend": {
    "s3": {
      "config": {
        "profile": "mgmt",
        "bucket": "my_terraform_state",
        "region": "us-east-1"
      }
    }
  }
}
```

- `aws`:
    - `profile`: The AWS profile with your credentials that have access to the s3 bucket to store the state in.
- `backend`:
    - `s3`: S3 specific configuration for storing the Terraform remote state
    - `config`:
        - `profile`: The aws profile to use for the s3 backend configuration. If not present it defaults to the top-level `aws.profile` setting.
        - `bucket`: The bucket where the remote state will be stored.
        - `region`: Which region to create the bucket in
        - `key`: This generated automatically based on and will be `<stack_name>/<env_name>.tfstate`

If you're creating multiple environments across different AWS accounts (i.e. mgmt, dev, preprod, prod) it's recommended that you create a bucket in one of those accounts and use that to save your state.

```
# ~/.aws/credentials

[prod]
aws_access_key_id
aws_secret_access_key

[mgmt]
aws_access_key_id
aws_secret_access_key
```

## Usage

```
$ tf -h
usage: tf [-h] command stack environment ...

positional arguments:
  command      Terraform command to execute
  stack        The name of the stack to target.
  environment  The name of the environment to target.
  tfargs       Additional arguments to passthrough to Terraform.

optional arguments:
  -h, --help   show this help message and exit
```

- To execute a plan for a specific stack and environment:
  ```
  tf plan <stack_name> <env>
  ```

- To delete a specific module run this:
   ```
   tf delete <stack_name> <env> -target=module.mymodule
   ```

