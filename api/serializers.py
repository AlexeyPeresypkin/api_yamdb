from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from .models import Genre, Title, Category, Review, Comments


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    # title = serializers.CharField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title,
                    author=request.user
            ).exists():
                raise ValidationError('Only one review is allowed')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    review = serializers.CharField(read_only=True, source='review.title')
    author = serializers.CharField(read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'review', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = "__all__"
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Title
