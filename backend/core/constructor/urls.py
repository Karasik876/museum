from django.urls import path
from .views import ConstructedCollectionViewSet

urlpatterns = [
    path('constructed-collections/<int:pk>/', ConstructedCollectionViewSet.as_view({'get': 'get_collection_by_id'}), name='constructed-collections'),
    path('constructed-collections/create/', ConstructedCollectionViewSet.as_view({'get': 'create_collection_get', 'post': 'create_collection_post'}), name='constructed-collections-create'),
]
