from django.utils.deprecation import MiddlewareMixin
from user_agents import parse

class UserTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = parse(user_agent_string)

        # Extract details
        request.device_type = "Mobile" if user_agent.is_mobile else "Tablet" if user_agent.is_tablet else "PC"
        request.ip_address = self.get_client_ip(request)
        request.browser = user_agent.browser.family  # Get browser name (Chrome, Firefox, etc.)
        request.os = user_agent.os.family  # Get OS (Windows, iOS, Android, etc.)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
