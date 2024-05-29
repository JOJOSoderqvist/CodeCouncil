class PrintRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method
        path = request.get_full_path()

        print(f"{method} request to {path}")

        response = self.get_response(request)
        return response
