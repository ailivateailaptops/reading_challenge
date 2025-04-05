from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start-test/', views.start_test, name='start_test'),
    path('record-speech/', views.record_speech, name='record_speech'),
    path('evaluate/', views.evaluate_speech, name='evaluate_speech'),
]
