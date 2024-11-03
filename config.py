# config.py

# Define the root directory for the project
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# Paths
REPORTS_FOLDER = os.path.join(ROOT, "reports/")
FIGURES_FOLDER = os.path.join(REPORTS_FOLDER, "figures/")
DATA_FOLDER = os.path.join(ROOT, "data/")

# Data paths
DATA_PATH = os.path.join(DATA_FOLDER, "sample_transactions_data.pkl")
MCC_CODES_PATH = os.path.join(DATA_FOLDER, "mcc_codes.json")

# Plot paths
EARNINGS_EXPENSES_PLOT_PATH = os.path.join(FIGURES_FOLDER, "earnings_and_expenses.png")
EXPENSES_SUMMARY_PLOT_PATH = os.path.join(FIGURES_FOLDER, "expenses_summary.png")

# Model settings
MODEL_NAME = "llama3.2:1b"
MODEL_TEMPERATURE = 0
