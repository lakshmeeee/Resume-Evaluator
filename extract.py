from pydantic import BaseModel, Field

from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent
from langchain.agents import AgentType


#input
class DocInput(BaseModel):
    question: str = Field()


# initialization
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
tools = []
text_splitter = CharacterTextSplitter(
    chunk_size = 800, # Maximum size of chunks to return
    chunk_overlap  = 0, # Overlap in characters between chunk
)
embeddings = OpenAIEmbeddings()


def tool_creation(name,path):
    try:
        docs = text_splitter.split_text(path)
        retriever = FAISS.from_texts(docs, embeddings).as_retriever()
    except TypeError:
        docs = text_splitter.split_documents(path)
        retriever = FAISS.from_documents(docs, embeddings).as_retriever()

    tools.append(
        Tool(
            args_schema=DocInput,
            name=name,
            description=f"useful when you want to answer questions about {name}",
            func=RetrievalQA.from_chain_type(llm=llm, retriever=retriever),
        )
    )


def call_agent(inp):
    agent = initialize_agent(
        agent=AgentType.OPENAI_FUNCTIONS,
        tools=tools,
        llm=llm,
        verbose=True,
    )

    agent({"input": inp})