# Cluster Deployment

## Install command line tools
All the following operations are completed through the `gptdb` command. To use the `gptdb` command, you first need to install the `GPT-DB` project. You can install it through the following command

```shell
$ pip install -e ".[default]"
```
It can also be used in script mode
```shell
$ python pilot/scripts/cli_scripts.py
```

## Start Model Controller
```shell
$ gptdb start controller
```

## View log
```shell
$ docker logs db-gpt-webserver-1 -f
```
By default, `Model Server` will start on port `8000`

## Start Model Worker

:::tip
Start `glm-4-9b-chat` model Worker
:::

```shell
gptdb start worker --model_name glm-4-9b-chat \
--model_path /app/models/glm-4-9b-chat \
--port 8001 \
--controller_addr http://127.0.0.1:8000
```


:::tip
Start `vicuna-13b-v1.5` model Worker
:::

```shell
gptdb start worker --model_name vicuna-13b-v1.5 \
--model_path /app/models/vicuna-13b-v1.5 \
--port 8002 \
--controller_addr http://127.0.0.1:8000
```
:::info note
⚠️  Make sure to use your own model name and model path.

:::


## Start Embedding Model Worker

```shell
gptdb start worker --model_name text2vec \
--model_path /app/models/text2vec-large-chinese \
--worker_type text2vec \
--port 8003 \
--controller_addr http://127.0.0.1:8000
```
:::info note
⚠️  Make sure to use your own model name and model path.

:::

## Start Reranking Model Worker

```shell
gptdb start worker --worker_type text2vec \
--rerank \
--model_path /app/models/bge-reranker-base \
--model_name bge-reranker-base \
--port 8004 \
--controller_addr http://127.0.0.1:8000
```
:::info note
⚠️  Make sure to use your own model name and model path.

:::

:::tip
View and inspect deployed models
:::


```shell
$ gptdb model list

+-------------------+------------+------------+------+---------+---------+-----------------+----------------------------+
|    Model Name     | Model Type |    Host    | Port | Healthy | Enabled | Prompt Template |       Last Heartbeat       |
+-------------------+------------+------------+------+---------+---------+-----------------+----------------------------+
|   glm-4-9b-chat     |    llm     | 172.17.0.2 | 8001 |   True  |   True  |                 | 2023-09-12T23:04:31.287654 |
|  WorkerManager    |  service   | 172.17.0.2 | 8001 |   True  |   True  |                 | 2023-09-12T23:04:31.286668 |
|  WorkerManager    |  service   | 172.17.0.2 | 8003 |   True  |   True  |                 | 2023-09-12T23:04:29.845617 |
|  WorkerManager    |  service   | 172.17.0.2 | 8002 |   True  |   True  |                 | 2023-09-12T23:04:24.598439 |
|  WorkerManager    |  service   | 172.21.0.5 | 8004 |   True  |   True  |                 | 2023-09-12T23:04:24.598439 |
|     text2vec      |  text2vec  | 172.17.0.2 | 8003 |   True  |   True  |                 | 2023-09-12T23:04:29.844796 |
| vicuna-13b-v1.5   |    llm     | 172.17.0.2 | 8002 |   True  |   True  |                 | 2023-09-12T23:04:24.597775 |
| bge-reranker-base |  text2vec  | 172.21.0.5 | 8004 |   True  |   True  |                 | 2024-05-15T11:36:12.935012 |
+-------------------+------------+------------+------+---------+---------+-----------------+----------------------------+
```


## Use model serving

The model service deployed as above can be used through gptdb_server. First modify the `.env` configuration file to change the connection model address

```shell
gptdb start webserver --light
```

## Start Webserver 

```shell
LLM_MODEL=vicuna-13b-v1.5
# The current default MODEL_SERVER address is the address of the Model Controller
MODEL_SERVER=http://127.0.0.1:8000
```
`--light` means not to start the embedded model service.


Or it can be started directly by command to formulate the model.
```shell
LLM_MODEL=glm-4-9b-chat gptdb start webserver --light --remote_embedding
```

## Command line usage
For more information about the use of the command line, you can view the command line help. The following is a reference example.


:::tip
View gptdb help `gptdb --help`
:::

