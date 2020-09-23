[![CircleCI](https://circleci.com/gh/ylathouris/hello.svg?style=shield)](https://circleci.com/gh/ylathouris/hello)  ![Coverage](coverage.svg)

# Hello

A simple Hello World serverless application.


### Architecture Decisions (ADRs)

* [Record Decisions](docs/arch/001-record-decisions.md)
* [Compute](docs/arch/002-compute.md)
* [Runtime](docs/arch/003-runtime.md)
* [Serverless Framework](docs/arch/004-serverless-framework.md)
* [Test Framework](docs/arch/005-test-framework.md)
* [Access Control](docs/arch/006-access-control.md)
* [Secrets](docs/arch/007-secrets.md)
* [Deployment](docs/arch/008-deployment.md)

<br/>

### Development

**Test**

Use the following script to run the unit tests.

```shell
$ ./test
```

**Deploy**

Use the following script to deploy the application to AWS. This
will perform the following steps:

* Create the build artifact for the source code using `chalice package`
* Create a plan for the deployment using `terraform plan`
* Ask if you want to continue with the deployment
* Perform the deployment using `terraform apply`

```shell
$ ./deploy
```

**Destroy**

Use the following script to teardown the application (i.e. delete
all the infrastructure resources from AWS)

```shell
$ ./destroy
```
