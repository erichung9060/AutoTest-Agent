from typing import TypedDict


class WorkflowState(TypedDict):
    task_title: str
    task_description: str
    run_result: str
    judge_result: str
    retry_count: int
    status: str
    passed: bool