```shell
gptdb --help

Already connect 'gptdb'
Usage: gptdb [OPTIONS] COMMAND [ARGS]...

Options:
  --log-level TEXT  Log level
  --version         Show the version and exit.
  --help            Show this message and exit.

Commands:
  install    Install dependencies, plugins, etc.
  knowledge  Knowledge command line tool
  model      Clients that manage model serving
  start      Start specific server.
  stop       Start specific server.
  trace      Analyze and visualize trace spans.
```


:::tip
Check the gptdb start command `gptdb start --help`
:::

```shell
gptdb start --help

Already connect 'gptdb'
Usage: gptdb start [OPTIONS] COMMAND [ARGS]...

  Start specific server.

Options:
  --help  Show this message and exit.

Commands:
  apiserver   Start apiserver
  controller  Start model controller
  webserver   Start webserver(gptdb_server.py)
  worker      Start model worker
(gptdb_env) magic@B-4TMH9N3X-2120 ~ %
```

:::tip
View the gptdb start model service help command `gptdb start worker --help`
:::

```shell
gptdb start worker --help

Already connect 'gptdb'
Usage: gptdb start worker [OPTIONS]

  Start model worker

Options:
  --model_name TEXT               Model name  [required]
  --model_path TEXT               Model path  [required]
  --worker_type TEXT              Worker type
  --worker_class TEXT             Model worker class,
                                  pilot.model.cluster.DefaultModelWorker
  --model_type TEXT               Model type: huggingface, llama.cpp, proxy
                                  and vllm  [default: huggingface]
  --host TEXT                     Model worker deploy host  [default: 0.0.0.0]
  --port INTEGER                  Model worker deploy port  [default: 8001]
  --daemon                        Run Model Worker in background
  --limit_model_concurrency INTEGER
                                  Model concurrency limit  [default: 5]
  --standalone                    Standalone mode. If True, embedded Run
                                  ModelController
  --register                      Register current worker to model controller
                                  [default: True]
  --worker_register_host TEXT     The ip address of current worker to register
                                  to ModelController. If None, the address is
                                  automatically determined
  --controller_addr TEXT          The Model controller address to register
  --send_heartbeat                Send heartbeat to model controller
                                  [default: True]
  --heartbeat_interval INTEGER    The interval for sending heartbeats
                                  (seconds)  [default: 20]
  --log_level TEXT                Logging level
  --log_file TEXT                 The filename to store log  [default:
                                  gptdb_model_worker_manager.log]
  --tracer_file TEXT              The filename to store tracer span records
                                  [default:
                                  gptdb_model_worker_manager_tracer.jsonl]
  --tracer_storage_cls TEXT       The storage class to storage tracer span
                                  records
  --device TEXT                   Device to run model. If None, the device is
                                  automatically determined
  --prompt_template TEXT          Prompt template. If None, the prompt
                                  template is automatically determined from
                                  model path, supported template: zero_shot,vi
                                  cuna_v1.1,llama-2,codellama,alpaca,baichuan-
                                  chat,internlm-chat
  --max_context_size INTEGER      Maximum context size  [default: 4096]
  --num_gpus INTEGER              The number of gpus you expect to use, if it
                                  is empty, use all of them as much as
                                  possible
  --max_gpu_memory TEXT           The maximum memory limit of each GPU, only
                                  valid in multi-GPU configuration
  --cpu_offloading                CPU offloading
  --load_8bit                     8-bit quantization
  --load_4bit                     4-bit quantization
  --quant_type TEXT               Quantization datatypes, `fp4` (four bit
                                  float) and `nf4` (normal four bit float),
                                  only valid when load_4bit=True  [default:
                                  nf4]
  --use_double_quant              Nested quantization, only valid when
                                  load_4bit=True  [default: True]
  --compute_dtype TEXT            Model compute type
  --trust_remote_code             Trust remote code  [default: True]
  --verbose                       Show verbose output.
  --help                          Show this message and exit.
```

:::tip
View gptdb model service related commands `gptdb model --help`
:::

```shell
gptdb model --help


Already connect 'gptdb'
Usage: gptdb model [OPTIONS] COMMAND [ARGS]...

  Clients that manage model serving

Options:
  --address TEXT  Address of the Model Controller to connect to. Just support
                  light deploy model, If the environment variable
                  CONTROLLER_ADDRESS is configured, read from the environment
                  variable
  --help          Show this message and exit.

Commands:
  chat     Interact with your bot from the command line
  list     List model instances
  restart  Restart model instances
  start    Start model instances
  stop     Stop model instances
```



