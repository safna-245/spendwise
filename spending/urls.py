from django.urls import path
from spending.views import SignUpView,GetMeView,ExpenseListCreateView

from spending.views import ExpenseRetrieveUpdateDeleteView
urlpatterns = [

    path("register/",SignUpView.as_view()),
    path("me/",GetMeView.as_view()),
    path("expenses/",ExpenseListCreateView.as_view()),
    path("expenses/<int:pk>/",ExpenseRetrieveUpdateDeleteView.as_view())
]