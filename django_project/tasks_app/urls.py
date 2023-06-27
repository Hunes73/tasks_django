from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, LogoutView
from . import views

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
