import gradio as gr
import pandas as pd
from utils.agent import run_agent
from config import DATA_PATH

def load_data():
    """Load data with error handling"""
    try:
        return pd.read_pickle(DATA_PATH)
    except Exception as e:
        raise RuntimeError(f"Failed to load data from {DATA_PATH}: {str(e)}")

def generate_report(input_text):
    """Generate report with improved error handling and input validation"""
    if not input_text or not input_text.strip():
        return "Please provide a valid input text.", None
    
    try:
        # Get the data
        df = load_data()
        
        # Run the agent to generate the report
        result = run_agent(df, input_text)
        
        # Check if report generation was successful
        if result.get("create_report"):
            client_id = result.get("client_id")
            start_date = result.get("start_date")
            end_date = result.get("end_date")
            pdf_path = result.get("pdf_path")
            
            if not all([client_id, start_date, end_date, pdf_path]):
                return "Missing required information in the result.", None
            
            # Status message
            status_message = f"Generating report for client {client_id} from {start_date} to {end_date}"
            return status_message, pdf_path
        else:
            return "No data available for the specified client or date range.", None
            
    except Exception as e:
        error_message = f"Error generating report: {str(e)}"
        print(error_message)  # For logging
        return error_message, None

def create_gradio_interface():
    """Create and configure the Gradio interface"""
    with gr.Blocks() as app:
        gr.Markdown("# AI Agent Report Generator")
        
        # Input section
        with gr.Row():
            input_text = gr.Textbox(
                label="Enter your request",
                placeholder="Example: Create a pdf report for client 126 from 2024-01-01 to 2024-02-01",
                scale=3
            )

        # Output section
        with gr.Row():
            status = gr.Textbox(label="Status", interactive=False)
            pdf_viewer = gr.File(label="Generated Report")

        # Control section
        with gr.Row():
            generate_button = gr.Button("Generate Report", variant="primary")

        # Set button action
        generate_button.click(
            fn=generate_report,
            inputs=input_text,
            outputs=[status, pdf_viewer],
            api_name="generate"  # Enable API endpoint
        )
        
        return app

# Launch the Gradio app
if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch(
        server_name="0.0.0.0",  # Allow external connections
        share=True,  # Create a public URL
        debug=True   # Enable debug mode
    )