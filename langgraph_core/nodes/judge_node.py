from agents import JudgeAgent
from ..WorkflowState import WorkflowState


def judge_node(state: WorkflowState) -> WorkflowState:
    print("Running judge agent")
    
    title = state["task_title"]
    description = state["task_description"]
    run_result = state["run_result"]

    judge_agent = JudgeAgent()
    
    passed, retry, judge_result, screenshot_path = judge_agent.run(title, description, run_result)
    # TODO: try catch in judge_test_result

    if retry and state["retry_count"] < 2:
        state["retry"] = True
    else:
        judge_agent.save_report(title, description, run_result, judge_result, passed, screenshot_path)
        state["passed"] = passed
        state["judge_result"] = judge_result
        state["screenshot_path"] = screenshot_path

    return state