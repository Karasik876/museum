import base64

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ConstructedCollection, UserConstructedCollection
from .serializers import ConstructedCollectionSerializer, ConstructedCollectionCreateSerializer, UserConstructedCollectionCreateSerializer
from core.utils import upload_image

class ConstructedCollectionViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action in ['create_collection_get', 'create_collection_post', 'upload_collection_image']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action in ['create_collection_get', 'create_collection_post']:
            return ConstructedCollectionCreateSerializer
        return ConstructedCollectionSerializer

    @action(detail=True)
    def get_collection_by_id(self, request, *args, **kwargs):
        collection_id = kwargs.get('pk')
        collection = get_object_or_404(ConstructedCollection, id=collection_id)
        serializer = ConstructedCollectionSerializer(collection)
        return Response(serializer.data)

    @action(detail=False)
    def create_collection_get(self, request, *args, **kwargs):
        return Response({"name": ''})

    @action(detail=False)
    def create_collection_post(self, request, *args, **kwargs):
        data = request.data.copy()
        img = request.data.get('collection_image')
        if img:
            image_url = upload_image.delay(base64.b64encode(img.read()), 'collection_images/avatars', True)
            data['collection_image'] = image_url.wait(timeout=None, interval=0.5)

        serializer = ConstructedCollectionCreateSerializer(data=data)
        if serializer.is_valid():
            collection = serializer.save()

            user_collection_data = {'user': request.user.id, 'constructed_collection': collection.id}
            user_collection_serializer = UserConstructedCollectionCreateSerializer(data=user_collection_data)
            if user_collection_serializer.is_valid():
                user_collection_serializer.save()
                full_collection_serializer = ConstructedCollectionSerializer(collection)
                return Response(full_collection_serializer.data, status=status.HTTP_201_CREATED)
            return Response(user_collection_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)