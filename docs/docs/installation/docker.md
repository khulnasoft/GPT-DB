# Docker Deployment

## Docker image preparation

There are two ways to prepare a Docker image. 1. Pull from the official image 2. Build locally. You can **choose any one** during actual use.

1.Pulled from the official image repository, [Eosphoros AI Docker Hub](https://hub.docker.com/u/khulnasoft)
```bash
docker pull khulnasoft/gptdb:latest
```
2.local build(optional)
```bash
bash docker/build_all_images.sh
```
Check the Docker image
```bash
# command
docker images | grep "khulnasoft/gptdb"

# result
--------------------------------------------------------------------------------------
khulnasoft/gptdb-allinone       latest    349d49726588   27 seconds ago       15.1GB
khulnasoft/gptdb                latest    eb3cdc5b4ead   About a minute ago   14.5GB
```
`khulnasoft/gptdb` is the base image, which contains project dependencies and the sqlite database. The `khulnasoft/gptdb-allinone` image is built from `khulnasoft/gptdb`, which contains a MySQL database. Of course, in addition to pulling the Docker image, the project also provides Dockerfile files, which can be built directly through scripts in GPT-DB. Here are the build commands:

```bash
bash docker/build_all_images.sh
```
When using it, you need to specify specific parameters. The following is an example of specifying parameter construction:

```bash
bash docker/build_all_images.sh \
--base-image nvidia/cuda:11.8.0-runtime-ubuntu22.04 \
--pip-index-url https://pypi.tuna.tsinghua.edu.cn/simple \
--language zh
```
You can view the specific usage through the command `bash docker/build_all_images.sh --help`

## Run Docker container

### Run through Sqlite database


```bash
docker run --ipc host --gpus all -d \
-p 5670:5670 \
-e LOCAL_DB_TYPE=sqlite \
-e LOCAL_DB_PATH=data/default_sqlite.db \
-e LLM_MODEL=glm-4-9b-chat \
-e LANGUAGE=zh \
-v /data/models:/app/models \
--name gptdb \
khulnasoft/gptdb
```
Open the browser and visit [http://localhost:5670](http://localhost:5670)

- `-e LLM_MODEL=glm-4-9b-chat`, which means the base model uses `glm-4-9b-chat`. For more model usage, you can view the configuration in `/pilot/configs/model_config.LLM_MODEL_CONFIG`.
- `-v /data/models:/app/models`, specifies the model file to be mounted. The directory `/data/models` is mounted in `/app/models` of the container. Of course, it can be replaced with other paths.

After the container is started, you can view the logs through the following command
```bash
docker logs gptdb -f
```

### Run through MySQL database

```bash
docker run --ipc host --gpus all -d -p 3306:3306 \
-p 5670:5670 \
-e LOCAL_DB_HOST=127.0.0.1 \
-e LOCAL_DB_PASSWORD=aa123456 \
-e MYSQL_ROOT_PASSWORD=aa123456 \
-e LLM_MODEL=glm-4-9b-chat \
-e LANGUAGE=zh \
-v /data/models:/app/models \
--name db-gpt-allinone \
db-gpt-allinone
```
Open the browser and visit [http://localhost:5670](http://localhost:5670)

- `-e LLM_MODEL=glm-4-9b-chat`, which means the base model uses `glm-4-9b-chat`. For more model usage, you can view the configuration in `/pilot/configs/model_config.LLM_MODEL_CONFIG`.
- `-v /data/models:/app/models`, specifies the model file to be mounted. The directory `/data/models` is mounted in `/app/models` of the container. Of course, it can be replaced with other paths.

After the container is started, you can view the logs through the following command
```bash
docker logs db-gpt-allinone -f
```

### Run through the OpenAI proxy model
```bash
PROXY_API_KEY="You api key"
PROXY_SERVER_URL="https://api.openai.com/v1/chat/completions"
docker run --gpus all -d -p 3306:3306 \
-p 5670:5670 \
-e LOCAL_DB_HOST=127.0.0.1 \
-e LOCAL_DB_PASSWORD=aa123456 \
-e MYSQL_ROOT_PASSWORD=aa123456 \
-e LLM_MODEL=proxyllm \
-e PROXY_API_KEY=$PROXY_API_KEY \
-e PROXY_SERVER_URL=$PROXY_SERVER_URL \
-e LANGUAGE=zh \
-v /data/models/text2vec-large-chinese:/app/models/text2vec-large-chinese \
--name db-gpt-allinone \
db-gpt-allinone
```
- `-e LLM_MODEL=proxyllm`, set the model to serve the third-party model service API, which can be openai or fastchat interface.
- `-v /data/models/text2vec-large-chinese:/app/models/text2vec-large-chinese`, sets the knowledge base embedding model to `text2vec`

Open the browser and visit [http://localhost:5670](http://localhost:5670)


