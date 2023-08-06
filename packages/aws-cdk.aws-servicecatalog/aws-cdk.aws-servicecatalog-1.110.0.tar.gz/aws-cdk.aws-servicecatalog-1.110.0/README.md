# AWS Service Catalog Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

[AWS Service Catalog](https://docs.aws.amazon.com/servicecatalog/latest/dg/what-is-service-catalog.html)
enables organizations to create and manage catalogs of products for their end users that are approved for use on AWS.

## Table Of Contents

* [Portfolio](#portfolio)

  * [Granting access to a portfolio](#granting-access-to-a-portfolio)
  * [Sharing a portfolio with another AWS account](#sharing-a-portfolio-with-another-aws-account)

The `@aws-cdk/aws-servicecatalog` package contains resources that enable users to automate governance and management of their AWS resources at scale.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_servicecatalog as servicecatalog
```

## Portfolio

AWS Service Catalog portfolios allow admins to manage products that their end users have access to.
Using the CDK, a new portfolio can be created with the `Portfolio` construct:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
servicecatalog.Portfolio(self, "MyFirstPortfolio",
    display_name="MyFirstPortfolio",
    provider_name="MyTeam"
)
```

You can also specify properties such as `description` and `acceptLanguage`
to help better catalog and manage your portfolios.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
servicecatalog.Portfolio(self, "MyFirstPortfolio",
    display_name="MyFirstPortfolio",
    provider_name="MyTeam",
    description="Portfolio for a project",
    accept_language=servicecatalog.AcceptLanguage.EN
)
```

Read more at [Creating and Managing Portfolios](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/catalogs_portfolios.html).

A portfolio that has been created outside the stack can be imported into your CDK app.
Portfolios can be imported by their ARN via the `Portfolio.fromPortfolioArn()` API:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
portfolio = servicecatalog.Portfolio.from_portfolio_arn(self, "MyImportedPortfolio", "arn:aws:catalog:region:account-id:portfolio/port-abcdefghi")
```

### Granting access to a portfolio

You can manage end user access to a portfolio by granting permissions to `IAM` entities like a user, group, or role.
Once resources are deployed end users will be able to access them via the console or service catalog CLI.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_iam as iam


user = iam.User(self, "MyUser")
portfolio.give_access_to_user(user)

role = iam.Role(self, "MyRole",
    assumed_by=iam.AccountRootPrincipal()
)
portfolio.give_access_to_role(role)

group = iam.Group(self, "MyGroup")
portfolio.give_access_to_group(group)
```

### Sharing a portfolio with another AWS account

A portfolio can be programatically shared with other accounts so that specified users can also access it:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
portfolio.share_with_account("012345678901")
```
