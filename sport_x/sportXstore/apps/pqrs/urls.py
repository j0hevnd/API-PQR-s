from django.urls import path

from apps.pqrs import views

app_name = 'app_pqrs'

urlpatterns = [
    path('list-pqrs/', views.PqrsListView.as_view(), name='list_pqrs'),
    path('create-pqrs/', views.PqrsCreateView.as_view(), name='create_pqrs'),
    path('detail-pqrs/<int:pk>/', views.PqrsDetailView.as_view(), name='detail_pqrs'),
    path('update-pqrs/<int:pk>/', views.PqrsRetrieveUpdateView.as_view(), name='update_pqrs'),
    path('delete-pqrs/<int:pk>/', views.PqrsDeleteView.as_view(), name='delete_pqrs'),
    path('delete-severals-pqrs/', views.PqrsDeleteSeveralApiView.as_view(), name='delete_several_pqrs'),
]