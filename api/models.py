from django.conf import settings
from django.db import models
# from django.db.models import permalink
# from taggit.managers import TaggableManager
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True)
    # slug = models.SlugField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=30, unique=True)
    # slug = models.SlugField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return ('tags', None, {'slug': self.slug})


class SeoModel(models.Model):
    seo_title = models.CharField(
        max_length=70,
        blank=True,
        null=True,
    )
    seo_description = models.CharField(
        max_length=300,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class User(AbstractUser):
    # followers = models.ManyToManyField('self', related_name ='user_followers', symmetrical=False)
    bio = models.CharField(max_length=100, null=True)
    avatar = models.ImageField(
        'profile picture',
        upload_to='media/avatars/',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username


STATUS = {0: "Draft", 1: "Submit"}


class Post(SeoModel):
    author = models.ForeignKey(
        'User',
        related_name='user_posts',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    views = models.IntegerField(default=0)
    # tags = TaggableManager()
    tags = models.ManyToManyField('Tag', related_name='posts')
    content = models.TextField()
    # likes = models.ManyToManyField(Like, related_name="post_likes")
    # likes = models.IntegerField(default=0)
    submited_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(auto_now=True)
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    status = models.IntegerField(
        default=0, choices=list(STATUS.items()), verbose_name='Status')

    approve = models.BooleanField(default=False)
    # slug = models.SlugField(max_length=100, default='')
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    category = models.ForeignKey(
        'category',
        related_name="post_category",
        verbose_name="categories",
        on_delete=models.CASCADE,
    )

    # seo_tags = models.ForeignKey('Seo', related_name='post_seotags', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return ('post_detail', None, {'slug': self.slug})

    class Meta:
        ordering = ('-submited_at', )

    # def increase_views(self):
    #     self.views += 1
    #     self.save(update_fields=['views'])


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="comment",
        verbose_name="comments",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    # likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    # comment_likes = models.ManyToManyField(User, related_name="comment_likes")
    description = models.TextField()
    # likes = models.IntegerField(default=0)
    approve = models.BooleanField(default=False)
    submited_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(
        default=0, choices=list(STATUS.items()), verbose_name='Status')
    # active = models.BooleanField(default=False)
    # image = models.ImageField(upload_to='blogImgs/')
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ('-submited_at', )


class Page(models.Model):
    author = models.ForeignKey(
        'User',
        related_name='user_page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    views = models.IntegerField(default=0)
    # tags = TaggableManager()
    content = models.TextField()
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    publish = models.BooleanField(default=False)
    # slug = models.SlugField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class user_actions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_post = models.ForeignKey(
        Post, related_name='post_likes', on_delete=models.CASCADE)
    liked_comments = models.ForeignKey(
        Comment, related_name='comment_likes', on_delete=models.CASCADE)
    fav = models.ForeignKey(
        Post, related_name='fav_post', on_delete=models.CASCADE)
    target = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    follower = models.ForeignKey(
        User,
        related_name='targets',
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    def __str__(self):
        return self.user.username