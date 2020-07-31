import json


class Expenses:
    def __init__(self):
        try:
            with open("expenses.json", "r") as f:
                self.expenses = json.load(f)
        except FileNotFoundError:
            self.expenses = []

    def all(self):
        return self.expenses

    def get(self, id):
        return self.expenses[id]

    def create(self, data):
        data.pop('csrf_token')
        self.expenses.append(data)

    def save_all(self):
        with open("expenses.json", "w") as f:
            json.dump(self.expenses, f)

    def update(self, id, data):
        data.pop('csrf_token')
        self.expenses[id] = data
        self.save_all()

class Budget:
    def __init__(self):
        try:
            with open("budget.json", "r") as f:
                self.budgets = json.load(f)
        except FileNotFoundError:
            self.budgets = []

    def create(self, data):
        data.pop('csrf_token')
        self.budgets.append(data)

    def all(self):
        return self.budgets
    
    def get(self, id):
        return self.budgets[id]
    
    def save_all(self):
        with open("budget.json", "w") as f:
            json.dump(self.budgets, f)

    def update(self, id, data):
        data.pop('csrf_token')
        self.budgets[id]['expense_type'] = data['expense_type']
        self.budgets[id]['budget'] = data['budget']
        self.save_all()

    def sum(self, expense_type, amount):
        for item in self.budgets:
            if item['expense_type'] == expense_type:
                if 'sum' in item.keys():
                    item['sum'] += amount
                else:
                    item.update({'sum': float(amount) })
                self.save_all()
        
expenses = Expenses()
budgets = Budget()