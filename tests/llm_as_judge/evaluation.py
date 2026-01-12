import os
import uuid

from application.agents.deep_research_agent.research_agent import DeepResearchAgent
from langsmith import Client

from tests.llm_as_judge.dataset import messages_should_continue, messages_should_stop

langsmith_client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))

# Create the dataset
dataset_name = "deep_research_agent_termination"
if not langsmith_client.has_dataset(dataset_name=dataset_name):

    # Create the dataset
    dataset = langsmith_client.create_dataset(
        dataset_name=dataset_name,
        description="A dataset that evaluates whether a researcher can accurately decide to continue calling tools, or to stop.",
    )

    # Create the examples
    langsmith_client.create_examples(
        dataset_id=dataset.id,
        examples=[
            {
                "inputs": {"researcher_messages": messages_should_continue},
                "outputs": {"next_step": "continue"},
            },
            {
                "inputs": {"researcher_messages": messages_should_stop},
                "outputs": {"next_step": "stop"},
            },
        ],
    )


def evaluate_next_step(outputs: dict, reference_outputs: dict):
    tool_calls = outputs["researcher_messages"][-1].tool_calls
    made_tool_call = len(tool_calls) > 0
    return {
        "key": "correct_next_step",
        "score": made_tool_call == (reference_outputs["next_step"] == "continue"),
    }


def target_func(inputs: dict):
    deep_research_agent = DeepResearchAgent()
    config = {"configurable": {"thread_id": uuid.uuid4()}}
    result = deep_research_agent.nodes["llm_call"].invoke(inputs, config=config)
    return result


langsmith_client.evaluate(
    target_func,
    data=dataset_name,
    evaluators=[evaluate_next_step],
    experiment_prefix="Researcher Iteration",
)
