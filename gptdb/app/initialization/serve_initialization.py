from gptdb._private.config import Config
from gptdb.component import SystemApp


def register_serve_apps(system_app: SystemApp, cfg: Config, webserver_port: int):
    """Register serve apps"""
    system_app.config.set("gptdb.app.global.language", cfg.LANGUAGE)
    if cfg.API_KEYS:
        system_app.config.set("gptdb.app.global.api_keys", cfg.API_KEYS)
    if cfg.ENCRYPT_KEY:
        system_app.config.set("gptdb.app.global.encrypt_key", cfg.ENCRYPT_KEY)

    # ################################ Prompt Serve Register Begin ######################################
    from gptdb.serve.prompt.serve import (
        SERVE_CONFIG_KEY_PREFIX as PROMPT_SERVE_CONFIG_KEY_PREFIX,
    )
    from gptdb.serve.prompt.serve import Serve as PromptServe

    # Replace old prompt serve
    # Set config
    system_app.config.set(f"{PROMPT_SERVE_CONFIG_KEY_PREFIX}default_user", "gptdb")
    system_app.config.set(f"{PROMPT_SERVE_CONFIG_KEY_PREFIX}default_sys_code", "gptdb")
    # Register serve app
    system_app.register(PromptServe, api_prefix="/prompt")
    # ################################ Prompt Serve Register End ########################################

    # ################################ Conversation Serve Register Begin ######################################
    from gptdb.serve.conversation.serve import (
        SERVE_CONFIG_KEY_PREFIX as CONVERSATION_SERVE_CONFIG_KEY_PREFIX,
    )
    from gptdb.serve.conversation.serve import Serve as ConversationServe

    # Set config
    system_app.config.set(
        f"{CONVERSATION_SERVE_CONFIG_KEY_PREFIX}default_model", cfg.LLM_MODEL
    )
    # Register serve app
    system_app.register(ConversationServe, api_prefix="/api/v1/chat/dialogue")
    # ################################ Conversation Serve Register End ########################################

    # ################################ AWEL Flow Serve Register Begin ######################################
    from gptdb.serve.flow.serve import (
        SERVE_CONFIG_KEY_PREFIX as FLOW_SERVE_CONFIG_KEY_PREFIX,
    )
    from gptdb.serve.flow.serve import Serve as FlowServe

    # Register serve app
    system_app.register(FlowServe)

    # ################################ AWEL Flow Serve Register End ########################################

    # ################################ Rag Serve Register Begin ######################################

    from gptdb.serve.rag.serve import (
        SERVE_CONFIG_KEY_PREFIX as RAG_SERVE_CONFIG_KEY_PREFIX,
    )
    from gptdb.serve.rag.serve import Serve as RagServe

    # Register serve app
    system_app.register(RagServe)

    # ################################ Rag Serve Register End ########################################

    # ################################ Datasource Serve Register Begin ######################################

    from gptdb.serve.datasource.serve import (
        SERVE_CONFIG_KEY_PREFIX as DATASOURCE_SERVE_CONFIG_KEY_PREFIX,
    )
    from gptdb.serve.datasource.serve import Serve as DatasourceServe

    # Register serve app
    system_app.register(DatasourceServe)

    # ################################ Datasource Serve Register End ########################################

    # ################################ Chat Feedback Serve Register End ########################################
    from gptdb.serve.feedback.serve import (
        SERVE_CONFIG_KEY_PREFIX as Feedback_SERVE_CONFIG_KEY_PREFIX,
    )
    from gptdb.serve.feedback.serve import Serve as FeedbackServe

    # Register serve feedback
    system_app.register(FeedbackServe)
    # ################################ Chat Feedback Register End ########################################

    # ################################ GptDbs Register Begin ########################################
    # Register serve gptdbshub
    from gptdb.serve.gptdbs.hub.serve import Serve as GptdbsHubServe

    system_app.register(GptdbsHubServe)
    # Register serve gptdbsmy
    from gptdb.serve.gptdbs.my.serve import Serve as GptdbsMyServe

    system_app.register(GptdbsMyServe)
    # ################################ GptDbs Register End ########################################

    # ################################ File Serve Register Begin ######################################

    from gptdb.configs.model_config import FILE_SERVER_LOCAL_STORAGE_PATH
    from gptdb.serve.file.serve import (
        SERVE_CONFIG_KEY_PREFIX as FILE_SERVE_CONFIG_KEY_PREFIX,
    )
    from gptdb.serve.file.serve import Serve as FileServe

    local_storage_path = (
        cfg.FILE_SERVER_LOCAL_STORAGE_PATH or FILE_SERVER_LOCAL_STORAGE_PATH
    )
    if cfg.WEBSERVER_MULTI_INSTANCE:
        local_storage_path = f"{local_storage_path}_{webserver_port}"
    # Set config
    system_app.config.set(
        f"{FILE_SERVE_CONFIG_KEY_PREFIX}local_storage_path", local_storage_path
    )
    system_app.config.set(
        f"{FILE_SERVE_CONFIG_KEY_PREFIX}file_server_port", webserver_port
    )
    if cfg.FILE_SERVER_HOST:
        system_app.config.set(
            f"{FILE_SERVE_CONFIG_KEY_PREFIX}file_server_host", cfg.FILE_SERVER_HOST
        )
    # Register serve app
    system_app.register(FileServe)

    # ################################ File Serve Register End ########################################

    # ################################ Evaluate Serve Register Begin ##################################
    from gptdb.serve.evaluate.serve import Serve as EvaluateServe

    # Register serve Evaluate
    system_app.register(EvaluateServe)
    # ################################ Evaluate Serve Register End ####################################

    # ################################ Libro Serve Register Begin #####################################
    from gptdb.serve.libro.serve import Serve as LibroServe

    # Register serve libro
    system_app.register(LibroServe)
    # ################################ Libro Serve Register End #######################################
