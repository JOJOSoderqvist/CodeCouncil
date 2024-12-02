from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app import views
from askme_karpikhin import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>/', views.question_view, name='question'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('ask/', views.ask, name='ask'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('<int:card_id>/change_rating', views.change_rating, name='change_rating'),
    path('<int:answer_id>/change_is_correct', views.change_answer_correct, name='change_rating'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
