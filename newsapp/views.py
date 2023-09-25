from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count

import requests

from .models import History, UserInfo , is_admin



API_KEY = "a08db25b53b343b98b9d8b14540d3920"


# Create your views here.
def HomeView(request):
    # view function for home page which will show latest news of india.
    url =  f"https://newsapi.org/v2/top-headlines?country=in&apiKey={API_KEY}"
    data = requests.get(url)
    response = data.json()
    articles = response['articles']
    context = {'articles' : articles}

    return render(request, 'newsapp/Home.html', context)


@login_required(login_url='/login/')
def SearchView(request):
    """search view will get keyword as a search name and new page will show news according to keyword entered."""
    keyword = request.GET['Search']
    language = request.GET['Language']
    country = request.GET['Country']
    url =f"https://newsapi.org/v2/everything?q={keyword}&apiKey={API_KEY}"
    if language:
        url += f"&language={language}"
    if country:
        url += f"&country={country}"


    data = requests.get(url)
    response = data.json()
    articles = response['articles']
                
    urls = []
    for article in articles:
        url = article.get('url', '')
        if url:
            urls.append(url)
    context = {'articles' : articles , 'keyword': keyword, 'result': urls}
    # for saving response in history model
    history = History(user=request.user,keyword=keyword, result =urls ) 
    history.save()          
                

    return render(request, 'newsapp/search.html', context)


# @login_required(login_url='/login/')
# def SearchView(request):
#     # search view will get keyword as a search name and new page will show news according to keyword entered.
    
#     # To check per user quota of user
#     print(request.user.id)
#     user_info = UserInfo.objects.all()
#     print(user_info)
#     if user_info.User_quota >0:
#         keyword = request.GET['Search']
#         if keyword:
#             user_info.User_quota -= 1
#             user_info.save()
#             url =f"https://newsapi.org/v2/everything?q={keyword}&apiKey={API_KEY}"
#             data = requests.get(url)
#             response = data.json()
#             articles = response['articles']
            
#             urls = []
#             for article in articles:
#                 url = article.get('url', '')
#                 if url:
#                     urls.append(url)
#             context = {'articles' : articles , 'keyword': keyword, 'result': urls}
            
#             # save keyword in model History
#             History.objects.create(keyword=keyword, result =urls)

#             return render(request, 'newsapp/search.html', context)
#     else:
#       messages.error(request, "Search quota exhausted.")  
#     return render(request, 'newsapp/home.html')




def HistoryView(request):
    # history view for showing saved history object saved in history table with latest history on top with timestamp
    
    keyword = History.objects.filter(user=request.user).order_by('-time')
    context = {'keyword': keyword }
    return render(request, 'newsapp/history.html', context)


def SavedHistoryView(request):
    """
        This view will show urls that returned while particular search is made
    """
    result = History.objects.values('result')
    for url in result:
        print(url)
    
    context={'result': result}
    return render(request, 'newsapp/savedhistory.html', context)


def SignupView(request):
    """
        Signup or register new user
    """
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password= password)
            login(request, user)
            UserInfo.objects.create(user=user, username= username)
            messages.success(request,("Registration successfull"))
            return redirect('Home')
    else:
        form = UserCreationForm()

    return render(request, 'newsapp/signup.html', {'form': form})


def LoginView(request):
    """
        Login functionality
    """
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else: 
            return redirect('Login')
    else:

        return render(request, 'newsapp/login.html')
    

def LogoutView(request):
    logout(request)
    return redirect('Home')

@user_passes_test(is_admin)
def dashboard(request):
    """
        only admin can access dashboard section. Most searched keywords will be displayed on dashboard with their count.
    """
    trending_keyword = History.objects.values('keyword').annotate(search_count = Count('keyword')).order_by('-search_count')[:15]
    context ={'trending_keyword' : trending_keyword}
    return render(request, 'newsapp/dashboard.html', context)
