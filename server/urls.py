from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<uuid:ChecklistTemplateID_Value>", views.checklist_detail, name="detail"),
]
