# inventory/urls.py
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.InventoryListView.as_view(), name='list'),
    path('<int:pk>/', views.InventoryDetailView.as_view(), name='detail'),
    path('create/', views.InventoryCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.InventoryUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.InventoryDeleteView.as_view(), name='delete'),
]
