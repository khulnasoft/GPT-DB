# Source Code Deployment

## Environmental requirements

| Startup Mode         | CPU * MEM    |       GPU      |         Remark  |
|:--------------------:|:------------:|:--------------:|:---------------:|
|     Proxy model          |    4C * 8G      |        None    |  Proxy model does not rely on GPU                         |
|     Local model          |    8C * 32G     |       24G      |  It is best to start locally with a GPU of 24G or above   |






### Download source code

:::tip
Download GPT-DB
:::



```bash
git clone https://github.com/khulnasoft/GPT-DB.git
```

### Miniconda environment installation

- The default database uses SQLite, so there is no need to install a database in the default startup mode. If you need to use other databases, you can read the [advanced tutorials](/docs/application_manual/advanced_tutorial) below. We recommend installing the Python virtual environment through the conda virtual environment. For the installation of Miniconda environment, please refer to the [Miniconda installation tutorial](https://docs.conda.io/projects/miniconda/en/latest/).

:::tip
Create a Python virtual environment
:::

```bash
python >= 3.10
conda create -n gptdb_env python=3.10
conda activate gptdb_env

# it will take some minutes
pip install -e ".[default]"
```

:::tip
Copy environment variables
:::
```bash
cp .env.template  .env
```


## Model deployment

GPT-DB can be deployed on servers with lower hardware through proxy model, or as a private local model under the GPU environment. If your hardware configuration is low, you can use third-party large language model API services, such as OpenAI, Azure, Qwen, ERNIE Bot, etc.

:::info note

⚠️  You need to ensure that git-lfs is installed
```bash
● CentOS installation: yum install git-lfs
● Ubuntu installation: apt-get install git-lfs
● MacOS installation: brew install git-lfs
```
:::
### Proxy model

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs
  defaultValue="openai"
  values={[
    {label: 'Open AI', value: 'openai'},
    {label: 'Qwen', value: 'qwen'},
    {label: 'ChatGLM', value: 'chatglm'},
    {label: 'WenXin', value: 'erniebot'},
    {label: 'Yi', value: 'yi'},
  ]}>
  <TabItem value="openai" label="open ai">
  Install dependencies

```bash
pip install  -e ".[openai]"
```

Download embedding model

```bash
cd GPT-DB
mkdir models and cd models
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese
```

Configure the proxy and modify LLM_MODEL, PROXY_API_URL and API_KEY in the `.env`file

```bash
# .env
LLM_MODEL=chatgpt_proxyllm
PROXY_API_KEY={your-openai-sk}
PROXY_SERVER_URL=https://api.openai.com/v1/chat/completions
# If you use gpt-4
# PROXYLLM_BACKEND=gpt-4
```
  </TabItem>
  <TabItem value="qwen" label="通义千问">
Install dependencies

```bash
pip install dashscope
```

Download embedding model

```bash
cd GPT-DB
mkdir models and cd models

# embedding model
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese
or
git clone https://huggingface.co/moka-ai/m3e-large
```

Configure the proxy and modify LLM_MODEL, PROXY_API_URL and API_KEY in the `.env`file

```bash
# .env
# Aliyun tongyiqianwen
LLM_MODEL=tongyi_proxyllm
TONGYI_PROXY_API_KEY={your-tongyi-sk}
PROXY_SERVER_URL={your_service_url}
```
  </TabItem>
  <TabItem value="chatglm" label="chatglm" >
Install dependencies

```bash
pip install zhipuai
```

Download embedding model

```bash
cd GPT-DB
mkdir models and cd models

# embedding model
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese
or
git clone https://huggingface.co/moka-ai/m3e-large
```

Configure the proxy and modify LLM_MODEL, PROXY_API_URL and API_KEY in the `.env`file

```bash
# .env
LLM_MODEL=zhipu_proxyllm
PROXY_SERVER_URL={your_service_url}
ZHIPU_MODEL_VERSION={version}
ZHIPU_PROXY_API_KEY={your-zhipu-sk}
```
  </TabItem>

  <TabItem value="erniebot" label="文心一言" default>

Download embedding model

```bash
cd GPT-DB
mkdir models and cd models

# embedding model
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese
or
git clone https://huggingface.co/moka-ai/m3e-large
```

Configure the proxy and modify LLM_MODEL, MODEL_VERSION, API_KEY and API_SECRET in the `.env`file

```bash
# .env
LLM_MODEL=wenxin_proxyllm
WEN_XIN_MODEL_VERSION={version} # ERNIE-Bot or ERNIE-Bot-turbo
WEN_XIN_API_KEY={your-wenxin-sk}
WEN_XIN_API_SECRET={your-wenxin-sct}
```
  </TabItem>
  <TabItem value="yi" label="Yi">
  Install dependencies

Yi's API is compatible with OpenAI's API, so you can use the same dependencies as OpenAI's API.

```bash
pip install  -e ".[openai]"
```

Download embedding model

```shell
cd GPT-DB
mkdir models and cd models
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese
```

Configure the proxy and modify LLM_MODEL, YI_API_BASE and YI_API_KEY in the `.env`file

```shell
# .env
LLM_MODEL=yi_proxyllm
YI_MODEL_VERSION=yi-34b-chat-0205
YI_API_BASE=https://api.lingyiwanwu.com/v1
YI_API_KEY={your-yi-api-key}
```
  </TabItem>
</Tabs>


:::info note

⚠️ Be careful not to overwrite the contents of the `.env` configuration file
:::


### Local model
<Tabs
  defaultValue="vicuna"
  values={[
    {label: 'ChatGLM', value: 'chatglm'},
    {label: 'Vicuna', value: 'vicuna'},
    {label: 'Baichuan', value: 'baichuan'},
  ]}>
  <TabItem value="vicuna" label="vicuna">

##### Hardware requirements description
| Model    		    |   Quantize   |  VRAM Size   	| 
|------------------ |--------------|----------------|
|Vicuna-7b-1.5     	|   4-bit      |  8GB         	|
|Vicuna-7b-1.5 		|   8-bit	   |  12GB        	|
|Vicuna-13b-v1.5   	|   4-bit      |  12GB        	|
|Vicuna-13b-v1.5    |   8-bit      |  24GB          |

##### Download LLM

```bash
cd GPT-DB
mkdir models and cd models

# embedding model
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese
or
git clone https://huggingface.co/moka-ai/m3e-large

# llm model, if you use openai or Azure or tongyi llm api service, you don't need to download llm model
git clone https://huggingface.co/lmsys/vicuna-13b-v1.5

```
##### Environment variable configuration, configure the LLM_MODEL parameter in the `.env` file
```bash
# .env
LLM_MODEL=vicuna-13b-v1.5
```
  </TabItem>

  <TabItem value="baichuan" label="baichuan">

##### Hardware requirements description
| Model    		    |   Quantize   |  VRAM Size   	| 
|------------------ |--------------|----------------|
|Baichuan-7b     	|   4-bit      |  8GB         	|
|Baichuan-7b  		|   8-bit	   |  12GB          |
|Baichuan-13b     	|   4-bit      |  12GB        	|
|Baichuan-13b       |   8-bit      |  20GB          |

##### Download LLM


```bash
cd GPT-DB
mkdir models and cd models

# embedding model
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese
or
git clone https://huggingface.co/moka-ai/m3e-large

# llm model
git clone https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat
or
git clone https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat

```
##### Environment variable configuration, configure the LLM_MODEL parameter in the `.env` file
```bash
# .env
LLM_MODEL=baichuan2-13b
```
  </TabItem>

  <TabItem value="chatglm" label="chatglm">

##### Hardware requirements description
| Model    		        | Quantize    | VRAM Size   	  | 
|--------------------|-------------|----------------|
| glm-4-9b-chat     	 | Not support | 16GB         	 |
| ChatGLM-6b     	   | 4-bit       | 7GB         	  |
| ChatGLM-6b 	  	    | 8-bit	      | 9GB            |
| ChatGLM-6b       	 | FP16        | 14GB        	  |


##### Download LLM

```bash
cd GPT-DB
mkdir models and cd models

# embedding model
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese
or
git clone https://huggingface.co/moka-ai/m3e-large

# llm model
git clone https://huggingface.co/THUDM/glm-4-9b-chat

```
##### Environment variable configuration, configure the LLM_MODEL parameter in the `.env` file
```bash
# .env
LLM_MODEL=glm-4-9b-chat
```
  </TabItem>

</Tabs>


### llama.cpp(CPU)
:::info note
⚠️ llama.cpp can be run on Mac M1 or Mac M2
:::

GPT-DB also supports the lower-cost inference framework llama.cpp, which can be used through llama-cpp-python.


#### Document preparation
Before using llama.cpp, you first need to prepare the model file in gguf format. There are two ways to obtain it. You can choose one method to obtain the corresponding file.

:::tip
Method 1: Download the converted model
:::

If you want to use [Vicuna-13b-v1.5](https://huggingface.co/lmsys/vicuna-13b-v1.5), you can download the converted file [TheBloke/vicuna-13B-v1.5-GGUF](https://huggingface.co/TheBloke/vicuna-13B-v1.5-GGUF), only this one file is needed. Download the file and put it in the model path. You need to rename the model to: `ggml-model-q4_0.gguf`.
```bash
wget https://huggingface.co/TheBloke/vicuna-13B-v1.5-GGUF/resolve/main/vicuna-13b-v1.5.Q4_K_M.gguf -O models/ggml-model-q4_0.gguf
```

:::tip
Method 2: Convert files yourself
:::
During use, you can also convert the model file yourself according to the instructions in [llama.cpp#prepare-data–run](https://github.com/ggerganov/llama.cpp#prepare-data--run), and place the converted file in the models directory and name it `ggml-model-q4_0.gguf`.


#### Install dependencies
llama.cpp is an optional installation item in GPT-DB. You can install it with the following command.

```bash
pip install -e ".[llama_cpp]"
```

#### Modify configuration file
Modify the `.env` file to use llama.cpp, and then you can start the service by running the [command](../quickstart.md)


#### More descriptions

| environment variables               | default value    |       description     |
|-------------------------------------|------------------|-----------------------|
| `llama_cpp_prompt_template`         | None             |        Prompt template now supports `zero_shot, vicuna_v1.1,alpaca,llama-2,baichuan-chat,internlm-chat`. If it is None, the model Prompt template can be automatically obtained according to the model path.    |  
|          `llama_cpp_model_path`     |   None           |               model path        | 
|          `llama_cpp_n_gpu_layers`   | 1000000000         |    How many network layers to transfer to the GPU, set this to 1000000000 to transfer all layers to the GPU. If your GPU is low on memory, you can set a lower number, for example: 10.                   | 
|           `llama_cpp_n_threads`     |     None     |      The number of threads to use. If None, the number of threads will be determined automatically.                 | 
|            `llama_cpp_n_batch`      |     512     |         The maximum number of prompt tokens to be batched together when calling llama_eval              | 
|             `llama_cpp_n_gqa`       |     None     |          For the llama-2 70B model, Grouped-query attention must be 8.             | 
|           `llama_cpp_rms_norm_eps`  |     5e-06     |      For the llama-2 model, 5e-6 is a good value.                 | 
|          `llama_cpp_cache_capacity` |     None     |    Maximum model cache size. For example: 2000MiB, 2GiB                   | 
|            `llama_cpp_prefer_cpu`   |     False     |    If a GPU is available, the GPU will be used first by default unless prefer_cpu=False is configured.              | 

## Install GPT-DB Application Database
<Tabs
  defaultValue="sqlite"
  values={[
    {label: 'SQLite', value: 'sqlite'},
    {label: 'MySQL', value: 'mysql'},
  ]}>
<TabItem value="sqlite" label="sqlite">

:::tip NOTE

You do not need to separately create the database tables related to the GPT-DB application in SQLite; 
they will be created automatically for you by default.

:::


 </TabItem>
<TabItem value="mysql" label="MySQL">

:::warning NOTE

After version 0.4.7, we removed the automatic generation of MySQL database Schema for safety.

:::

1. Frist, execute MySQL script to create database and tables.

```bash
$ mysql -h127.0.0.1 -uroot -p{your_password} < ./assets/schema/gptdb.sql
```

2. Second, set GPT-DB MySQL database settings in `.env` file.

```bash
LOCAL_DB_TYPE=mysql
LOCAL_DB_USER= {your username}
LOCAL_DB_PASSWORD={your_password}
LOCAL_DB_HOST=127.0.0.1
LOCAL_DB_PORT=3306
```

 </TabItem>
</Tabs>


## Test data (optional)
The GPT-DB project has a part of test data built-in by default, which can be loaded into the local database for testing through the following command
- **Linux**

```bash
bash ./scripts/examples/load_examples.sh

```
- **Windows**

```bash
.\scripts\examples\load_examples.bat
```

## Run service
The GPT-DB service is packaged into a server, and the entire GPT-DB service can be started through the following command.
```bash
python gptdb/app/gptdb_server.py
```
:::info NOTE
### Run service

If you are running version v0.4.3 or earlier, please start with the following command:

```bash
python pilot/server/gptdb_server.py
```
### Run GPT-DB with command `gptdb`

If you want to run GPT-DB with the command `gptdb`:

```bash
gptdb start webserver
```

:::

## Visit website
Open the browser and visit [`http://localhost:5670`](http://localhost:5670)