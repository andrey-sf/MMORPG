from django.urls import path

from .views import AdCreateView, AdDeleteView, AdUpdateView, respond_to_ad, AdDetailView, accept_response, \
    delete_response

app_name = 'board'

urlpatterns = [
    path('add/', AdCreateView.as_view(), name='ad_create'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='ad_delete'),
    path('<int:pk>/edit/', AdUpdateView.as_view(), name='ad_update'),
    path('<int:ad_id>/respond/', respond_to_ad, name='ad_respond'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('accept_response/<int:response_id>/', accept_response, name='accept_response'),
    path('delete_response/<int:response_id>/', delete_response, name='delete_response'),
]
