from django.urls import path

from . import views

app_name = 'maintainer'
urlpatterns = [
    path('', views.maintainer_list, name='list'),
    path('<uuid:ChecklistTemplateMaintainerID_Value>', views.maintainer_detail, name='detail'),
    path('<uuid:ChecklistTemplateMaintainerID_Value>/json', views.maintainer_json, name='json'),
]
