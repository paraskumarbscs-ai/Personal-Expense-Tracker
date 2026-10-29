
# Personal Expense Tracker 💰

A Python-based expense tracking dashboard built with Streamlit.

## Features
- Add and categorize expenses
- Save transactions to CSV
- View monthly spending summaries
- Visualize spending with interactive charts
- Filter transactions by category
- Download transactions as CSV

## Technologies
- Python
- Streamlit
- Pandas
- Plotly

## Installation

1. Clone this repository:
   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   cd Personal-Expense-Tracker
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate it on Windows:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Data Storage
Transactions are stored locally in `expenses.csv`.
The CSV file is created automatically when an expense is added.

## Future Improvements
- Monthly budgets and budget alerts
- User authentication
- SQLite database
- Recurring expenses
- Income tracking
