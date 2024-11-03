# tools.py
import re
from fpdf import FPDF

def preprocess_input(input_text):

    # List of phrases to remove from the input
    unwanted_phrases = [
                            "create a pdf report", 
                            "generate a PDF", 
                            "make a PDF", 
                            "pdf", 
                            "produce a pdf report", 
                            "make a report", 
                            "create a report", 
                            "generate a report", 
                            "produce a report", 
                            "report in pdf format", 
                            "pdf format", 
                            "make a summary", 
                            "create summary", 
                            "pdf summary", 
                            "generate summary", 
                            "make a detailed report", 
                            "generate a detailed report", 
                            "produce a summary", 
                            "summarize in pdf"
                        ]

    for phrase in unwanted_phrases:
        # Create a regex pattern that ignores case
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        # Replace the phrase with an empty string
        input_text = pattern.sub("", input_text)
    # Remove extra whitespace
    return input_text.strip()

def extract_dates_and_client_id(chain, input_text):
    """
    Extracts the start and end dates, as well as the client ID, from the given input text.

    Parameters
    ----------
    chain : ChatOllama
        The Langchain AI model to use for text processing.
    input_text : str
        The input text to extract the dates and client ID from.

    Returns
    -------
    tuple
        A tuple of (start_date, end_date, client_id), where start_date and end_date are strings in the format "YYYY-MM-DD",
        and client_id is an integer. If any value is not found, it will be returned as None.
    """
    # Preprocess the input text
    cleaned_input = preprocess_input(input_text)
    
    if not cleaned_input:
        return None, None, None  # Return None for all if input is invalid

    response = chain.invoke({"input_prompt": cleaned_input})
    
    # Use regex to find dates and client ID
    start_date_match = re.search(r"START_DATE:\s*(\d{4}-\d{2}-\d{2})", response.content)
    end_date_match = re.search(r"END_DATE:\s*(\d{4}-\d{2}-\d{2})", response.content)
    client_id_match = re.search(r"CLIENT_ID:\s*(\d+)", response.content)
    
    # Extract values if found
    start_date = start_date_match.group(1) if start_date_match else None
    end_date = end_date_match.group(1) if end_date_match else None
    client_id = int(client_id_match.group(1)) if client_id_match else None
    
    return start_date, end_date, client_id  # Return dates and client ID as a tuple

class CustomPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Client Report", align="C", ln=True)
        self.ln(10)

    def add_table(self, data_frame, title):
        # Table title
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.ln(5)
        
        # Column headers
        self.set_font("Arial", "B", 10)
        col_width = self.epw / len(data_frame.columns)  # Column width is evenly distributed
        for col_name in data_frame.columns:
            self.cell(col_width, 10, col_name, border=1, align="C")
        self.ln()
        
        # Table rows
        self.set_font("Arial", "", 8)
        for _, row in data_frame.iterrows():
            for item in row:
                self.cell(col_width, 10, str(item), border=1, align="C")
            self.ln()
        self.ln(10)  # Space after table