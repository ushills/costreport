def get_cost_detail(project, cost_code):
    return [
        {
            "transaction_id": 1,
            "transaction_date": "30/9/19",
            "project": "12345",
            "cost_code": "C34223",
            "supplier": "Subcontractor A",
            "transaction_amount": 34213,
            "transaction_description": "Starting allocation of tender sum",
            "user": "Bob",
        },
        {
            "transaction_id": 3,
            "transaction_date": "13/10/19",
            "project": "12345",
            "cost_code": "C34223",
            "supplier": "Subcontractor A",
            "transaction_amount": 3344,
            "transaction_description": "Variation 1",
            "user": "Alice",
        },
        {
            "transaction_id": 2,
            "transaction_date": "28/9/19",
            "project": "12345",
            "cost_code": "C34223",
            "supplier": "Subcontractor B",
            "transaction_amount": 232,
            "transaction_description": "Starting alloctanion of tender sum",
            "user": "Bob",
        },
    ]


def get_cost_summary(project, cost_code):
    cost_summary = {
        "cost_code": "C34223",
        "cost_code_description": "Space Heating & Air Treatment",
        "cost_allowance": 56000,
        "cost_forecast": 45000,
    }
    return cost_summary

