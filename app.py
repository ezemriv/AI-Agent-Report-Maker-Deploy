import gradio as gr
import pandas as pd
from utils.agent import run_agent
from config import DATA_PATH

def generate_report(input_text):
    """Generate report with improved error handling and input validation"""
    if not input_text or not input_text.strip():
        return "Please provide a valid input text.", None
    
    try:
        # Get the data
        df = pd.read_pickle(DATA_PATH)
        
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
            status_message = f"✅ Report generated successfully for client {client_id}\nPeriod: {start_date} to {end_date}"
            
            return status_message, pdf_path
        else:
            return "❌ No data available for the specified client or date range.", None
            
    except Exception as e:
        error_message = f"❌ Error generating report: {str(e)}"
        print(error_message)  # For logging
        return error_message, None

def create_gradio_interface():
    """Create and configure the Gradio interface"""
    with gr.Blocks(theme=gr.themes.Soft()) as app:
        gr.Markdown(
            """
            # 📊 AI Agent Report Generator
            Generate custom PDF reports for your clients with natural language instructions.
            """
        )
        
        with gr.Row():
            input_text = gr.Textbox(
                label="Enter your request",
                placeholder="Example: Generate a pdf report for client 126 from 2010-01-01 to 2014-02-01",
                lines=2
            )

        with gr.Row():
            generate_button = gr.Button("🚀 Generate Report", variant="primary")

        with gr.Row():
            status = gr.Markdown(label="Status")
            pdf_output = gr.File(label="Generated Report")

        # Example queries
        gr.Examples(
            examples=[
                ["Generate a pdf report for client 126 from 2010-01-01 to 2014-02-01"],
                ["Create a pdf report for client 1556 for the first month of 2011"],
            ],
            inputs=input_text
        )

        generate_button.click(
            fn=generate_report,
            inputs=input_text,
            outputs=[status, pdf_output]
        )
        
        return app

if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch(
        server_name="0.0.0.0",
        share=True,
        debug=True
    )