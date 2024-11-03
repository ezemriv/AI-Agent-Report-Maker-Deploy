import os
import pandas as pd
from datetime import datetime

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from utils.data_functions import (
    earnings_and_expenses,
    expenses_summary,
    cash_flow_summary,
)

from utils.tools import extract_dates_and_client_id, CustomPDF

from config import (
    REPORTS_FOLDER,
    EARNINGS_EXPENSES_PLOT_PATH,
    EXPENSES_SUMMARY_PLOT_PATH,
    MODEL_NAME,
    MODEL_TEMPERATURE,
)

def run_agent(df: pd.DataFrame, input_text: str) -> dict:
    """
    Main function to extract information, process data, and generate a report.
    """
    # Set up the model and prompt for date and client ID extraction
    model = ChatOllama(model=MODEL_NAME, temperature=MODEL_TEMPERATURE)
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            (
                "You are a helpful assistant that extracts information from the given text."
                "Extract client id number as CLIENT_ID."
                "Extract START and END dates."
                "For each date found, output it in the format START_DATE and END_DATE."
                "Dates should be formatted as 'YYYY-MM-DD'."
                "If no day is provided in each date, assume the day is 01."
                "If there is reference to only one month, assume the start day is 01 and the end day is the last day of the month."
                "Return client id and only 2 dates. Do not include any additional text."
            ),
        ),
        ("human", "{input_prompt}"),
    ])
    chain = prompt | model

    # Extract client ID and dates
    start_date, end_date, client_id = extract_dates_and_client_id(chain, input_text)
    print("Extracted Dates:", start_date, end_date)
    print("Extracted Client ID:", client_id)

    # Process data for reporting
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    earnings_and_expenses_df = earnings_and_expenses(df, client_id, start_date, end_date)
    expenses_df = expenses_summary(df, client_id, start_date, end_date)
    cash_flow_df = cash_flow_summary(df, client_id, start_date, end_date)
    
    # Check if all dataframes are empty and set report flag
    create_report = not (earnings_and_expenses_df.empty and expenses_df.empty and cash_flow_df.empty)
    if not create_report:
        print("No data available for the specified client or date range. Skipping report generation.")
        return {"create_report": False}

    # Generate PDF
    pdf = CustomPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Report for Client {client_id} | Date Range: {start_date} to {end_date}", ln=True, align="C")
    pdf.ln(10)

    # Add tables and images to PDF
    pdf.add_table(earnings_and_expenses_df, "Earnings and Expenses Summary")
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Earnings and Expenses Plot", ln=True)
    pdf.image(EARNINGS_EXPENSES_PLOT_PATH, x=10, w=180)
    pdf.ln(10)
    pdf.add_table(expenses_df, "Expenses Summary by Merchant Category")
    pdf.cell(0, 10, "Expenses Summary Plot", ln=True)
    pdf.image(EXPENSES_SUMMARY_PLOT_PATH, x=10, w=180)
    pdf.ln(10)
    pdf.add_table(cash_flow_df, "Cash Flow Summary")

    # Save PDF
    os.makedirs(REPORTS_FOLDER, exist_ok=True)
    pdf_filename = os.path.join(REPORTS_FOLDER, f"client_{client_id}_report.pdf")
    pdf.output(pdf_filename)
    print(f"PDF report saved at {pdf_filename}")

    return {
        "start_date": start_date,
        "end_date": end_date,
        "client_id": client_id,
        "pdf_path": pdf_filename,
        "create_report": True,
    }
