
import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GOOGLE_API_KEY is not set")

from langchain.agents import create_agent

from langchain.messages import HumanMessage

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="google_genai:gemini-flash-lite-latest",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

prompt = HumanMessage(input("Input: "))

result = agent.invoke(
    {"messages": [prompt]}
)
print(result["messages"][-1].text)

# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
# )
# print(result["messages"][-1].content_blocks)


# def get_response(prompt: str) -> str:
#     return prompt

# def main():
#     while True:
#         try:
#             prompt = input("Input: ")
#             if prompt == "exit": break
#             response = get_response(prompt)
#         except EOFError:
#             break
#         print(response)

# if __name__ == "__main__":
#     main()

