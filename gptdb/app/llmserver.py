#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from gptdb._private.config import Config
from gptdb.configs.model_config import EMBEDDING_MODEL_CONFIG, LLM_MODEL_CONFIG
from gptdb.model.cluster import run_worker_manager

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_PATH)


CFG = Config()

model_path = LLM_MODEL_CONFIG.get(CFG.LLM_MODEL)

if __name__ == "__main__":
    """run llm server including controller, manager worker
    If you use gunicorn as a process manager, initialize_app can be invoke in `on_starting` hook.
    """
    run_worker_manager(
        model_name=CFG.LLM_MODEL,
        model_path=model_path,
        standalone=True,
        port=CFG.MODEL_PORT,
        embedding_model_name=CFG.EMBEDDING_MODEL,
        embedding_model_path=EMBEDDING_MODEL_CONFIG[CFG.EMBEDDING_MODEL],
    )
