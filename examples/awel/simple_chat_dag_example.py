"""AWEL: Simple chat dag example

    GPT-DB will automatically load and execute the current file after startup.

    Example:

    .. code-block:: shell

        GPTDB_SERVER="http://127.0.0.1:5555"
        MODEL="gpt-3.5-turbo"
        curl -X POST $GPTDB_SERVER/api/v1/awel/trigger/examples/simple_chat \
        -H "Content-Type: application/json" -d '{
            "model": "'"$MODEL"'",
            "user_input": "hello"
        }'
"""

from gptdb._private.pydantic import BaseModel, Field
from gptdb.core import ModelMessage, ModelRequest
from gptdb.core.awel import DAG, HttpTrigger, MapOperator
from gptdb.model.operators import LLMOperator


class TriggerReqBody(BaseModel):
    model: str = Field(..., description="Model name")
    user_input: str = Field(..., description="User input")


class RequestHandleOperator(MapOperator[TriggerReqBody, ModelRequest]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def map(self, input_value: TriggerReqBody) -> ModelRequest:
        messages = [ModelMessage.build_human_message(input_value.user_input)]
        print(f"Receive input value: {input_value}")
        return ModelRequest.build_request(input_value.model, messages)


with DAG("gptdb_awel_simple_dag_example", tags={"label": "example"}) as dag:
    # Receive http request and trigger dag to run.
    trigger = HttpTrigger(
        "/examples/simple_chat", methods="POST", request_body=TriggerReqBody
    )
    request_handle_task = RequestHandleOperator()
    llm_task = LLMOperator(task_name="llm_task")
    model_parse_task = MapOperator(lambda out: out.to_dict())
    trigger >> request_handle_task >> llm_task >> model_parse_task


if __name__ == "__main__":
    if dag.leaf_nodes[0].dev_mode:
        # Development mode, you can run the dag locally for debugging.
        from gptdb.core.awel import setup_dev_environment

        setup_dev_environment([dag], port=5555)
    else:
        # Production mode, GPT-DB will automatically load and execute the current file after startup.
        pass
