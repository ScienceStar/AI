from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

api_key = os.getenv("OPENAI_API_KEY")
chat = ChatOpenAI(
    api_key=api_key,   # ← 换成你的
    model="gpt-4.1-mini",             # 你之前 curl 能跑的模型
    temperature=0.7,
)

resp = chat.invoke([
    HumanMessage(content="你好，简单自我介绍一下")
])

print(api_key)

print(resp.content)