# Family budget

## Description
    SImple web application to keep family expenses within a budget.

## Technologies
    - Python
    - Flask
    - CSS
    - Bootstrap
    - HTML
    - API

## How to run the applicaiton

1. Clone the repository.
2. Make sure that folder "templates" is inside of the root folder
3. Open command prompt
4. Navigate to root folder (cd folder_path)
5. Install flask (pip install flask)
6. Optional: Set environment variable (set FLASK_ENV=development) 
7. Set flask application (set FLASK_APP=app.py)
8. Run flask (flask run)
9. Navigate to http://127.0.0.1:5000/main in your browser

## How to use

1. Open URL .../main
2. Plan your budget by adding expense type and amount
3. Add your first expense by entering a date, amount, selecting an expense type.
   NOTE: you can add an expense only if the expense type is added to your budget.
   If your expense was saved successfully, you will get a green pop up message on top of your screen.
   If you get an error, check the correctness of your data. 
4. You can display the history of your expenses by clicking on "Show expenses" button.

## How to use API

1.  Get list of all your expenses:
    Method: GET,
    Endpoint: /api/v1/expenses/

2. Get list of all your budgets:
    Method: GET,
    Endpoint: /api/v1/budgets/

3. Get detsils of selected budget. As <int:budget_id> indicate the position of the budget on the budgets list.
    Method: GET,
    Endpoint: /api/v1/budget/<int:budget_id>

4. Add expense to your expenses list. You can add an expense only if budgets for the expense type already exists.
    Method: POST,
    Endpoint: /api/v1/expense,
    Header: Content-Type: application/json,
    Body example:
        {
        'date': "2020-10-01",
        'expense_type': "Rent",
        'amount': 1000,
        'comment': ""
        }

5. Delete a budget from the budgets list. As <int:budget_id> indicate the position of the budget on the budgets list.
    Method: DELETE,
    Endpoint: /api/v1/main/<int:budget_id>


