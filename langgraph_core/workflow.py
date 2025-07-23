from langgraph.graph import StateGraph, END
from .nodes import run_test_node, judge_node, reset_env_node
from .WorkflowState import WorkflowState


def route_after_judge(state: WorkflowState) -> str:
    if state["status"] == "retry":
        return "restart"
    else:
        return "end"

def create_workflow():
    workflow = StateGraph(WorkflowState)
    
    workflow.add_node("run_test", run_test_node)
    workflow.add_node("judge", judge_node)
    workflow.add_node("restart", reset_env_node)
    
    workflow.add_edge("run_test", "judge")
    
    workflow.add_conditional_edges(
        "judge",
        route_after_judge,
        {
            "restart": "restart",
            "end": END
        }
    )
    
    workflow.add_edge("restart", "run_test")
    
    workflow.set_entry_point("run_test")
    
    return workflow.compile()

class LangGraphTestRunner:
    def __init__(self):
        self.workflow = create_workflow()
    
    def run_test_workflow(self, task_title: str, task_description: str) -> dict:
        initial_state = WorkflowState(
            task_title=task_title,
            task_description=task_description,
            test_result="",
            retry_count=0,
            status="pending",
            passed=False
        )
        
        result = self.workflow.invoke(initial_state)
        
        return result
    
    def generate_workflow_diagram(self, output_path: str = "workflow_diagram.png"):
        diagram = self.workflow.get_graph().draw_mermaid_png()
        with open(output_path, "wb") as f:
            f.write(diagram)
        
        print(f"Workflow diagram saved to: {output_path}")
        return output_path