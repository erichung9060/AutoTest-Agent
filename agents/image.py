from langchain.schema import HumanMessage
from agents.Agent import Agent
from functools import lru_cache


class ImageSummarizeAgent(Agent):
    def __init__(self, model="gpt-4o-mini"):
        super().__init__(model)
        print(f"Initialized ImageSummarizeAgent with model: {self.model}")
        
    @lru_cache(maxsize=128)
    def summarize(self, base64_image: str) -> str:
        try:            
            message = HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": "Please describe the content of the image in as much detail as possible. Include all visible elements, text, layout, colors, and other details."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            )
            
            response = self.llm.invoke([message])
            summary = response.content
            print(f"Image summary generated: {len(summary)} characters")
            return summary
            
        except Exception as e:
            print(f"Error summarizing image: {e}")
            return f"Image processing failed: {str(e)}"