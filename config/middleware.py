"""
Middleware to log 500 tracebacks to /tmp so we can debug when DEBUG=False.
"""
import traceback
import sys


class Log500TracebackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception:
            self._log(request)
            raise

    def process_exception(self, request, exception):
        self._log(request)
        return None

    def _log(self, request):
        try:
            with open("/tmp/remedy_500.log", "a") as f:
                f.write("\n" + "=" * 60 + "\n")
                f.write(f"Host: {request.get_host()!r}\nPath: {request.path}\n")
                f.write(traceback.format_exc())
                f.write("\n")
        except Exception:
            pass
