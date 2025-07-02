from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.user_login_view, name='login'),
    path('logout/', views.user_logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Programme URLs
    path('programmes/', views.programme_list_view, name='programme_list'),
    path('programmes/add/', views.programme_create_view, name='programme_create'),
    path('programmes/<int:pk>/', views.programme_detail_view, name='programme_detail'),
    path('programmes/<int:pk>/edit/', views.programme_update_view, name='programme_update'),
    path('programmes/<int:pk>/delete/', views.programme_delete_view, name='programme_delete'),

    # Financial Transaction URLs
    path('finances/', views.financial_transaction_list_view, name='financial_transaction_list'),
    path('finances/add/', views.financial_transaction_create_view, name='financial_transaction_create'),
    path('finances/<int:pk>/', views.financial_transaction_detail_view, name='financial_transaction_detail'),
    path('finances/<int:pk>/edit/', views.financial_transaction_update_view, name='financial_transaction_update'),
    path('finances/<int:pk>/delete/', views.financial_transaction_delete_view, name='financial_transaction_delete'),

    # To-Do List URLs
    path('todo/', views.todo_list_view, name='todo_list'),
    path('todo/add/', views.todo_create_view, name='todo_create'),
    path('todo/<int:pk>/', views.todo_detail_view, name='todo_detail'),
    path('todo/<int:pk>/edit/', views.todo_update_view, name='todo_update'),
    path('todo/<int:pk>/delete/', views.todo_delete_view, name='todo_delete'),

    # Commercial URLs (New)
    path('commercials/', views.commercial_list_view, name='commercial_list'),
    path('commercials/add/', views.commercial_create_view, name='commercial_create'),
    path('commercials/<int:pk>/', views.commercial_detail_view, name='commercial_detail'),
    path('commercials/<int:pk>/edit/', views.commercial_update_view, name='commercial_update'),
    path('commercials/<int:pk>/delete/', views.commercial_delete_view, name='commercial_delete'),
]
