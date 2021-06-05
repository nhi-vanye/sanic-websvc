from websvc import Config as thisApp


# TODO
# Might be an interesing experiment to measure the impact of pre-calculating
# all values and storing them in a DB/cache indexed by salary for a simple
# lookup. The number of possible salaries is limited (i.e. pre-calculate the
# first 100,000 items)
async def calculate_tax(salary: float = 0.0, details: bool = False) -> dict:
    """
    Calculate the tax owed based on the salary
    """

    total_tax_to_pay = 0.0
    detailed = []
    last = 0

    # The assumption is that the rules are ordered by salary DESCENDING
    for rule in thisApp.RULES["rules"]:
        if salary >= rule["from"]:
            tax_to_pay = (salary - rule["from"]) * rule["rate"]

            salary = rule["from"]

            total_tax_to_pay += tax_to_pay

            if details:
                if last:
                    detailed.append(
                        f"Tax paid on salary between £{rule['from']} "
                        f"and £{last} = £{tax_to_pay:.2f}"
                    )
                else:
                    detailed.append(
                        f"Tax paid on salary above £{rule['from']} " f"= £{tax_to_pay:.2f}"
                    )

            last = rule["from"] - 1

    return {"tax_owed": total_tax_to_pay, "details": detailed}
