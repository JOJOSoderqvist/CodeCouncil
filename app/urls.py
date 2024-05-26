from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('ask/', views.ask, name='ask'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
