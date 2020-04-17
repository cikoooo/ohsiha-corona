from django.urls import path

from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('view/<int:pk>', views.news_view, name='news_view'),
    path('new', views.news_create, name='news_new'),
    path('edit/<int:pk>', views.news_update, name='news_edit'),
    path('delete/<int:pk>', views.news_delete, name='news_delete'),
    path('corona', views.corona_data, name='corona_data'),
    path('visualization', views.corona_visualization, name='corona_visualization'),
]
