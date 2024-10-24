---
sidebar_position: 0
---
# Quickstart
GPT-DB supports the installation and use of a variety of open source and closed models. Different models have different requirements for environment and resources. If localized model deployment is required, GPU resources are required for deployment. The API proxy model requires relatively few resources and can be deployed and started on a CPU machine.


:::info note
- Detailed installation and deployment tutorials can be found in [Installation](./installation).
- This page only introduces deployment based on ChatGPT proxy and local glm model.
:::

## Environmental preparation

### Download source code

:::tip
Download GPT-DB
:::



```bash
git clone https://github.com/khulnasoft/GPT-DB.git
```

### Miniconda environment installation

- The default database uses SQLite, so there is no need to install a database in the default startup mode. If you need to use other databases, you can read the [advanced tutorials](./application/advanced_tutorial/rag.md) below. We recommend installing the Python virtual environment through the conda virtual environment. For the installation of Miniconda environment, please refer to the [Miniconda installation tutorial](https://docs.conda.io/projects/miniconda/en/latest/).

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

:::info note

Provide two deployment methods to quickly start experiencing GPT-DB.

:::
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs
  defaultValue="openai"
  values={[
    {label: 'Open AI(Proxy LLM)', value: 'openai'},
    {label: 'glm-4(Local LLM)', value: 'glm-4'},
  ]}>

  <TabItem value="openai" label="openai">

:::info note

⚠️  You need to ensure that git-lfs is installed
```bash
● CentOS installation: yum install git-lfs
● Ubuntu installation: apt-get install git-lfs
● MacOS installation: brew install git-lfs
```
:::

#### Install dependencies

```bash
pip install  -e ".[openai]"
```

#### Download embedding model

```bash
cd GPT-DB
mkdir models and cd models
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese
```

#### Configure the proxy and modify LLM_MODEL, PROXY_API_URL and API_KEY in the `.env`file

```bash
# .env
LLM_MODEL=chatgpt_proxyllm
PROXY_API_KEY={your-openai-sk}
PROXY_SERVER_URL=https://api.openai.com/v1/chat/completions
```
  </TabItem>

  <TabItem value="glm-4" label="glm-4">

#### Hardware requirements description
|  Model    		   | GPU VRAM Size   	 | 
|:--------------:|-------------------|
| glm-4-9b     	 | 16GB        	     |

#### Download LLM

```bash
cd GPT-DB
mkdir models and cd models

# embedding model
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese
# also you can use m3e-large model, you can choose one of them according to your needs
# git clone https://huggingface.co/moka-ai/m3e-large

# LLM model, if you use openai or Azure or tongyi llm api service, you don't need to download llm model
git clone https://huggingface.co/THUDM/glm-4-9b-chat

```
#### Environment variable configuration, configure the LLM_MODEL parameter in the `.env` file
```bash
# .env
LLM_MODEL=glm-4-9b-chat
```
  </TabItem>

</Tabs>


## Test data (optional)
Load default test data into SQLite database
- **Linux**

```bash
bash ./scripts/examples/load_examples.sh
```
- **Windows**

```bash
.\scripts\examples\load_examples.bat
```

## Run service

```bash
python gptdb/app/gptdb_server.py
```

:::info NOTE
### Run old service

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


### (Optional) Run web front-end separately

On the other hand, you can also run the web front-end separately.

```bash
cd web & npm install
cp .env.template .env
// set the API_BASE_URL to your GPT-DB server address, it usually is http://localhost:5670
npm run dev
```
Open the browser and visit [`http://localhost:3000`](http://localhost:3000)






