import traceback
import os

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/api/route-analysis/' and request.method == 'POST':
            try:
                body = request.body.decode('utf-8')
                with open('django_request.log', 'a', encoding='utf-8') as f:
                    f.write(f"\n--- REQUEST AT {request.path} ---\n")
                    f.write(f"Body: {body}\n")
                    f.write("------------------------------\n")
            except:
                pass
        
        response = self.get_response(request)
        
        if request.path == '/api/route-analysis/' and request.method == 'POST':
            with open('django_request.log', 'a', encoding='utf-8') as f:
                f.write(f"--- RESPONSE FOR {request.path} ---\n")
                f.write(f"Status: {response.status_code}\n")
                if response.status_code >= 400:
                    try:
                        f.write(f"Content: {response.content.decode('utf-8')[:500]}\n")
                    except:
                        pass
                f.write("------------------------------\n")
        
        return response

    def process_exception(self, request, exception):
        with open('django_error.log', 'a', encoding='utf-8') as f:
            f.write(f"\n--- EXCEPTION AT {request.path} ---\n")
            f.write(traceback.format_exc())
            f.write("\n------------------------------\n")
        return None
