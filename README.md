<div align="center">

# 🧠 AI Research Assistant

### An Intelligent Multi-Agent Research Assistant powered by LangGraph, RAG, LLMs & Human-in-the-Loop

<p>

Research papers • Literature Review • Research Gap Detection • AI Chat Assistant

</p>

</div>

---

# 📌 Overview

AI Research Assistant is an intelligent agentic system that automates the complete research workflow.

Instead of simply answering questions, the assistant:

- Searches the latest research papers from arXiv
- Lets users choose relevant papers (Human-in-the-Loop)
- Downloads and processes PDFs
- Creates embeddings using HuggingFace
- Retrieves relevant chunks using RAG
- Generates research answers
- Produces concise summaries
- Detects research gaps
- Generates literature reviews
- Supports conversational AI with short-term memory

---

# 🚀 Features

## 🔍 Research Paper Search

- Searches the latest papers directly from arXiv
- Finds papers based on semantic user queries
- Returns the most relevant publications

---

## 👨‍💻 Human-in-the-Loop (HITL)

Instead of automatically analyzing every paper,

the assistant:

- Displays retrieved papers
- Lets the user choose which papers to analyze
- Continues the workflow only after user approval

This keeps the research process interactive and accurate.

---

## 📄 Automatic PDF Processing

After selection, the assistant:

- Downloads research PDFs
- Extracts text using PyMuPDF
- Splits documents into semantic chunks
- Adds metadata like:

- Paper title
- Authors
- Paper ID

---

## 🧠 Retrieval Augmented Generation (RAG)

The assistant uses Retrieval Augmented Generation to reduce hallucinations.

Workflow:

PDFs

↓

Chunking

↓

Embeddings

↓

Vector Database (ChromaDB)

↓

Retriever

↓

LLM

Only relevant paper content is sent to the LLM.

---

## 🤖 AI Research Assistant

Generates:

- Accurate answers
- Context-aware explanations
- Easy-to-understand research insights

---

## 📚 Literature Review Generator

Automatically writes structured literature reviews by analyzing selected papers.

Useful for:

- Thesis writing
- Research proposals
- Survey papers

---

## 🔬 Research Gap Detection

Analyzes selected papers to identify:

- Existing limitations
- Open challenges
- Future research directions

---

## 📝 Automatic Paper Summarization

Produces concise summaries highlighting:

- Main objective
- Methodology
- Results
- Contributions

---

## 💬 Intelligent Chat Mode

The assistant is capable of normal conversations.

It can answer:

- AI questions
- Programming questions
- General queries

without invoking the research workflow.

---

## 🧭 Intelligent Query Routing

A routing agent automatically decides whether a query should go to:

- Research Workflow

OR

- Normal AI Chat

making the system efficient.

---

## 🧠 Short-Term Memory

Uses PostgreSQL Checkpointer with LangGraph to maintain conversation state.

The assistant remembers:

- Previous messages
- Workflow state
- Current research session

within the same thread.

---

## ⚡ LangGraph Multi-Agent Workflow

The workflow consists of multiple specialized agents.

```
START
   │
   ▼
Router
   │
 ┌───────┐
 │       │
 ▼       ▼
Chat   Research Search
            │
            ▼
     Human Approval
            │
            ▼
      Retrieve PDFs
            │
            ▼
      Generate Answer
            │
            ▼
        Summarize
            │
            ▼
     Gap Detection
            │
            ▼
 Literature Review
            │
            ▼
           END
```

---

# 🏗️ Tech Stack

| Category | Technologies |
|-----------|-------------|
| Framework | LangGraph |
| LLM | Groq (Llama 3.3 70B) |
| Embeddings | HuggingFace MiniLM |
| Vector Store | ChromaDB |
| PDF Loader | PyMuPDF |
| Paper Search | arXiv API |
| Memory | PostgreSQL Checkpointer |
| Backend | Python |
| Frontend | Streamlit |
| Chunking | Recursive Character Text Splitter |

---

# 📂 Project Structure

```text
AI-Research-Assistant/

│

├── main.py

├── frontend.py

├── requirements.txt

├── README.md

├── .env

│

├── Vector Database

│

└── PostgreSQL Checkpointer
```

---

# ⚙️ Workflow

```text
User Query

↓

Router Agent

↓

Research Query?

↓

Search arXiv

↓

Display Papers

↓

Human Selects Papers

↓

Download PDFs

↓

Extract Text

↓

Chunk Documents

↓

Generate Embeddings

↓

Store in ChromaDB

↓

Retrieve Relevant Context

↓

LLM

↓

Answer

↓

Summary

↓

Research Gaps

↓

Literature Review
```

---

# 🎯 Applications

- Academic Research
- Literature Review Automation
- Research Gap Analysis
- AI Research Assistance
- Student Projects
- Thesis Writing
- Survey Paper Generation
- Research Proposal Preparation

---

# 💡 Future Enhancements

- Multi-paper comparison
- Citation generation (APA, IEEE)
- PDF report export
- Research trend visualization
- Multi-agent debate system
- Long-term memory
- Web search integration
- Cross-paper citation graph
- Semantic search across saved papers
- Voice-based research assistant

---

# 📈 Key Highlights

✅ Multi-Agent Architecture

✅ Retrieval Augmented Generation (RAG)

✅ Human-in-the-Loop

✅ Short-Term Memory

✅ LangGraph Workflow

✅ PostgreSQL Checkpointing

✅ Intelligent Query Router

✅ Research Gap Detection

✅ Literature Review Generation

✅ AI Chat Assistant

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a star!

Built with ❤️ using LangGraph, Groq, HuggingFace and ChromaDB.

</div>
