from flask import Flask, request, render_template, redirect, url_for

from forms import ExpenseForm, BudgetForm
from models import expenses, budgets

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/expenses/", methods=["GET", "POST"])
def expenses_list():
    form_expenses = ExpenseForm()
    form_budget = BudgetForm()
    error = ""
    if request.method == "POST":
        if form_expenses.validate_on_submit():
            expenses.create(form_expenses.data)
            expenses.save_all()
            budgets.sum(form_expenses.data['expense_type'], form_expenses.data['amount'])  
            return redirect(url_for("expenses_list"))
        if form_budget.validate_on_submit():
            budgets.create(form_budget.data)
            budgets.save_all()      
        return redirect(url_for("expenses_list"))
    return render_template("expenses.html", form_expenses=form_expenses, form_budget=form_budget,
                            expenses=expenses.all(), budgets=budgets.all(), error=error)


@app.route("/expenses/<int:budget_id>/", methods=["GET", "POST"])
def budget_details(budget_id):
    budget = budgets.get(budget_id - 1)
    form_budget = BudgetForm(data=budget)

    if request.method == "POST":
        if form_budget.validate_on_submit():
            budgets.update(budget_id - 1, form_budget.data)
        return redirect(url_for("expenses_list"))
    return render_template("budget.html", form_budget=form_budget, budget_id=budget_id)


if __name__ == "__main__":
    app.run(debug=True)