# Kubectl bundle for Cog

Early trial of a bundle to expose kubectl commands from Slack.

## TL;DR

```
# get resources
!kubectl:get <resource-type> [-n namespace] [-a=false] [-l selector]

# run
!kubectl:run <name> --image=<image> --labels <command> [-n namespace] [--generator gen] [--port] [--expose=false]
```

## References

- [kubectl docs](https://kubernetes.io/docs/user-guide/kubectl-overview/)

# Installing

## From GitHub repository:

From the cog command line

```
wget -qO- https://github.com/honestbee/cog-kubectl/raw/master/config.yaml |
 cogctl bundle install -er default - --force
```

# Configuring

The `kubectl` bundle requires Kubernetes credentials with appropriate role.

You can set these variables with Cog's dynamic config feature:

```bash
echo '"KUBERNETES_TOKEN": <YOUR_TOKEN>' >> config.yaml
echo '"KUBERNETES_SERVER": <YOUR_API_ENDPOINT>' >> config.yaml
echo '"KUBERNETES_CERT": <YOUR_CA_CERT_BASE64>' >> config.yaml
cogctl bundle config create kubectl config.yaml --layer=base
```

```
!permission grant r53:read cog-admin
!kubectl:get po
```

# Development

## Building

To build the Docker image, simply run:

    $ make docker

Requires Docker.

## Running Bundle Locally

Test commands locally:

Create `.env`:
```
COG_BUNDLE=kubectl

KUBERNETES_TOKEN=AKIA...
KUBERNETES_SERVER=...
KUBERNETES_CERT=...
```

Add Command and argument(s)
```
COG_COMMAND=get
COG_ARGC=1
COG_ARGV=pods
```

Confirm environment is set properly:

```
docker-compose config
```

Test Options (in .env file):
```
# all passed in option flags
COG_OPTS=selector,show-all

# selector as string option
COG_OPT_SELECTOR=app=spider

# zone as bool option
COG_OPT_SHOW-ALL=True
```

Run the command using the bundle:
```bash
docker-compose run command
```

## Running Bundle through Shell

similar to above, set environment variables (either via `.env`) and confirm
```bash
docker-compose config
```

```bash
$ docker-compose run command sh
$ python -c "from kubectl.commands.get import Get;g=Get();g.execute()"
```

