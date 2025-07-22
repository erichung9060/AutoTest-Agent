from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents import RunTestAgent, JudgeAgent

class WorkflowState(TypedDict):
    task_title: str
    task_description: str
    test_result: str
    retry_count: int
    final_result: str
    status: str

def run_test_node(state: WorkflowState) -> WorkflowState:
    print(f"Running test (attempt {state['retry_count'] + 1})")
    
    run_test_agent = RunTestAgent()
    
    try:
        test_result = run_test_agent.run(
            title=state["task_title"],
            description=state["task_description"]
        )
        
        state["test_result"] = test_result
        state["retry_count"] += 1
        
        # Simple heuristic to determine if test failed
        # You can modify this logic based on your test result format
        if any(keyword in str(test_result).lower() for keyword in ["error", "failed", "exception", "timeout"]):
            state["status"] = "test_failed"
        else:
            state["status"] = "test_passed"
            
    except Exception as e:
        state["test_result"] = f"Test execution error: {str(e)}"
        state["status"] = "test_failed"
        state["retry_count"] += 1
    
    return state

def judge_node(state: WorkflowState) -> WorkflowState:
    print("Judging test results")
    
    judge_agent = JudgeAgent()
    
    try:
        judge_result = judge_agent.judge_test_result(
            title=state["task_title"],
            description=state["task_description"],
            run_result=state["test_result"]
        )
        
        state["final_result"] = judge_result
        state["status"] = "completed"
        
    except Exception as e:
        state["final_result"] = f"Judge error: {str(e)}"
        state["status"] = "judge_error"
    
    return state

def should_retry(state: WorkflowState) -> str:
    if state["status"] == "test_failed" and state["retry_count"] < 2:
        return "retry"
    elif state["status"] == "test_failed" and state["retry_count"] >= 2:
        return "failed_final"
    elif state["status"] == "test_passed":
        return "judge"
    else:
        return "end"

def create_workflow():
    workflow = StateGraph(WorkflowState)
    
    workflow.add_node("run_test", run_test_node)
    workflow.add_node("judge", judge_node)
    
    workflow.add_conditional_edges(
        "run_test",
        should_retry,
        {
            "retry": "run_test",
            "judge": "judge", 
            "failed_final": END,
            "end": END
        }
    )
    
    workflow.add_edge("judge", END)
    
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
            final_result="",
            status="pending"
        )
        
        final_state = self.workflow.invoke(initial_state)
        
        return {
            "task_title": final_state["task_title"],
            "task_description": final_state["task_description"],
            "test_result": final_state["test_result"],
            "retry_count": final_state["retry_count"],
            "final_result": final_state["final_result"],
            "status": final_state["status"]
        }
    
    def generate_workflow_diagram(self, output_path: str = "workflow_diagram.png"):
        try:
            diagram = self.workflow.get_graph().draw_mermaid_png()
            with open(output_path, "wb") as f:
                f.write(diagram)
            
            print(f"Workflow diagram saved to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error generating workflow diagram: {e}")
            return None
