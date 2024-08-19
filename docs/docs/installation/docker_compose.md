# Docker-Compose Deployment

## Run via Docker-Compose
```python
$ docker compose up -d
------------------------------------------
[+] Building 0.0s (0/0)
[+] Running 2/2
✔ Container gpt-db-db-1         Started                                                                                                                                                                                          0.4s
✔ Container gpt-db-webserver-1  Started
```


## View log
```python
$ docker logs gpt-db-webserver-1 -f
```

:::info note

For more configuration content, you can view the `docker-compose.yml` file
:::


## Visit
Open the browser and visit [http://localhost:5670](http://localhost:5670)
