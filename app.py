import gradio as gr
import pandas as pd
from utils.agent import run_agent
from config import DATA_PATH

# Load the sample data
df = pd.read_pickle(DATA_PATH)

def generate_report(input_text):
    # Run the agent to generate the report
    result = run_agent(df, input_text)
    
    # Check if report generation was successful
    if result["create_report"]:
        client_id = result["client_id"]
        start_date = result["start_date"]
        end_date = result["end_date"]
        pdf_path = result["pdf_path"]

        # Status message
        status_message = f"Generating report for client {client_id} from {start_date} to {end_date}"
        return status_message, pdf_path  # Return status message and PDF path
    else:
        return "No data available for the specified client or date range.", None

# Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# AI Agent Report Generator")
    input_text = gr.Textbox(label="Enter client ID and date range")

    # Display status message
    status = gr.Textbox(label="Status", interactive=False)

    # Create PDF output element (can display or download)
    pdf_viewer = gr.File(label="Generated Report")

    # Button to generate the report
    generate_button = gr.Button("Generate Report")

    # Set button action
    generate_button.click(
        fn=generate_report,
        inputs=input_text,
        outputs=[status, pdf_viewer]
    )

# Launch the Gradio app
if __name__ == "__main__":
    app.launch()
