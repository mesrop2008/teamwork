
from django.contrib import admin
from django.urls import path
from workplanner import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.schedule, name = 'schedule')
]
