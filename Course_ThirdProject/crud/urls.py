from django.urls import path
from crud import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('edit/<int:id>/', views.edit),
    path('delete/<int:id>/', views.delete),

    path('finance/<int:id>/', views.finance, name='finance'),
    path('finance/<int:person_id>/create/', views.finance_create, name='finance_create'),
    path('finance/entry/<int:fid>/', views.finance_edit, name='finance_edit'),
    path('finance/entry/<int:fid>/delete/', views.finance_delete, name='finance_delete'),
]
