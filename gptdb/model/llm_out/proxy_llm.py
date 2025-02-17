#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from gptdb.model.proxy.llms.baichuan import baichuan_generate_stream
from gptdb.model.proxy.llms.bard import bard_generate_stream
from gptdb.model.proxy.llms.chatgpt import chatgpt_generate_stream
from gptdb.model.proxy.llms.claude import claude_generate_stream
from gptdb.model.proxy.llms.gemini import gemini_generate_stream
from gptdb.model.proxy.llms.proxy_model import ProxyModel
from gptdb.model.proxy.llms.spark import spark_generate_stream
from gptdb.model.proxy.llms.tongyi import tongyi_generate_stream
from gptdb.model.proxy.llms.wenxin import wenxin_generate_stream
from gptdb.model.proxy.llms.zhipu import zhipu_generate_stream

# This has been moved to gptdb/model/adapter/proxy_adapter.py
# def proxyllm_generate_stream(
#     model: ProxyModel, tokenizer, params, device, context_len=2048
# ):
#     generator_mapping = {
#         "proxyllm": chatgpt_generate_stream,
#         "chatgpt_proxyllm": chatgpt_generate_stream,
#         "bard_proxyllm": bard_generate_stream,
#         "claude_proxyllm": claude_generate_stream,
#         # "gpt4_proxyllm": gpt4_generate_stream, move to chatgpt_generate_stream
#         "wenxin_proxyllm": wenxin_generate_stream,
#         "tongyi_proxyllm": tongyi_generate_stream,
#         "zhipu_proxyllm": zhipu_generate_stream,
#         "gemini_proxyllm": gemini_generate_stream,
#         "bc_proxyllm": baichuan_generate_stream,
#         "spark_proxyllm": spark_generate_stream,
#     }
#     model_params = model.get_params()
#     model_name = model_params.model_name
#     default_error_message = f"{model_name} LLM is not supported"
#     generator_function = generator_mapping.get(
#         model_name, lambda *args: [default_error_message]
#     )
#
#     yield from generator_function(model, tokenizer, params, device, context_len)
