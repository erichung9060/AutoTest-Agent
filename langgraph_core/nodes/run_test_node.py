from agents import RunTestAgent
from ..WorkflowState import WorkflowState


def run_test_node(state: WorkflowState) -> WorkflowState:
    print(f"Running test agent")
    
    title = state["task_title"]
    description = state["task_description"]

    run_test_agent = RunTestAgent()
    
    run_result = run_test_agent.run(title, description)
    # TODO: try catch in run


    state["status"] = "test_completed"
    state["run_result"] = run_result
    
    return state