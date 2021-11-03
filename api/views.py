from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from api.filter import TitleFilter
from api.models import Review, Title, Category, Genre
from api.permissions import ReviewOrCommentPermission, IsAdminOrReadOnly
from api.serializers import (
    ReviewSerializer,
    CommentsSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleWriteSerializer,
    TitleReadSerializer
)
from rest_framework import permissions
from rest_framework import filters


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewOrCommentPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [ReviewOrCommentPermission]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Title, pk=title_id)
        review = get_object_or_404(Review, pk=review_id, title=title)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        author = self.request.user
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=author, review=review)


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    # filter_backends = [filters.SearchFilter]
    # filterset_fields = ['name', ]
    queryset = Category.objects.all()
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class TitleViewSet(ModelViewSet):
    serializer_class = TitleWriteSerializer
    queryset = Title.objects.annotate(rating=Avg(
        'reviews__score')).order_by('-id')
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    ]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer
