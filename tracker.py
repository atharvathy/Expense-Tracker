import sqlite3
import csv
import json
from datetime import datetime
from database import get_connection, init_db

class ExpenseTracker:
    def __init__(self, db_path="expenses.db"):
        self.db_path = db_path
        init_db(self.db_path)

    # ------------------ TRANSACTIONS CRUD ------------------ #
    def add_transaction(self, title, amount, trans_type, category, date=None, payment_method="Cash", note=""):
        if not title or not title.strip():
            raise ValueError("Title is required.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if trans_type not in ['Expense', 'Income']:
            raise ValueError("Type must be 'Expense' or 'Income'.")
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO transactions (title, amount, type, category, date, payment_method, note)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (title.strip(), float(amount), trans_type, category.strip(), date, payment_method.strip(), note.strip())
        )
        trans_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return trans_id

    def get_transaction(self, trans_id):
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (trans_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def update_transaction(self, trans_id, title, amount, trans_type, category, date, payment_method="Cash", note=""):
        if not title or not title.strip():
            raise ValueError("Title is required.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if trans_type not in ['Expense', 'Income']:
            raise ValueError("Type must be 'Expense' or 'Income'.")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE transactions 
               SET title = ?, amount = ?, type = ?, category = ?, date = ?, payment_method = ?, note = ?
               WHERE id = ?""",
            (title.strip(), float(amount), trans_type, category.strip(), date, payment_method.strip(), note.strip(), trans_id)
        )
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    def delete_transaction(self, trans_id):
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    def get_transactions(self, category=None, trans_type=None, start_date=None, end_date=None, search=None, limit=None):
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM transactions WHERE 1=1"
        params = []

        if category and category != 'All':
            query += " AND category = ?"
            params.append(category)

        if trans_type and trans_type != 'All':
            query += " AND type = ?"
            params.append(trans_type)

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        if search:
            query += " AND (title LIKE ? OR note LIKE ? OR category LIKE ?)"
            search_param = f"%{search.strip()}%"
            params.extend([search_param, search_param, search_param])

        query += " ORDER BY date DESC, id DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # ------------------ SUMMARY & STATS ------------------ #
    def get_summary(self):
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        # Total Income & Expenses
        cursor.execute("SELECT type, SUM(amount) as total FROM transactions GROUP BY type")
        rows = cursor.fetchall()

        total_income = 0.0
        total_expense = 0.0
        for row in rows:
            if row['type'] == 'Income':
                total_income = row['total'] or 0.0
            elif row['type'] == 'Expense':
                total_expense = row['total'] or 0.0

        net_balance = total_income - total_expense
        savings_rate = ((total_income - total_expense) / total_income * 100) if total_income > 0 else 0.0

        # Expenses by category
        cursor.execute("""
            SELECT category, SUM(amount) as total 
            FROM transactions 
            WHERE type = 'Expense' 
            GROUP BY category 
            ORDER BY total DESC
        """)
        category_rows = cursor.fetchall()
        by_category = {row['category']: row['total'] for row in category_rows}

        # Monthly breakdown
        cursor.execute("""
            SELECT strftime('%Y-%m', date) as month, type, SUM(amount) as total
            FROM transactions
            GROUP BY month, type
            ORDER BY month ASC
        """)
        monthly_rows = cursor.fetchall()
        monthly_data = {}
        for row in monthly_rows:
            m = row['month']
            if not m:
                continue
            if m not in monthly_data:
                monthly_data[m] = {'income': 0.0, 'expense': 0.0}
            if row['type'] == 'Income':
                monthly_data[m]['income'] = row['total']
            else:
                monthly_data[m]['expense'] = row['total']

        conn.close()

        return {
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "net_balance": round(net_balance, 2),
            "savings_rate": round(savings_rate, 1),
            "by_category": by_category,
            "monthly_trend": monthly_data
        }

    def get_plotly_charts(self):
        """Generates interactive Plotly charts on Python backend."""
        import plotly.graph_objects as go
        import json
        from datetime import datetime

        summary = self.get_summary()
        by_cat = summary.get("by_category", {})
        monthly_trend = summary.get("monthly_trend", {})

        # 1. Category Donut Chart (Percentage removed, label & value only)
        if by_cat:
            cat_labels = list(by_cat.keys())
            cat_values = list(by_cat.values())
        else:
            cat_labels = ["No Expense Data"]
            cat_values = [1]

        colors = ['#2563eb', '#e11d48', '#059669', '#d97706', '#6366f1', '#ec4899', '#06b6d4', '#84cc16', '#f97316']

        cat_fig = go.Figure(data=[go.Pie(
            labels=cat_labels,
            values=cat_values,
            hole=.65,
            marker_colors=colors[:len(cat_labels)] if by_cat else ['#e2e8f0'],
            textinfo='label' if by_cat else 'none',
            hoverinfo='label+value'
        )])
        cat_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=True,
            legend=dict(font=dict(color='#475569', family='Outfit', size=12)),
            font=dict(family='Outfit')
        )

        # 2. Monthly Income vs Expense Bar Chart (Formatted Month Names without time/timestamps)
        raw_months = list(monthly_trend.keys()) if monthly_trend else []
        clean_months = []
        for m in raw_months:
            try:
                dt = datetime.strptime(m, "%Y-%m")
                clean_months.append(dt.strftime("%B %Y"))
            except Exception:
                clean_months.append(m)

        if not clean_months:
            clean_months = ["Current Month"]

        income_vals = [monthly_trend[m]['income'] for m in raw_months] if raw_months else [0]
        expense_vals = [monthly_trend[m]['expense'] for m in raw_months] if raw_months else [0]

        trend_fig = go.Figure(data=[
            go.Bar(name='Income', x=clean_months, y=income_vals, marker_color='#059669', hoverinfo='x+y+name'),
            go.Bar(name='Expense', x=clean_months, y=expense_vals, marker_color='#e11d48', hoverinfo='x+y+name')
        ])
        trend_fig.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(font=dict(color='#475569', family='Outfit', size=12)),
            xaxis=dict(tickfont=dict(color='#64748b', family='Outfit'), showgrid=False),
            yaxis=dict(tickfont=dict(color='#64748b', family='Outfit'), gridcolor='rgba(0,0,0,0.04)'),
            font=dict(family='Outfit')
        )

        return {
            "category_chart": json.loads(cat_fig.to_json()),
            "trend_chart": json.loads(trend_fig.to_json())
        }

    # ------------------ BUDGETS ------------------ #
    def get_budgets(self):
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        
        # Get set budget limits
        cursor.execute("SELECT category, monthly_limit FROM budgets")
        budget_map = {row['category']: row['monthly_limit'] for row in cursor.fetchall()}

        # Get current month expenses
        current_month = datetime.now().strftime("%Y-%m")
        cursor.execute("""
            SELECT category, SUM(amount) as spent 
            FROM transactions 
            WHERE type = 'Expense' AND strftime('%Y-%m', date) = ?
            GROUP BY category
        """, (current_month,))
        spent_map = {row['category']: row['spent'] for row in cursor.fetchall()}

        conn.close()

        result = []
        # Union of categories in budget map and spent map
        all_categories = sorted(list(set(list(budget_map.keys()) + list(spent_map.keys()))))
        for cat in all_categories:
            limit = budget_map.get(cat, 0.0)
            spent = spent_map.get(cat, 0.0)
            pct = (spent / limit * 100) if limit > 0 else 0.0
            result.append({
                "category": cat,
                "monthly_limit": round(limit, 2),
                "spent": round(spent, 2),
                "remaining": round(limit - spent, 2),
                "percentage": round(pct, 1),
                "is_over": spent > limit if limit > 0 else False
            })

        return result

    def set_budget(self, category, limit):
        if limit < 0:
            raise ValueError("Budget limit cannot be negative.")
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO budgets (category, monthly_limit) VALUES (?, ?)
            ON CONFLICT(category) DO UPDATE SET monthly_limit = excluded.monthly_limit
        """, (category.strip(), float(limit)))
        conn.commit()
        conn.close()
        return True

    # ------------------ IMPORT / EXPORT ------------------ #
    def export_csv(self, file_path):
        transactions = self.get_transactions()
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Title', 'Amount', 'Type', 'Category', 'Date', 'Payment Method', 'Note'])
            for t in transactions:
                writer.writerow([t['id'], t['title'], t['amount'], t['type'], t['category'], t['date'], t['payment_method'], t['note']])
        return len(transactions)

    def export_json(self, file_path):
        transactions = self.get_transactions()
        budgets = self.get_budgets()
        data = {
            "transactions": transactions,
            "budgets": budgets,
            "exported_at": datetime.now().isoformat()
        }
        with open(file_path, mode='w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return len(transactions)

    def import_csv(self, file_path):
        added_count = 0
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.add_transaction(
                        title=row.get('Title') or row.get('title'),
                        amount=float(row.get('Amount') or row.get('amount')),
                        trans_type=row.get('Type') or row.get('type') or 'Expense',
                        category=row.get('Category') or row.get('category') or 'Miscellaneous',
                        date=row.get('Date') or row.get('date'),
                        payment_method=row.get('Payment Method') or row.get('payment_method') or 'Cash',
                        note=row.get('Note') or row.get('note') or ''
                    )
                    added_count += 1
                except Exception as e:
                    print(f"Skipping row {row}: {e}")
        return added_count

    def import_json(self, file_path):
        added_count = 0
        with open(file_path, mode='r', encoding='utf-8') as f:
            data = json.load(f)
            raw_transactions = data.get("transactions", data if isinstance(data, list) else [])
            for row in raw_transactions:
                try:
                    self.add_transaction(
                        title=row.get('title'),
                        amount=float(row.get('amount')),
                        trans_type=row.get('type', 'Expense'),
                        category=row.get('category', 'Miscellaneous'),
                        date=row.get('date'),
                        payment_method=row.get('payment_method', 'Cash'),
                        note=row.get('note', '')
                    )
                    added_count += 1
                except Exception as e:
                    print(f"Skipping JSON item {row}: {e}")
        return added_count
