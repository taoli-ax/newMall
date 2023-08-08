```bash
worker_1  | [2023-01-07 05:52:27,995: ERROR/MainProcess] consumer: Cannot connect to amqp://admin:**@127.0.0.1:5672//: [Errno 111] Connection refused.
worker_1  | Trying again in 4.00 seconds... (2/100)
```
<p>
why this happen??
</p>

*Hmm...,but rabbitmq running well,and also available visit in Chrome ```localhost:15672```*
```console
rabbitmq  |   Starting broker... completed with 3 plugins.
```
### try to fix with solution 1

```shell
docker cp  containerId:/etc/rabbitmq/conf.d/10-defaults.conf ./

NODE_IP_ADDRESS=127.0.0.1
SHIT...not work

```
### try to fix with solution 2
<p>set new user and expose 5672,someone says expose different with ports</p>

```yaml
environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin
expose:
  - 5672
```
<p>shit ... not work</p>

### try to fix with solution 3
<p> If rabbitmq first,and then celery worker follow it ,or links...??</p>

```yaml
 worker:
    ...
    links:
      - db
      - rabbitmq
    depends_on:
      - rabbitmq
```
<p> shit ... not work and ps: links is not used any more,throw it....</p>

### try to fix with solution 4

```shell
docker port rabbitmq
    15672/tcp -> 0.0.0.0:15672
    15672/tcp -> :::15672
    22/tcp -> 0.0.0.0:22
    22/tcp -> :::22
    5672/tcp -> 0.0.0.0:5672
    5672/tcp -> :::5672

```
docker-desktop rabbitmq show
```shell
 0.0.0.0:15672
 :::15672
```
*:::15672 is Ipv6 address,should I use Ipv4 address?*

***ONE NIGHT SLEEP LATER...***<BR>
***ONE NIGHT SLEEP LATER...***<BR>
***ONE NIGHT SLEEP LATER...***<BR>
***ONE NIGHT SLEEP LATER...***<BR>

<ul>
<li>why amqp://admin:**@127.0.0.1:5672// can not work</li>
<li>why localhost:15672 works</li>
</ul>

***Is it because the ip address somehow different ??***

***Let's set same IP address for both of celery and browser***

## How to fix ?
<p>we need fix IP for rabbitmq and worker
Yeah ,you heard me ,we need create a new network for our docker-compose </p>



```yaml
networks:
  nn:
    ipam: 
      driver: default
      config:
        - subnet: "192.168.5.0/24"
          
services:
   rabbitmq:
    image: rabbitmq:3.11-management
    container_name: rabbitmq
    hostname: rabbit
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin
    volumes:
      - ./rabbitmq:/var/lib/rabbitmq
      - ./conf:/etc/rabbitmq
    privileged: true
    ports:
      - 15672:15672
      - 5672:5672
      - 22:22
    expose:
      - 5672
    networks:
      nn:
        ipv4_address: "192.168.5.4"
```

```shell

```


# It works!


```shell
rabbitmq  |   Starting broker... completed with 3 plugins.
worker_1  | [2023-01-07 05:52:32,011: INFO/MainProcess] Connected to amqp://admin:**@192.168.5.4:5672//
worker_1  | [2023-01-07 05:52:32,026: INFO/MainProcess] mingle: searching for neighbors
worker_1  | [2023-01-07 05:52:33,060: INFO/MainProcess] mingle: all alone
worker_1  | [2023-01-07 05:52:33,100: INFO/MainProcess] celery@4a0189310984 ready.
```

<a href="https://docs.docker.com/compose/compose-file/#network-configuration-reference">network-configuration-reference</a>