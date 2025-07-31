from typing import TypedDict, Optional


class WorkflowState(TypedDict):
    task_title: str
    task_description: str
    run_result: str
    judge_result: str
    retry_count: int
    retry: bool
    passed: bool
    screenshot_path: Optional[str]