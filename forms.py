from flask_wtf import FlaskForm
from wtforms import FloatField, TextAreaField, SelectField, StringField, DateField
from wtforms.validators import DataRequired, ValidationError



class ExpenseForm(FlaskForm):
    date = DateField('Date', format="%d.%m.%Y", validators=[DataRequired()])
    expense_type = SelectField('Select Field', choices=[], validators=[DataRequired()])
    amount = FloatField('Amount', [DataRequired()])
    comment = TextAreaField('Comment')

class BudgetForm(FlaskForm):
    expense_type = StringField('Expense Type', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])

class MonthForm(FlaskForm):
    month = SelectField('Month', choices=[], validators=[DataRequired()])
