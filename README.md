# 📊 AI Agent Report Maker - Deploy Edition

**AI-Agent-Report-Maker-Deploy** is a streamlined application built to generate financial reports based on user prompts. Leveraging Gradio or Streamlit for an interactive front-end, this project utilizes an AI-powered agent that processes date ranges, retrieves relevant data, and generates detailed PDF reports. The application is ideal for quick deployment, providing users with a simple and efficient way to gain insights from transaction data.

---

## 📜 Project Overview

This deploy-ready version focuses on the core functionality of the AI agent from the original **AI-Agent-Report-Maker** project. Users can input a natural language prompt (e.g., "Create a report for 2021 for client 1556"), and the agent will extract dates, process data, and generate a financial summary in PDF format.

### Key Features
- **AI-Powered Date Extraction**: Automatically identifies and extracts relevant date ranges from prompts.
- **Data Processing and Summaries**: Provides earnings, expenses, and cash flow summaries over specified periods.
- **PDF Report Generation**: Outputs user-friendly reports for easy analysis and insights.

---

## 📂 Project Structure

```plaintext
project/
│
├── app.py                   # Main application file for Gradio or Streamlit
├── requirements.txt         # Dependencies
├── README.md                # Project description and setup instructions
├── config.py                # Configuration (paths, settings)
│
├── data/
│   ├── data_functions.py    # Data processing functions
│   └── sample_transactions_data.csv      # Sample dataset only for clients 126 and 1556, dates 2010-01-01 to 2019-10-31
│
├── reports/                 # Output folder for generated reports
│
├── utils/
│   ├── pdf_generator.py     # PDF generation functions
│   ├── date_extraction.py   # Date extraction logic
│   └── ai_agent.py          # Main AI agent logic
```