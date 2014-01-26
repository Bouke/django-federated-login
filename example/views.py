from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from example.utils import class_view_decorator


class HomeView(TemplateView):
    template_name = 'home.html'


@class_view_decorator(login_required)
class ExampleSecretView(TemplateView):
    template_name = 'secret.html'
