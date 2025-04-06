from django.urls import path
from . import views

urlpatterns = [
    # path("The path used in the domain", views.your_function_name_from_views.py, name="your_function_name_from_views.py")
    # it is not required to have the name="" same as function name but it is useful
    path("", views.home, name="home"),
    path("webhook_1H/", views.webhook_1H, name="webhook_1H"),
    # If you need more webhooks or site pages, register the function in here with domain path, e.g. https://website_name/domain_path
    path("webhook_TIMEFRAME/", views.webhook_TIMEFRAME, name="webhook_TIMEFRAME"),
]