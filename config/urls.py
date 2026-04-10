from django.contrib import admin
from django.urls import path
from workplanner import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('add-shift/', views.add_shift, name='add_shift'),
    path('delete-shift/<int:shift_id>/', views.delete_shift, name='delete_shift'),
    path('confirm-shift/<int:shift_id>/', views.confirm_shift, name='confirm_shift'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
