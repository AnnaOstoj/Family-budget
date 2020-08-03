from flask import abort, Flask, flash, jsonify, make_response, request, render_template, redirect, url_for
from datetime import datetime, date
import calendar
from forms import ExpenseForm, BudgetForm, MonthForm
import json
from models import expenses, budgets


app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/main/", methods=["GET", "POST"])
def show_main():
    month_number = date.today().month
    month = calendar.month_name[month_number]

    if request.method == "POST":
        if request.form["btn"] == "Register new expense":
            return redirect(url_for("add_expense"))

        elif request.form["btn"] == "Add budget":
            return redirect(url_for("add_budget"))

        elif request.form["btn"] == "Show expenses":
            return redirect(url_for("expenses_list"))
            
    return render_template("main.html", month=month,
                            expenses=expenses.all(), budgets=budgets.all(),
                            total_budget=budgets.sum_total_budget(), amount_left=budgets.sum_amount_left())


@app.route("/addbudget/", methods=["GET", "POST"])
def add_budget():
    form_budget = BudgetForm()
    if request.method == "POST":
        if form_budget.validate_on_submit():
            budgets.create(form_budget.data)
            budgets.save_all()      
        return redirect(url_for("show_main"))
    return render_template("add_budget.html",  form_budget=form_budget)

@app.route("/regexpense/", methods=["GET", "POST"])
def add_expense():
    form_expenses = ExpenseForm()
    form_expenses.expense_type.choices = [(str(i['expense_type']), i['expense_type']) for i in budgets.all()]
    month_number = date.today().month

    if request.method == "POST":
        if request.form["btn"] == "Add":

            if form_expenses.validate_on_submit():  
                if budgets.check_type(form_expenses.data['expense_type']):
                    expenses.create(form_expenses.data)
                    expenses.save_all()
                    if form_expenses.data['date'].month == month_number:   
                        budgets.sum(form_expenses.data['expense_type'], form_expenses.data['amount'])  
                        flash("Your expense has been registered", 'success')
                else: 
                    flash("Expense not registered. Expense type does not exist in your budget", 'danger')
                return redirect(url_for("add_expense"))

        if request.form["btn"] == "Back":
            return redirect(url_for("show_main"))

    return render_template("reg_expense.html", form_expenses=form_expenses)

@app.route("/expenses/", methods=["GET", "POST"])
def expenses_list():

    form_month=MonthForm()
    form_month.month.choices = [calendar.month_name[i] for i in range(1,13)]

    if request.method == "POST":
        if request.form["btn"] == "Filter":
            month_name= form_month.data['month']
            month_number = datetime.strptime(month_name, "%B").month
            filtered_expenses = expenses.filter(month_number)
            return render_template("expenses.html", expenses=filtered_expenses, form_month=form_month)

    return render_template("expenses.html", expenses=expenses.all(), form_month=form_month)

@app.route("/main/budget/<int:budget_id>/", methods=["GET", "POST"])
def budget_details(budget_id):
    budget = budgets.get(budget_id - 1)
    form_budget = BudgetForm(data=budget)
    if request.method == "POST":
        if request.form["btn"] == "Save":
            budgets.update(budget_id - 1, form_budget.data)
            flash(f"Your budget for {form_budget.data['expense_type']} is now modified", 'success')
            return redirect(url_for("show_main"))        
        elif request.form["btn"] == "Delete":
            budgets.delete(budget_id - 1)
            flash(f"Your budget for {form_budget.data['expense_type']} is deleted", 'success')
            return redirect(url_for("show_main"))
    return render_template("budget.html", form_budget=form_budget, budget_id=budget_id)


@app.route("/api/v1/expenses/", methods=["GET"])
def expenses_list_api_v1():
    return jsonify(expenses.all())

@app.route("/api/v1/budget/<int:budget_id>", methods=["GET"])
def get_budget(budget_id):
    budget = budgets.get(budget_id)
    print(budget)
    if not budget:
        abort(404)
    return jsonify({"budget": budget})

@app.route("/api/v1/main", methods=["POST"]) # nie działa
def create_expense():

    data = request.get_json()

    name = data['name']
    return jsonify({"result": "Success", "name": name})

"""
    if not request.json or not 'expense_type' in request.json:
       abort(400)

    expense = {
        'date': request.json['date'],
        'expense_type': request.json['expense_type'],
        'amount': request.json['amount'],
        'comment':request.json['comment']
    }
    expenses.create(expense)

    return make_response(jsonify({'expense': expense}), 201)   
"""
@app.route("/api/v1/main/<int:budget_id>", methods=['DELETE'])
def delete_budget(budget_id):
    result = budgets.get(budget_id - 1)
    budgets.delete(budget_id - 1)
    return jsonify({'result': result})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


if __name__ == "__main__":
    app.run(debug=True)