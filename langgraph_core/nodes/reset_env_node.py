import subprocess
import time
from ..WorkflowState import WorkflowState


def reset_env_node(state: WorkflowState) -> WorkflowState:
    print("Restarting environment...")
    
    try:
        subprocess.run(["adb", "shell", "input", "keyevent", "KEYCODE_APP_SWITCH"], check=True)
        print("App switcher opened")
        
        time.sleep(2)
        
        subprocess.run(["adb", "shell", "input", "swipe", "540", "1800", "540", "100"], check=True)
        print("App closed")
        
        time.sleep(1)
        
        print("Environment restart completed")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during environment reset: {e}")
    except Exception as e:
        print(f"Unexpected error during restart: {e}")
    
    state["status"] = "pending"
    state["retry_count"] += 1
    return state