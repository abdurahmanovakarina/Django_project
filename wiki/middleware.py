from wiki.singleton import SectionTree
from django.template.response import TemplateResponse


# Define the NavbarFooterMiddleware class
class NavbarFooterMiddleware:
    # Initialize the class with get_response method
    def __init__(self, get_response):
        self.get_response = get_response

    # Define the call method to execute the middleware
    def __call__(self, request):
        # Get the section tree
        section_tree = SectionTree().tree
        # Get the response from the view
        response = self.get_response(request)
        # If the response is a TemplateResponse, add the section tree to the context data
        if isinstance(response, TemplateResponse):
            response.context_data["section_tree"] = section_tree
        # Return the response
        return response
