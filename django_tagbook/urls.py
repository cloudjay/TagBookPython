from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path
from books.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page),
    path('login/', LoginView.as_view(template_name='registration/login.html')),
    path('logout/', logout_page),
    path('register/', register_page),
    path('edit/', edit_page),
    path('user/<str:username>', user_page),
    path('checkisbn/', check_page), # check if user has the record of this book
    path('finishyear/', finish_year_page),
    path('listyear/', list_of_year_page),
    path('listtag/', list_of_tag_page),
    path('listauthor/', list_of_author_page),
    path('listflag/', list_by_flags_page),
    path('delete/', delete_page),
]
