from sanic import exceptions
from sanic.request import Request
from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView
from sanic_openapi import openapi

from .calculate import calculate_tax


class CalculateTax(HTTPMethodView):
    @openapi.summary("Calculate tax to be paid")
    @openapi.document("FRED")
    @openapi.parameter(name="salary", schema=float, location="query")
    @openapi.parameter(name="details", schema=bool, location="query")
    async def get(self, request: Request) -> HTTPResponse:

        if "salary" not in request.args:

            raise exceptions.InvalidUsage("Missing required parameter : 'salary'")
        details = False

        if "details" in request.args:
            details = bool((request.args.get("details")))

        try:
            # shortcut - request.args.get("salary") is too long to keep typing
            salary = float(request.args.get("salary"))
        except Exception as e:
            raise exceptions.InvalidUsage(f"Parsing salary : {str(e)}")

        if salary < 0.0:
            raise exceptions.InvalidUsage(f"Salary ({salary}) cannot be negative")

        tax_owed = await calculate_tax(salary=salary, details=details)

        resp = {"salary": salary, "tax_owed": tax_owed["tax_owed"]}

        # don't leak additional information unless explicitly asked...
        if details:
            resp["details"] = tax_owed["details"]

        return json(resp)
