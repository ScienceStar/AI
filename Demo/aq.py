from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def main():
    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0.7
    )

    resp = llm.invoke([
        HumanMessage(content="用一句话解释什么是 JVM")
    ])

    print(resp.content)

if __name__ == "__main__":
    main()