from django.urls import path

from main_app.views import *

urlpatterns = [
    path('', TaskView.as_view(), name='main'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('author/<int:pk>/', TaskViewAuthor.as_view(), name='author'),
    path('add/', AddTask.as_view(), name='add'),
    path('edit/<int:pk>/', EditTask.as_view(), name='edit'),
    path('delete/<int:pk>/', DeleteTask.as_view(), name='delete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registration/', registration_view, name='registration')

]
