import os
import json
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
from tracker import ExpenseTracker

app = Flask(__name__)
tracker = ExpenseTracker()

@app.route('/')
def index():
    return render_template('index.html')

# ---------------- API ENDPOINTS ----------------

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    category = request.args.get('category')
    trans_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    search = request.args.get('search')
    limit = request.args.get('limit', type=int)

    transactions = tracker.get_transactions(
        category=category,
        trans_type=trans_type,
        start_date=start_date,
        end_date=end_date,
        search=search,
        limit=limit
    )
    return jsonify(transactions)

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json() or {}
    try:
        trans_id = tracker.add_transaction(
            title=data.get('title'),
            amount=float(data.get('amount', 0)),
            trans_type=data.get('type', 'Expense'),
            category=data.get('category', 'Miscellaneous'),
            date=data.get('date'),
            payment_method=data.get('payment_method', 'Cash'),
            note=data.get('note', '')
        )
        return jsonify({'success': True, 'id': trans_id, 'message': 'Transaction added successfully'}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/transactions/<int:trans_id>', methods=['GET'])
def get_single_transaction(trans_id):
    transaction = tracker.get_transaction(trans_id)
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    return jsonify(transaction)

@app.route('/api/transactions/<int:trans_id>', methods=['PUT'])
def update_transaction(trans_id):
    data = request.get_json() or {}
    try:
        updated = tracker.update_transaction(
            trans_id=trans_id,
            title=data.get('title'),
            amount=float(data.get('amount', 0)),
            trans_type=data.get('type', 'Expense'),
            category=data.get('category', 'Miscellaneous'),
            date=data.get('date'),
            payment_method=data.get('payment_method', 'Cash'),
            note=data.get('note', '')
        )
        if updated:
            return jsonify({'success': True, 'message': 'Transaction updated successfully'})
        return jsonify({'error': 'Transaction not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/transactions/<int:trans_id>', methods=['DELETE'])
def delete_transaction(trans_id):
    deleted = tracker.delete_transaction(trans_id)
    if deleted:
        return jsonify({'success': True, 'message': 'Transaction deleted successfully'})
    return jsonify({'error': 'Transaction not found'}), 404

@app.route('/api/summary', methods=['GET'])
def get_summary():
    summary = tracker.get_summary()
    return jsonify(summary)

@app.route('/api/plotly-charts', methods=['GET'])
def get_plotly_charts():
    charts = tracker.get_plotly_charts()
    return jsonify(charts)

@app.route('/api/budgets', methods=['GET'])
def get_budgets():
    budgets = tracker.get_budgets()
    return jsonify(budgets)

@app.route('/api/budgets', methods=['POST'])
def set_budget():
    data = request.get_json() or {}
    category = data.get('category')
    limit = data.get('limit')
    if not category or limit is None:
        return jsonify({'error': 'Category and limit are required'}), 400
    try:
        tracker.set_budget(category, float(limit))
        return jsonify({'success': True, 'message': f'Budget for {category} set to {float(limit):.2f}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/export/<string:fmt>', methods=['GET'])
def export_data(fmt):
    temp_dir = tempfile.gettempdir()
    if fmt == 'csv':
        file_path = os.path.join(temp_dir, "expenses_export.csv")
        tracker.export_csv(file_path)
        return send_file(file_path, as_attachment=True, download_name="expenses_export.csv", mimetype="text/csv")
    elif fmt == 'json':
        file_path = os.path.join(temp_dir, "expenses_export.json")
        tracker.export_json(file_path)
        return send_file(file_path, as_attachment=True, download_name="expenses_export.json", mimetype="application/json")
    return jsonify({'error': 'Unsupported format'}), 400

@app.route('/api/import', methods=['POST'])
def import_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'Empty filename'}), 400

    filename = file.filename.lower()
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.filename)
    file.save(temp_path)

    try:
        if filename.endswith('.csv'):
            count = tracker.import_csv(temp_path)
        elif filename.endswith('.json'):
            count = tracker.import_json(temp_path)
        else:
            return jsonify({'error': 'Only CSV and JSON files are supported'}), 400
        
        return jsonify({'success': True, 'imported_count': count, 'message': f'Successfully imported {count} transactions.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
