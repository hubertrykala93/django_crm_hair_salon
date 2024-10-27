class RegistrationCleanUpMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        registration_in_progress = request.session.get("registration_in_progress", False)
        print(registration_in_progress)
        print(request.GET)

        if registration_in_progress and not "register-employee" in request.GET:
            keys = [
                "registration_in_progress",
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

        return self.get_response(request)
