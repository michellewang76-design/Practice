# 📈 Affiliate Payout & Performance Dashboard

👉 [**Click here to view the project mindmap online**](https://raw.githack.com/michellewang76-design/Practice/main/Affiliates_Analysis/docs/mindmap.html)

## 📖 Project Overview
The **Affiliate Payout & Performance Dashboard** is a robust, automated web application built with Streamlit. It is designed to streamline the ingestion, merging, and visualization of monthly affiliate payout records.

Going beyond standard data visualization, this project integrates a **Local Persistent Data Warehouse** and an **AI Business Analyst**. By leveraging Google's Gemini LLM alongside a ChromaDB-powered RAG (Retrieval-Augmented Generation) architecture, the system automatically translates complex data trends into professional, actionable business commentaries and allows for interactive historical data querying.

---

## ✨ Core Features

### 1. 🗄️ Persistent Local Data Warehouse
* **Automated Storage:** Uploaded `.csv` files are permanently saved to a local physical directory (`uploaded_monthly_data/`).
* **Smart Deduplication:** The system automatically scans file names upon upload. If a file already exists, it intelligently skips it to prevent data duplication.
* **Auto-Merging:** Upon launch, the system recursively reads all historical CSV files in the storage folder and seamlessly concatenates them into a master dynamic dataset.

### 2. 📊 Dynamic & Interactive Visualizations
* **Intelligent Time Filtering:** Dropdowns automatically default to the latest available Year and Month within the dataset.
* **Comprehensive Metrics:** Interactive charts (built with Plotly) tracking Payout Status, Affiliate Criteria, Bank Processing, and Paid Affiliate Trends.
* **Organic FTT Analysis:** Overlaid bar charts analyzing the ratio of Organic Affiliates' FTT against the overall numbers.

### 3. 🤖 AI-Powered Business Insights & RAG Chat
* **Interactive AI Chat Assistant:** A toggleable, persistent sidebar chat interface that allows users to naturally query historical knowledge base documents (e.g., past campaign details, strategy memos) without disrupting the main dashboard view.
* **Contextual Awareness:** The `DashboardContextBuilder` translates real-time active dashboard data into an LLM-readable format.
* **Knowledge Retrieval:** Utilizes a local `ChromaDB` vector database to retrieve historical strategic priorities and operational guidelines.
* **Automated Reporting:** Calls the `gemini-flash-latest` model to synthesize the data and knowledge base into a comprehensive, markdown-formatted business commentary and interactive responses.

---

## 📁 Project Directory Structure

Based on the current environment, here is the functional breakdown of the project files:

```text
Affiliates_Analysis/
│
├── app.py                  # Main Streamlit application entry point (UI, Routing & Layout)
├── chat_sidebar.py         # Renders the interactive AI chat sidebar UI with scrollable container
├── llm_service.py          # Handles Gemini API configuration and text generation
├── context_builder.py      # Extracts DataFrame logic into prompt context
├── knowledge_base.py       # Manages ChromaDB vector embeddings and search
├── merge.py                # Utility scripts for specific data processing
│
├── uploaded_monthly_data/  # Local persistent directory for uploaded CSV files
├── chroma_db/              # Local vector database storage for RAG documents
│
├── .env                    # (Ignored in Git) Stores sensitive API keys
└── requirements.txt        # Project dependencies (Streamlit, Pandas, etc.)
│
├── docs/                   # save PRD, retro & mindmap

🚀 Installation & Setup Guide
Step 1: Prepare the Environment
It is highly recommended to use a virtual environment to avoid dependency conflicts.

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Activate the virtual environment (Mac/Linux)
source .venv/bin/activate

Step 2: Install Dependencies
Ensure you are in the project root directory and run:

pip install -r requirements.txt

Step 3: Configure Environment Variables
Create a file named .env in the root directory. Add your Google Gemini API key to this file:

GOOGLE_API_KEY=your_api_key_here

💻 How to Use the Dashboard
Launch the Application:
Open your terminal, ensure the virtual environment is active, and run the main application file:

streamlit run app.py

Data Upload & Management:

Navigate to the "Data Upload" section on the left sidebar.

Drag and drop your monthly .csv files. The system will save new files to uploaded_monthly_data/ and automatically merge them.

Upload historical policy/campaign documents (.txt, .docx) into the Knowledge Base section to power the AI.

Explore Data:

Use the Choose a Year and Choose a Month dropdowns (which default to the latest period).

Navigate through the tabs to view Summaries, Breakdowns, Bank Processing, and Trend Analyses.

You can download the complete merged historical dataset directly from the sidebar.

💬 Use the AI Assistant (RAG Chat):

Toggle the "✨ Show/Hide AI Assistant" switch at the top of the main dashboard to dynamically expand or collapse the side panel.

Ask specific questions in the chat box (e.g., "What campaigns did we have in 2020?") and the AI will retrieve answers from your uploaded knowledge base.

Generate AI Insights Report:

Scroll to the bottom of the main dashboard.

Click the "Generate AI Insights" button.

Wait a few seconds while the AI cross-references your current data with the vector database to produce a customized financial report.

📋 Expected Data Format (CSV)
For the dashboard to process data correctly, the uploaded CSV files should ideally contain the following columns (case-sensitive):

Year

Month

Affiliate_ID

Status (e.g., Paid, Pending, Rejected)

Approved_Fee

Bank

Criteria

Organic (String identifier for organic traffic)

Ftt_Num (Integer representing FTT count)

Built with ❤️ using Python, Streamlit, and Google Gemini.