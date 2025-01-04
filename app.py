from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)
data_file = "transactions.xlsx"
fixed_file = "fixed_payments.xlsx"

# Initialize Excel files
def initialize_excel(file_name, columns):
    if not os.path.exists(file_name):
        df = pd.DataFrame(columns=columns)
        df.to_excel(file_name, index=False)

initialize_excel(data_file, ["Date", "Description", "Amount", "Type", "Category"])
initialize_excel(fixed_file, ["Date", "Description", "Amount", "Type"])

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        data = request.json
        date = data.get('date')
        description = data.get('description')
        amount = float(data.get('amount'))
        type_ = data.get('type')
        category = data.get('category', '')

        df = pd.read_excel(data_file)
        new_row = {"Date": date, "Description": description, "Amount": amount, "Type": type_, "Category": category}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(data_file, index=False)

        return jsonify({"status": "success", "message": "Transaction added successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    try:
        df = pd.read_excel(data_file)
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/generate_report', methods=['GET'])
def generate_report():
    try:
        if os.path.exists(data_file):
            return send_file(data_file, as_attachment=True, download_name="transactions_report.xlsx")
        else:
            return jsonify({"status": "error", "message": "No data available."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
