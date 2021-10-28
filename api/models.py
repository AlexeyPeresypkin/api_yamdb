from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)


class Title(models.Model):
    name = models.CharField(max_length=250)
    year = models.SmallIntegerField()
    category = models.ForeignKey(Category, related_name='title')
    genre = models.ForeignKey(Genre, related_name='title')

    def __str__(self):
        return self.name


class Review(models.Model):
    title_id = models.OneToOneField(Title, on_delete=models.CASCADE,
                                    related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.SmallIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]


class Comments(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE,
                                  related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, related_name='genre_title',
                                 on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE,
                                 related_name='genre_title')
