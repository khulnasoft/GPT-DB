---
sidebar_position: 0
---

# Overview

🤖 **GPT-DB is an open source AI native data app development framework with AWEL(Agentic Workflow Expression Language) and agents**. 

The purpose is to build infrastructure in the field of large models, through the development of multiple technical capabilities such as multi-model management (SMMF), Text2SQL effect optimization, RAG framework and optimization, Multi-Agents framework collaboration, AWEL (agent workflow orchestration), etc. Which makes large model applications with data simpler and more convenient.


🚀 **In the Data 3.0 era, based on models and databases, enterprises and developers can build their own bespoke applications with less code.**

<p align="left">
  <img src={'/img/gptdb.png'} width="680px" />
</p>


## Features

##### Private Domain Q&A & Data Processing & RAG
- Supports custom construction of knowledge bases through methods such as built-in, multi-file format uploads, and plugin-based web scraping. Enables unified vector storage and retrieval of massive structured and unstructured data.

##### Multi-Data Source & GBI(Generative Business Intelligence)
- Supports interaction between natural language and various data sources such as Excel, databases, and data warehouses. Also supports analysis reporting. 

##### SMMF(Service-oriented Multi-model Management Framework)
- Supports a wide range of models, including dozens of large language models such as open-source models and API proxies. Examples include LLaMA/LLaMA2, Baichuan, ChatGLM, ERNIE Bot, Qwen, Spark, etc.

##### Automated Fine-tuning
- Supports Text2SQL fine-tuning. Provides a lightweight automatic fine-tuning framework around the fields of LLM and Text2SQL, supporting methods such as LoRA/QLoRA/P-turning, making Text2SQL fine-tuning as convenient as a production line.
##### Data-Driven Multi-Agents & Plugins
- Supports executing tasks through custom plugins and natively supports the Auto-GPT plugin model. [Agents protocol](https://agentprotocol.ai/) follows the Agent Protocol standard.

##### Privacy and Security
- Supports data privacy protection. Ensures data privacy and security through techniques such as privatizing large language models and proxy de-identification.

## Getting Started

 - [Quickstart](./quickstart.md)
 - [Installation](./installation)


## Terminology

| terminology          | Description                                                   |
|----------------------|---------------------------------------------------------------|
| <center> `GPT-DB`       </center>| DataBase Generative Pre-trained Transformer, an open source framework around databases and large language models |
|<center> `Data App` </center> | an intelligent Data application built on GPT-DB. |
| <center> `Text2SQL/NL2SQL`  </center>  | Text to SQL uses large language model capabilities to generate SQL statements based on natural language, or provide explanations based on SQL statements |
| <center>`KBQA`   </center>  | Knowledge-Based Q&A system |
| <center>`GBI`            </center>  | Generative Business Intelligence, based on large language models and data analysis, provides business intelligence analysis and decision-making through dialogue |
| <center>`LLMOps`   </center>  | A large language model operation framework that provides a standard end-to-end workflow for training, tuning, deploying, and monitoring LLM to accelerate application deployment of generated AI models |
|<center> `Embedding`  </center>   | Methods to convert text, audio, video and other materials into vectors |
|<center> `RAG`   </center>| Retrieval Augmented Generation |
|<center> `AWEL` </center> | Agentic Workflow Expression Language, intelligent Workflow Expression Language 
|<center> `AWEL Flow` </center> | workflow orchestration using the intelligent workflow Expression Language 
|<center> `SMMF` </center> | a service-oriented multi-model management framework. 

## Use Cases

- [Use Cases](./use_cases.md)

## Modules

#### [SMMF](./modules/smmf.md)
Service-oriented Multi-model Management Framework 

#### [Retrieval](./modules/rag.md)
Multi-Knowledge Enhanced Retrieval-Augmented Generation Framework

#### [Agents](./modules/agent.md)
Data Driven Multi-Agents

#### [Fine-tuning](./modules/fine_tuning.md)
Fine-tuning module for Text2SQL/Text2DSL


## More

- [Connections](./modules/connections.md) 
Connect various data sources

- [Obvervablity](./application/advanced_tutorial/observability.md)
Observing & monitoring

- [Evaluation](./modules/eval.md)
Evaluate framework performance and accuracy

## Community
If you encounter any problems during the process, you can submit an [issue](https://github.com/khulnasoft/GPT-DB/issues) and communicate with us.

We welcome [discussions](https://github.com/orgs/khulnasoft/discussions) in the community

