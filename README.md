# 🤖 AI IT Helpdesk Agent

### Intelligent IT Support Using Agentic AI, RAG, and Model Context Protocol (MCP)

An AI-powered IT Helpdesk Agent designed to assist users with technical issues through knowledge retrieval, automated diagnostics, system information collection, and support ticket management.

The project combines **Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and Model Context Protocol (MCP)** to build an intelligent IT support assistant.

---

## 📌 Project Overview

Traditional IT support often requires users to manually troubleshoot problems or wait for technical assistance.

The AI IT Helpdesk Agent aims to simplify this process by using AI to understand user queries, retrieve relevant troubleshooting information, select diagnostic tools, and assist with support ticket management.

The system supports common IT troubleshooting scenarios, including internet connectivity issues, computer performance problems, software errors, and potential security incidents.

## ✨ Key Features

* 🤖 **AI-Powered Troubleshooting** — Uses an LLM to analyze IT problems and generate troubleshooting guidance.
* 📚 **Retrieval-Augmented Generation (RAG)** — Retrieves relevant information from an IT support knowledge base.
* 🔌 **Model Context Protocol (MCP)** — Connects the AI workflow to external diagnostic and support tools.
* 🌐 **Internet Connectivity Checks** — Checks whether an internet connection is available.
* 💻 **System Information** — Collects basic operating system and processor information.
* 🎫 **Support Ticket Management** — Creates and retrieves IT support tickets.
* 🔐 **Security Incident Handling** — Detects potential security-related requests and initiates a high-priority ticket workflow.
* 🖥️ **Streamlit Interface** — Provides a chat-style interface for interacting with the helpdesk.

> Note: The current Streamlit interface is a preliminary frontend. Its chat input and message display are implemented, but the AI backend still needs to be connected to make the complete interface functional.

---

## 🛠️ Technology Stack

| Technology                   | Purpose                                           |
| ---------------------------- | ------------------------------------------------- |
| Python                       | Core programming language                         |
| LangChain                    | LLM integration and agent workflows               |
| LangGraph                    | Agent framework and workflow support              |
| Ollama                       | Runs language models locally                      |
| Qwen 2.5 3B                  | Language model used by the current implementation |
| Nomic Embed Text             | Generates embeddings for knowledge retrieval      |
| ChromaDB                     | Stores and retrieves vector embeddings            |
| RAG                          | Retrieves relevant IT support information         |
| Model Context Protocol (MCP) | Exposes diagnostic and ticket-management tools    |
| Streamlit                    | Web-based user interface                          |
| Git and GitHub               | Version control and project hosting               |

---

## 🏗️ System Architecture

The project follows a modular architecture.

```text
              ┌────────────────────────┐
              │         User           │
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   Streamlit Interface  │
              │        (app.py)        │
              └────────────┬───────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │     AI Agent Layer     │
              │   LangChain + Ollama
```
