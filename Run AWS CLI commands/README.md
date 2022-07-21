### Amazon Web Services CLI with Lando dev tool

#### Set up

Under `services:` put this:

```
  aws:
    scanner: false
    type: compose
    app_mount: delegated
    services:
      user: root
      image: amazon/aws-cli:2.7.11
      command: tail -f /dev/null
      volumes:
        - aws:/root/.aws
      environment:
        LANDO_DROP_USER: root
    volumes:
      aws:

```

Under `tooling:` put this:

```
  aws:
    service: aws
    user: root

```

Rebuild the lando project: `lando rebuild -y`
After rebuilding the aws configurations will not be lost because the .config folder is saved in a volume.


#### Usage

The process is the exact same with the usage of aws cli. Just don't forget to put lando before these commands because they run in a container.

But first you need to authenticate:


```
lando aws configure
```

List configuration:

```
lando aws configure list
```

For example: list the S3 buckets.

```
lando aws s3api list-buckets --query "Buckets[].Name"
```
