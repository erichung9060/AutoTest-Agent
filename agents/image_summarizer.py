import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage


class ImageSummarizer:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_base=os.getenv("OPENAI_API_BASE"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model_name="claude-4-sonnet",
            temperature=0.0
        )
    
    def summarize(self, base64_image: str) -> str:
        try:
            print("Summarizing image with Claude-4-Sonnet...")
            
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
            return f"圖片處理失敗: {str(e)}"