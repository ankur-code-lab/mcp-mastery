# 🤖 MCP Mastery

A hands-on learning workspace for building and integrating **Model Context Protocol (MCP)** servers with LLM-powered agentic clients. This repository progresses from simple MCP server examples all the way to real-world use cases like weather querying, news fetching, and an AI-powered job search assistant.

---

## 📁 Project Structure

```
MCP-Mastery/
├── 1_Basic_MCP_Server/              # Foundational MCP server examples
│   ├── demo/                        # Minimal add/subtract tools demo
│   ├── weather/                     # Real-time weather MCP server
│   ├── mcp_use_framework/           # Agentic client using mcp-use library
│   ├── mcp_use_framework_config_file/  # Multi-server agent via mcp.json config
│   └── Integrating_with_Antigravity/   # Integration examples with Antigravity
│
├── 2_MCPServer_Data_Analysis/       # MCP server for data analysis tasks
│   ├── data/                        # Sample datasets (e.g., support tickets Excel file)
│   └── prompts/                     # Prompt templates for data analysis
│
├── 3_Tools_Resources_Prompts/       # Advanced MCP: Tools + Resources + Prompts
│   └── job_search/                  # Full-featured AI job search assistant
│       ├── server.py                # MCP server (tools, resources, prompts)
│       ├── client.py                # Agentic client
│       ├── mcp.json                 # Server configuration
│       ├── jobs/                    # Fetched and saved job data
│       └── resume/                  # Place your resume.pdf here
│
├── .env                             # API keys (never commit this!)
├── pyproject.toml                   # Project metadata and dependencies
├── requirements.txt                 # Pip-compatible dependency list
├── uv.lock                          # Locked dependency versions (via uv)
└── main.py                          # Project entry point
```

---

## ✨ Modules Overview

### 1️⃣ Basic MCP Server (`1_Basic_MCP_Server/`)

Introductory examples to understand how MCP servers work.

| Sub-project | Description |
|---|---|
| `demo/` | Hello-world MCP server exposing `add` and `subtract` tools |
| `weather/` | Async MCP server that fetches real-time weather via [WeatherAPI.com](https://www.weatherapi.com) |
| `mcp_use_framework/` | LLM agent using the `mcp-use` library to talk to an MCP server over stdio |
| `mcp_use_framework_config_file/` | Multi-server agentic client configured via `mcp.json`; connects to weather + news servers simultaneously |
| `Integrating_with_Antigravity/` | Examples integrating MCP servers with the Antigravity AI assistant |

---

### 2️⃣ MCP Server for Data Analysis (`2_MCPServer_Data_Analysis/`)

An MCP server designed for data analysis workflows. Includes sample data (support ticket Excel files) and prompt templates to drive LLM-powered analysis.

---

### 3️⃣ Tools, Resources & Prompts — Job Search (`3_Tools_Resources_Prompts/job_search/`)

A fully-featured AI job search assistant demonstrating MCP's **Tools**, **Resources**, and **Prompts** primitives together.

| MCP Primitive | Name | Description |
|---|---|---|
| 🔧 Tool | `search_jobs` | Searches live jobs via [JSearch (RapidAPI)](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch) |
| 🔧 Tool | `save_job` | Saves a selected job (with salary info) to local storage |
| 📦 Resource | `resume://default` | Extracts and exposes your resume PDF as text |
| 📦 Resource | `jobs://saved` | Returns a markdown listing of all saved jobs |
| 💬 Prompt | `analyze_job_market` | Generates structured job market analysis instructions |
| 💬 Prompt | `personalized_job_recommender` | Recommends jobs by matching them against your resume |
| 💬 Prompt | `create_match_report` | Creates a resume-vs-job match report |

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---|---|---|
| `fastmcp` | 3.1.0 | Building MCP servers quickly |
| `mcp-use` | 1.6.0 | Connecting LLM agents to MCP servers |
| `langchain-groq` | 1.1.2 | LLM integration (Groq-hosted models) |
| `pypdf` | 6.7.5 | Reading PDF resumes |
| `python-dotenv` | 1.2.2 | Loading environment variables from `.env` |
| `requests` | 2.32.5 | Making HTTP API calls |

---

## ⚙️ Setup Guide

### Prerequisites

- Python **3.11+**
- [`uv`](https://docs.astral.sh/uv/) package manager (recommended) **or** `pip`

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/<your-username>/MCP-Mastery.git
cd MCP-Mastery
```

---

### Step 2 — Install Dependencies

**Using `uv` (recommended):**
```bash
uv sync
```

**Using `pip`:**
```bash
pip install -r requirements.txt
```

---

### Step 3 — Configure API Keys

Create a `.env` file in the project root (copy the template below):

```bash
cp .env.example .env   # if .env.example exists, otherwise create manually
```

Open `.env` and fill in your keys:

```env
# Required for the weather server
WEATHERAPI_KEY=your_weatherapi_key_here

# Required for the job search server (via RapidAPI)
RAPIDAPI_KEY=your_rapidapi_key_here
RAPIDAPI_HOST=jsearch.p.rapidapi.com

# Required for the agentic clients (LLM)
GROQ_API_KEY=your_groq_api_key_here
```

> **Where to get the keys:**
> - `WEATHERAPI_KEY` → [weatherapi.com](https://www.weatherapi.com) (free tier available)
> - `RAPIDAPI_KEY` → [rapidapi.com](https://rapidapi.com) → subscribe to the [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
> - `GROQ_API_KEY` → [console.groq.com](https://console.groq.com) (free tier available)

---

### Step 4 — (Optional) Add Your Resume

For the job search assistant, place your resume as a PDF at:

```
3_Tools_Resources_Prompts/job_search/resume/resume.pdf
```

---

## 🚀 Running the Projects

### Demo Server (add/subtract tools)

```bash
# Terminal 1 — Start the server
cd 1_Basic_MCP_Server/demo
python server.py

# Terminal 2 — Run the client
python client.py
```

---

### Weather MCP Server

```bash
cd 1_Basic_MCP_Server/weather
python server.py
```

---

### Multi-Server Agentic Client (Weather + News)

```bash
cd 1_Basic_MCP_Server/mcp_use_framework_config_file
python agentic_client_advanced.py
# Then type your query at the prompt, e.g.:
# > What is the weather in Mumbai?
# > What's the latest tech news?
```

---

### Job Search Assistant

```bash
# Start the MCP server
cd 3_Tools_Resources_Prompts/job_search
python server.py

# In a new terminal, run the client
python client.py
```

---

## 🔒 Security Notes

- **Never commit your `.env` file** — it is listed in `.gitignore`
- The `Resources/` folder is also ignored (may contain sensitive data)
- Use `.env.example` (with dummy values) to document required variables for collaborators

---

## 📚 Learning Path

Follow the modules in order for the best learning experience:

```
1_Basic_MCP_Server/demo          →  Understand MCP basics (tools, stdio transport)
1_Basic_MCP_Server/weather       →  Build a real API-integrated MCP server
1_Basic_MCP_Server/mcp_use_framework  →  Connect an LLM agent to your MCP server
1_Basic_MCP_Server/mcp_use_framework_config_file  →  Scale to multiple servers via config
2_MCPServer_Data_Analysis        →  Apply MCP to data analysis workflows
3_Tools_Resources_Prompts/job_search  →  Master Tools + Resources + Prompts together
```

---

## 📄 License

This project is for educational purposes. Feel free to fork and build on it!
