from typing import TypedDict,List,Annotated
import os
import requests
import arxiv
import operator
import psycopg
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_chroma import Chroma
from langgraph.types import interrupt,Command
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
load_dotenv()

llm=ChatGroq(
    temperature=0,
    groq_api_key="",
    model_name= "llama-3.3-70b-versatile"
)
embeddings=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

class PaperState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    topic:str
    query:str
    answer:str
    context:str
    chunks:list
    papers:list
    selected_papers: list[int]
    summary:str
    gaps:str
    review:str
    route:str

def router_node(state: PaperState):

    prompt = f"""
    You are a router.

    If the user is asking about research papers, AI, machine learning,
    literature review, summarization, research gaps or wants papers,
    respond with only:

    research

    Otherwise respond with only:

    chat

    User Query:
    {state["query"]}
    """

    response = llm.invoke(prompt).content.strip().lower()

    return {"route": response}
    print(response)

def search_papers_node(state: PaperState):

    search = arxiv.Search(
        query=state["query"],
        max_results=5,
        sort_by=arxiv.SortCriterion.Relevance
    )

    client = arxiv.Client()
    papers = list(client.results(search))

    paper_list = [
        {
            "title": paper.title,
            "paper_id": paper.get_short_id(),
            "pdf_url": paper.pdf_url,
            "authors": [a.name for a in paper.authors]
        }
        for paper in papers
    ]

    human_response = interrupt(
        {
            "message": "Select the paper numbers you want to analyze.",
            "papers": [
                {
                    "index": i + 1,
                    "title": p["title"],
                    "authors": ", ".join(p["authors"])
                }
                for i, p in enumerate(paper_list)
            ]
        }
    )

    return {
        "papers": paper_list,
        "selected_papers": human_response["selected_papers"]
    }
def retrieve_node(state:PaperState):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    all_chunks=[]
    selected = state["selected_papers"]

    papers = [
        state["papers"][i - 1]
        for i in selected
    ]

    for paper in papers:
        paper_id = paper["paper_id"]

        safe_filename = (
            paper_id
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
        )

        pdf_path = f"{safe_filename}.pdf"
        response = requests.get(paper["pdf_url"])
        with open(pdf_path,"wb") as f:
            f.write(response.content)
        loader=PyMuPDFLoader(pdf_path)
        docs=loader.load()
        os.remove(pdf_path)
        chunks=splitter.split_documents(docs)
        for chunk in chunks:
            chunk.metadata["title"] = paper["title"]
            chunk.metadata["paper_id"] = paper["paper_id"]
            chunk.metadata["authors"] = ", ".join(paper["authors"])
        all_chunks.extend(chunks)
    vectorstore=Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        collection_name="research_papers"
    )
    retriever=vectorstore.as_retriever(
        search_kwargs={"k":4}
    )
    retrieved_docs=retriever.invoke(state["query"])
    context="\n\n".join(doc.page_content for doc in retrieved_docs)
    return{
        "context":context,
        "chunks":all_chunks
    }
def generate_node(state:PaperState):
    prompt = f"""
    You are an AI Research Assistant.

    Context:

    {state["context"]}

    Question:

    {state["query"]}

    Answer in simple English.
    """
    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }
def summary_node(state:PaperState):
    prompt1=f"""You are a person that writes the best and concise summary of a context provided to you {state["context"]}"""
    response1=llm.invoke(prompt1)
    return{
        "summary":response1.content
    }
def gap_detection_node(state:PaperState):
    prompt2=f"""You are an AI Assistant and your work is to find the gaps in the research papers {state["context"]} find the relevant gaps in the research paper and generate a report of it  """
    response2=llm.invoke(prompt2)
    return{
        "gaps":response2.content
    }
def literature_review(state:PaperState):
    prompt3=f"""You are an AI assistant your work it to write literature review of research paper topic given by the user while analyzing similar research papers related to it {state["context"]}"""
    response3=llm.invoke(prompt3)
    return{
        "review":response3.content
    }
def chat_node(state: PaperState):
    response = llm.invoke(state["messages"])
    return {
        "answer": response.content,
        "messages": [AIMessage(content=response.content)]

    }
def route(state: PaperState):

    route = state["route"].strip().lower()

    if "research" in route:
        return "search"

    return "chat"
builder = StateGraph(PaperState)
builder.add_node("router", router_node)
builder.add_node("chat", chat_node)
builder.add_node("search", search_papers_node)
builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)
builder.add_node("summarise",summary_node)
builder.add_node("gapDetection",gap_detection_node)
builder.add_node("literature_review",literature_review)
builder.add_edge(START,"router")
builder.add_conditional_edges(
    "router",
    route,
    {
        "search": "search",
        "chat": "chat"
    }
)
builder.add_edge("search", "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", "summarise")
builder.add_edge("summarise","gapDetection")
builder.add_edge("gapDetection","literature_review")
builder.add_edge("literature_review", END)
builder.add_edge("chat", END)
DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"
conn = psycopg.connect(DB_URI)

checkpointer = PostgresSaver(conn)

checkpointer.setup()

app = builder.compile(
    checkpointer=checkpointer
)
config = {
         "configurable": {
         "thread_id": "test1236"}
 }


if __name__ == "__main__":
        query=input("Enter your query:")

        result = app.invoke(
            {
                "messages": [HumanMessage(content=query)],
                "query": query,
                "topic": query,
                "selected_papers": [1, 2]  # temporary
            },
            config=config,
        )
        selection = input("Enter paper numbers (e.g. 1,3): ")

        selected = [int(x.strip()) for x in selection.split(",")]

        result = app.invoke(
            Command(
                resume={
                    "selected_papers": selected
                }
            ),
            config=config,
        )
        print(result["answer"])
        print(result["summary"])
        print(result["gaps"])
        print(result["review"])

