from django.urls import path, include
from . import views


urlpatterns = [
    path('' , views.HomeView , name = "Home"),
    path('signup/' , views.SignupView , name = 'Signup'),
    path('login/' , views.LoginView , name = 'Login'),
    path('logout/' , views.LogoutView , name = 'Logout'),
    path('search/' , views.SearchView , name = 'Search'),
    path('history/' , views.HistoryView , name = 'History'),
    path('savedhistory/' , views.SavedHistoryView , name = 'SavedHistory'),
    path('dashboard/' , views.dashboard , name = 'Dashboard'),
]