from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  
import uuid

from dotenv import load_dotenv
load_dotenv()

from rich.console import Console
from rich.markdown import Markdown

console = Console()

from tools import list_directory, read_safe_file


agent = create_agent(
    model="google_genai:gemini-flash-lite-latest",
    tools=[read_safe_file, list_directory],
    checkpointer=InMemorySaver(),
)

thread_config = {"configurable": {"thread_id": uuid.uuid1()}}
def get_response(prompt: str) -> str:
    return agent.invoke(
        {"messages": [{"role": "user", "content": prompt}]},
        thread_config,
    )["messages"][-1].text


def main():
    while True:
        print("\n-------- User ---------")
        try:
            prompt = input("Input: ")
            if prompt == "exit": break
            response = get_response(prompt)
        except EOFError:
            break
        print("\n--------- AI ----------")
        console.print(Markdown(response))
    

if __name__ == "__main__":
    main()