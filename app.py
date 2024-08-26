
from llama_index.core.agent.legacy.react.base import ReActAgent

from llama_index.llms.openai import OpenAI
from tools.CRUD_tool import all_tools


llm = OpenAI(model="gpt-3.5-turbo")
agent = ReActAgent.from_tools(all_tools, llm=llm, verbose=True)

response = agent.chat("What are all the states")
