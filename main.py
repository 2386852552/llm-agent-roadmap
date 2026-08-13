from dotenv import load_dotenv
import os
from rich import print

load_dotenv()

model_id = os.getenv("LLM_MODEL_ID")
api_key = os.getenv("LLM_API_KEY")
base_url = os.getenv("LLM_BASE_URL")

print("[bold green]环境加载成功！[/bold green]")

print(f"Model: {model_id}")

if api_key:
    print(f"API Key 已读取: {api_key[:8]}...")
else:
    print("未检测到 API Key")

print(f"Base URL: {base_url}")