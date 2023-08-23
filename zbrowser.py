
from typing import List, Union

# Langchain imports
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser, initialize_agent, AgentType
from langchain.prompts import BaseChatPromptTemplate, ChatPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
# LLM wrapper
from langchain.chat_models import ChatOpenAI
# Conversational memory
from langchain.memory import ConversationBufferWindowMemory


from prompt import CustomPromptTemplate
from output_parser import CustomOutputParser

from tools.browser import CustomBrowser


API_KEY = "<YOUR OPEN AI KEY>"
SERPAPI_KEY = "c27b9a1445b6e6b6ac2bed6dc5e8fcfab53a2df21eaabb58efadb29a242ca398"

search = SerpAPIWrapper(serpapi_api_key=SERPAPI_KEY)
# Set up the base template
template_with_history = """You are zchatbot, a professional chatbot for Zscaler who provides informative answers to users. You have access to the following tools:

{tools}

Use the tool only when question is about zscaler , otherwise just answer like a normal chatbot.
Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Remember to give detailed, informative answers

Previous conversation history:
{history}

New question: {input}
{agent_scratchpad}"""

zbrowser = CustomBrowser()

expanded_tools = [
    Tool(
        name=zbrowser.name,
        func=zbrowser.run,
        description=zbrowser.description
    )
]

# expanded_tools = [
#     Tool(
#         name = "Search",
#         func=search.run,
#         description="useful for when you need to answer questions about current events"
#     ),
#     Tool(
#         name = 'Knowledge Base',
#         func=podcast_retriever.run,
#         description="Useful for general questions about how to do things and for details on interesting topics. Input should be a fully formed question."
#     )
# ]


llm = ChatOpenAI(temperature=0, openai_api_key=API_KEY) 

# Re-initialize the agent with our new list of tools
prompt_with_history = CustomPromptTemplate(
    template=template_with_history,
    tools=expanded_tools,
    input_variables=["input", "intermediate_steps", "history"]
)

output_parser = CustomOutputParser()

llm_chain = LLMChain(llm=llm, prompt=prompt_with_history)
multi_tool_names = [tool.name for tool in expanded_tools]
multi_tool_agent = LLMSingleActionAgent(
    llm_chain=llm_chain, 
    output_parser=output_parser,
    stop=["\nObservation:"], 
    allowed_tools=multi_tool_names,
    handle_parsing_errors = True
)
# search = SerpAPIWrapper()
# llm_math_chain = LLMMathChain(llm=llm, verbose=True)
# tools = [
#     Tool.from_function(
#         func=search.run,
#         name="Search",
#         description="useful for when you need to answer questions about current events"
#         # coroutine= ... <- you can specify an async method if desired as well
#     ),
# ]
multi_tool_memory = ConversationBufferWindowMemory(k=2)
multi_tool_executor = AgentExecutor.from_agent_and_tools(agent=multi_tool_agent, tools=expanded_tools, verbose=True, memory=multi_tool_memory)
multi_tool_executor.run("What are Zscaler employee benefits 2023 US")
# multi_tool_executor.run("Who is Joe Biden")

# class Zscaler_browser(BaseModel):

# mrkl = initialize_agent(tools=expanded_tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors = True)

# # mrkl.run("What are zscaler employee benefits 2023 US")
# mrkl.run("Who is Joe Biden")