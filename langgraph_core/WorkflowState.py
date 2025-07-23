from typing import TypedDict


class WorkflowState(TypedDict):
    task_title: str
    task_description: str
    test_result: str
    retry_count: int
    status: str
    passed: bool