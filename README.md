# ExpenseTracker Application in Python

A modern, full-featured **Personal Finance & Expense Tracker Application** built with Python. Features an interactive **Web Dashboard** with real-time visual analytics (Chart.js), category budget limits, dark-mode glassmorphism UI, CSV/JSON import & export, and a comprehensive **CLI tool**.

---

##  Features

- **Transaction Management**: Add, edit, delete, and list expenses and incomes with date, payment method, category, and notes.
- **SQLite Data Persistence**: Zero external DB setup required. Automatically creates `expenses.db`.
- **Category Budget Tracking**: Set monthly limits per category with progress bars and visual alert badges.
- **Visual Analytics**: Interactive Category Expense Pie Chart and Monthly Income vs Expense Trend Bar Chart.
- **Filtering & Search**: Instantly filter by type, category, or keyword search across title/notes.
- **Data Export & Import**: One-click export and import for CSV and JSON format files.
- **Dual Mode Interface**: Run as a Web Application or as a Command-Line Interface (CLI).

---

## 🚀 Quick Start

### 1. Install Dependencies

Ensure Python 3.8+ is installed on your system.

```bash
pip install -r requirements.txt
```

### 2. Run Web Dashboard

Launch the web app on `http://127.0.0.1:5000`:

```bash
python main.py
```
*(or `python app.py`)*

Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 💻 Command Line Interface (CLI)

You can also manage your finances directly from your terminal!

### Add a New Expense or Income

```bash
python main.py cli add --title "Grocery Shopping" --amount 125.50 --category "Food & Dining" --type Expense
python main.py cli add --title "Monthly Salary" --amount 3500.00 --category "Salary" --type Income
```

### List Transactions

```bash
python main.py cli list
python main.py cli list --category "Food & Dining" --limit 10
```

### View Financial Summary

```bash
python main.py cli summary
```

### View & Set Budget Limits

```bash
python main.py cli budget
python main.py cli budget --set --category "Entertainment" --limit 250.00
```

### Export & Import Data

```bash
# Export
python main.py cli export --format csv --output my_expenses.csv
python main.py cli export --format json --output my_expenses.json

# Import
python main.py cli import --format csv --input my_expenses.csv
```

### Delete a Transaction

```bash
python main.py cli delete 1
```

---

## 📁 Project Structure

```
ExpenseTracker/
├── main.py                # Main entry point (Web dashboard or CLI mode)
├── tracker.py             # Business logic & ExpenseTracker class
├── database.py            # SQLite database schema and connection manager
├── cli.py                 # Terminal CLI command handlers
├── app.py                 # Flask web server & REST API endpoints
├── requirements.txt       # Dependencies
├── README.md              # Application documentation
├── static/
│   ├── css/
│   │   └── style.css      # Dark glassmorphism CSS design system
│   └── js/
│       └── app.js         # Frontend controller, REST API fetch, Chart.js integrations
└── templates/
    └── index.html         # Dashboard HTML layout and modals
```

---

## 🎨 UI Preview

- **Glassmorphism Design**: High contrast dark theme with vibrant emerald (income) and rose (expense) accents.
- **Dynamic Charts**: Chart.js integration for category breakdown & monthly trends.
- **Filter Controls**: Fast client-side and server-side search and category filtering.
