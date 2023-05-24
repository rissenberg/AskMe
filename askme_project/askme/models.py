from django.db import models
from django.db.models import Count, When
from django.contrib.auth.models import User


class PostManager(models.Manager):
    def get_hot_posts(self):
        return self.annotate(count=Count('likeq', distinct=True)).order_by('-count')

    def get_recent_posts(self):
        return self.all().order_by('-date')

    def get_posts_for_tag(self, title):
        return self.filter(tags__title=title)

    def get_posts_for_user(self, user_id):
        return self.filter(author__user_id=user_id)


class AnswerManager(models.Manager):
    def get_answers_for_question(self, p_id):
        return self.filter(question_id=p_id)


class TagManager(models.Manager):
    def get_tag_by_id(self, t_id):
        return self.filter(id=t_id)

    def get_tag_by_title(self, title):
        return self.get(title=title)

    def get_hot_tags(self):
        return self.all().annotate(count=Count('posts')).order_by('-count')[:9]

    def get_post_tags(self, p_id):
        return self.filter(question__id=p_id)


class ProfileManager(models.Manager):
    def get_top_users(self):
        return self.all().annotate(rating=0.3 * Count('answer') + 0.1 * Count('post')).order_by('-rating')[:10]

    def get_user_by_id(self, u_id):
        return self.get(user_id=u_id)


class LikeQManager(models.Manager):
    def get_likes_count_for_question(self, q_id):
        likes = self.filter(question_id=q_id)
        return likes.count()


class LikeAManager(models.Manager):
    def get_likes_count_for_answer(self, a_id):
        return self.count(answer_id=a_id)


# Models


class Profile(models.Model):
    objects = ProfileManager()

    user = models.OneToOneField(User, null=True, related_name='profile_related', on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to='profiles/avatars/')
    bio = models.TextField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username

    def answers(self):
        return Answer.objects.filter(author_id=self.id).count()


class Tag(models.Model):
    objects = TagManager()

    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Post(models.Model):
    objects = PostManager()

    author = models.ForeignKey(Profile, null=False, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=5000)

    def get_author(self):
        return self.author

    def get_author_id(self):
        return self.author.user.id

    def get_username(self):
        return self.author.user.username

    def get_like_count(self):
        return LikeQ.objects.filter(question_id=self.id).count()

    def get_answer_count(self):
        return Answer.objects.filter(question_id=self.id).count()

    def get_tags(self):
        return self.tags.all()

    def __str__(self):
        return self.title


class Answer(models.Model):
    objects = AnswerManager()

    question = models.ForeignKey(Post, default=1, null=False, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(auto_now=True)
    text = models.TextField()
    solution = models.BooleanField(default=False)

    def is_solution(self):
        return self.solution

    def get_author(self):
        return self.author

    def get_author_id(self):
        return self.author.user.id

    def get_username(self):
        return self.author.user.username

    def get_like_count(self):
        return LikeA.objects.filter(answer_id=self.id).count()

    def __str__(self):
        return f"{self.question.title}_answer"


class LikeQ(models.Model):
    objects = LikeQManager()

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Post, default=1, on_delete=models.CASCADE)


class LikeA(models.Model):
    objects = LikeAManager()

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
