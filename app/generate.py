from config import reader
from security import check
from prompt import TRANS_PROMPT
from llama_index.core import PromptTemplate
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI

system_prompt = PromptTemplate(TRANS_PROMPT)

read = reader.ConfigReader()

model_config = read.get_model_config()
api_config = read.get_api_config()

llm = OpenAI(
    model=model_config["name"],
    temperature=model_config["temperature"],
    max_tokens=model_config["max_tokens"],
    api_key=api_config["api_key"],
    timeout=api_config["timeout"]
)
agent = ReActAgent.from_tools(
    tools=[],
    llm=llm,
    system_prompt=system_prompt,
    verbose=True
)
