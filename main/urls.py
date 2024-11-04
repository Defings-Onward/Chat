from django.urls import path, reverse
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('create-post', views.create_post, name='create_post'),
    #path('logout', auth_views.LogoutView.as_view(template_name="main/base.html", next_page="login"), name='logout')
    #path('logout', views.logout_view, name='logout')
]