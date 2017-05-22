# Testing sample commands from shell

Get a shell with source code mounted:
```
docker-compose run command sh
```

1.  Get pods based on 2 label queries:

    ```bash
    COG_ARGC=1 COG_ARGV_0=po COG_OPTS=selector COG_OPT_SELECTOR_COUNT=2 COG_OPT_SELECTOR_0=app=atlas-atlas COG_OPT_SELECTOR_1=chart=address-0.2.0 python -c "from kubectl.commands.get import Get;c=Get();c.execute()"
    ```

1.  Get pods sorted by Node name:

    ```bash
    env COG_ARGC=1 COG_ARGV_0=po COG_OPTS=sort-by COG_OPT_SORT-BY=.spec.nodeName python -c "from kubectl.commands.get import Get;c=Get();c.execute()"
    ```

1.  Get svc:

    ```bash
    COG_ARGC=1 COG_ARGV_0=svc python -c "from kubectl.commands.get import Get;c=Get();c.execute()"
    ```

1.  Get deployments:

    ```bash
    COG_ARGC=1 COG_ARGV_0=deploy python -c "from kubectl.commands.get import Get;c=Get();c.execute()"
    ```

1.  Get multiple resource types:

    ```bash
    COG_ARGC=1 COG_ARGV_0=po,deploy,svc python -c "from kubectl.commands.get import Get;c=Get();c.execute()"
    ```

1.  Create an nginx Deployment imperatively:

    ```bash
    kubectl run nginx --image=nginx:1.10-alpine --port=80
    ```

    ```bash
    COG_ARGC=1 COG_ARGV_0=nginx COG_OPTS=image,port COG_OPT_IMAGE=nginx:1.10-alpine COG_OPT_PORT=80 python -c "from kubectl.commands.run import Run;c=Run();c.execute()"
    ```

1.  Get the nginx Deployment by label:

    ```bash
    kubectl get deploy -l run=nginx
    ```

    ```bash
    COG_ARGC=1 COG_ARGV_0=deploy COG_OPTS=selector COG_OPT_SELECTOR_COUNT=1 COG_OPT_SELECTOR_0=run=nginx python -c "from kubectl.commands.get import Get;c=Get();c.execute()"
    ```

1.  Expose the nginx Deployment:

    ```bash
    kubectl expose deploy nginx --target-port=80 --type=LoadBalancer
    ```

    ```bash
    env COG_ARGC=2 COG_ARGV_0=deploy COG_ARGV_1=nginx COG_OPTS=container-port,type COG_OPT_CONTAINER-PORT=80 COG_OPT_TYPE=loadBalancer python -c "from kubectl.commands.expose import Expose;c=Expose();c.execute()"
    ```


TODO:

1.  Scale the nginx Deployment:

    ```bash
    kubectl scale deploy nginx --replicas=3
    ```

1.  Set the image tag for nginx Deployment:

    ```bash
    kubectl set image deployment/nginx nginx=nginx:1.11-alpine
    ```

1.  Create deployment with altnerative entrypoint:

    ```bash
    kubectl run alpine-shell --image=alpine:3.5 -- sleep 1000
    ```