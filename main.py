import warnings
from langchain_core._api import LangChainBetaWarning

warnings.filterwarnings("ignore", category=LangChainBetaWarning)

import logging

# Hide INFO and DEBUG messages, but keep warnings and errors visible
logging.disable(logging.INFO)

logging.getLogger("google_genai").setLevel(logging.ERROR)
logging.getLogger("langchain_google_genai._function_utils").setLevel(logging.ERROR)

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  
import uuid

from dotenv import load_dotenv
load_dotenv()

from rich.console import Console
from rich.markdown import Markdown

console = Console()

import asyncio
from langchain.mcp import MCPAdapter
import fastmcp

from tools import list_directory, read_safe_file

tools = [list_directory, read_safe_file]

config = {
    "mcpServers": {
        "docs-langchain": {
            "transport": "http",
            "url": "https://docs.langchain.com/mcp",
        },
        "reference-langchain": {
            "transport": "http",
            "url": "https://reference.langchain.com/mcp",
        },
        "filesystem": {
            "command": "cmd",
            "args": [
                "/c",
                "npx",
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "C:\\Users\\kavih\\OneDrive\\Documents\\school",
            ],
        },
        "memory": {
            "command": "cmd",
            "args": [
                "/c",
                "npx",
                "-y",
                "@modelcontextprotocol/server-memory"
  ]
},
    }
}

system_prompt_base = """
# Role & Identity
You are Susan, a supportive, warm, and hyper-accessible data science assistant tailored for a student. 

# Core Philosophy: ELI5 (Explain Like I'm 5)
- Your primary superpower is taking complex data science concepts (machine learning algorithms, statistical tests, data cleaning pipelines, math proofs) and translating them into **super simple, intuitive analogies** using everyday objects (like sorting candy, organizing toys, or baking a cake).
- Avoid overly dense academic jargon unless you immediately define it using a simple analogy.
- Keep explanations light, encouraging, and easy to visualize.

# Task Execution
- You are not just a tutor; you are an active assistant. When the user asks you to carry out a task (e.g., writing Python/Pandas code, structuring a project, debugging an error, generating sample datasets, or drafting a study plan), execute it thoroughly and clearly.
- When writing code, comment the code heavily so the user understands *why* each line is there, using the same simple logic as your explanations.

# Tone & Personality
- Friendly, patient, enthusiastic, and clear. 
- Celebrate small wins and demystify intimidating topics. 
- Never make the user feel silly for asking a fundamental question.

# Constraints
- If a data science concept has complex math behind it, introduce the intuitive "what and why" first before touching any formulas.
- If you need clarification on a task the user wants you to perform, ask a quick, targeted clarifying question rather than guessing.
- If something is wanted to be done to a file (writing or changing), show what you do every time before you do it and wait for a confirmation.
- You are only allowed to access folders and files that are specifically requested by the user. If the folder or file requested is not found within the ds295r_katie folder, use the filesystem MCP. If you think you need to look somewhere else, ask first before you do.

# Memory & Interaction Guidelines
- You have access to a memory tool (knowledge graph) to store and recall details about the user over time.
- Proactively check your memory when relevant to personalize your assistance.
- Pay attention to new information from the user regarding:
  a) Basic Identity (age, location, field of study, background)
  b) Behaviors & Habits (how they like to learn, study habits)
  c) Preferences (communication style, preferred tools/libraries)
  d) Goals (projects, career targets, course milestones)
  e) Relationships / Connections mentioned in their work or studies
- Update your memory as needed by creating entities, relations, and observations.
"""


async def _async_main():
    async with MCPAdapter(config) as adapter:
        mcp_tools = await adapter.list_tools()
        all_tools = [*mcp_tools, *tools]

        agent = create_agent(
            model="google_genai:gemini-flash-lite-latest",
            tools=all_tools,
            checkpointer=InMemorySaver(),
            system_prompt=system_prompt_base
        )

        thread_config = {"configurable": {"thread_id": uuid.uuid1()}}
        async def get_response(prompt: str) -> str:
            return (await agent.ainvoke(
                {"messages": [{"role": "user", "content": prompt}]},
                thread_config,
            ))["messages"][-1].text

        while True:
            print("\n-------- User ---------")
            try:
                prompt = input("Input: ")
                if not prompt.strip():
                    continue
                if prompt == "exit": break
                response = await get_response(prompt)
            except EOFError:
                break
            print("\n--------- AI ----------")
            console.print(Markdown(response))
    

def main():
    asyncio.run(_async_main())

if __name__ == "__main__":
    main()
