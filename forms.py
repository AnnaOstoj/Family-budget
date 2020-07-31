from flask_wtf import FlaskForm
from wtforms import FloatField, TextAreaField, DateField, SelectField, StringField
from wtforms.validators import DataRequired


class ExpenseForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    expense_type = SelectField(choices=[('Food', 'Food'), ('Rent', 'Rent'), ('Clothes', 'Clothes'),
                                        ('Pets', 'Pets'), ('Education', 'Education'), ('Entertainment', "Entertainment")],
                                        validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    comment = TextAreaField('Comment')

class BudgetForm(FlaskForm):
    expense_type = StringField('Expense Type', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])

