### Google Cloud SDK with Lando dev tool

#### Set up

Under `services:` put this:

```
  cloud-sdk:
    type: compose
    app_mount: delegated
    services:
      image: google/cloud-sdk:389.0.0
      command: tail -f /dev/null
    volumes:
      cloud-sdk:

```

Under `tooling:` put this:

```
  gcloud:
    service: cloud-sdk
  gsutil:
    service: cloud-sdk

```

Rebuild the lando project: `lando rebuild -y`


#### Usage

The process is the exact same with gcloud or gsutil. Just don't forget to put lando before these commands because they run in a container.

But first you need to authenticate: (https://stackoverflow.com/questions/71561730/authorizing-client-libraries-without-access-to-a-web-browser-gcloud-auth-appli)


```
lando gcloud init --console-only
```

List already authenticated accounts:

```
lando gcloud auth list
```

If there are accounts listed here, you can perform operations according to your permissions.

For example: this is how you can get the GCS Bucket CORS settings:

```
lando gsutil cors get gs://mybucket123
```
