# def get_forecast_detail():
#     return [
#         {
#             "cost_code": "C34223",
#             "cost_code_description": "Space Heating & Air Treatment",
#             "cost_allowance": 56000,
#             "cost_forecast": 45000,
#         },
#     ]
from costreport.data.costcodes import Costcodes


def get_forecast_detail():
    cost_code_detail = Costcodes.query.order_by(Costcodes.costcode.asc()).all()
    print(cost_code_detail)
    return cost_code_detail


def get_summary_detail():
    return {
        "forecast_income": 2636636,
        "forecast_cost": 2343224,
        "forecast_profit": 324231,
        "forecast_profit_percentage": 0.085,
    }
