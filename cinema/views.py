from rest_framework.response import Response
from rest_framework import status, viewsets

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.viewsets import GenericViewSet

from cinema.models import Movie, Genre, Actor, CinemaHall
from cinema.serializers import (MovieSerializer,
                                GenreSerializer,
                                ActorSerializer,
                                CinemaHallSerializer)


class GenreList(APIView):
    @staticmethod
    def get(request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @staticmethod
    def post(request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class GenreDetail(APIView):
    @staticmethod
    def get_object(pk):
        return get_object_or_404(Genre, pk=pk)

    def get(self, request, pk):
        genre = self.get_object(pk=pk)
        serializer = GenreSerializer(genre)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        genre = self.get_object(pk=pk)
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        genre = self.get_object(pk=pk)
        serializer = GenreSerializer(genre, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        genre = self.get_object(pk=pk)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActorList(generics.GenericAPIView,
                mixins.ListModelMixin,
                mixins.CreateModelMixin):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ActorDetail(generics.GenericAPIView,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CinemaHallViewSet(GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
