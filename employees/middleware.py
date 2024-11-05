class RegistrationCleanUpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        employee_registration = request.session.get("employee_registration", False)
        employee_update = request.session.get("employee_update", False)
        payment_method_changed = request.session.get("payment_method_changed", False)

        if employee_registration and not "register-employee" in request.GET:
            keys = [
                "employee_registration",
                "user",
                "basic_information",
                "contact_information",
                "contract_information",
                "benefit_information",
                "banktransfer",
                "prepaidtransfer",
                "paypaltransfer",
                "cryptotransfer",
            ]

            for key in keys:
                if key in request.session:
                    request.session.pop(key)

            request.session.modified = True

        if employee_update and not "update-employee" in request.GET:
            request.session.pop("employee_update")

            request.session.modified = True

        if payment_method_changed and not "update-employee" in request.GET:
            request.session.pop("payment_method_changed")

            request.session.modified = True

        return self.get_response(request)
