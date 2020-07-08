from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)

    def get_all_likes(self):
        return Like.objects.filter(post=self)

    def like_manage(self, user):
        # try to get like from user and delete if exist else - create

        like = self.get_all_likes().filter(author=user)

        if like:
            return False, like.delete()
        else:
            return True, Like.objects.create(author=user, post=self)


class Like(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class UserActivity(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    last_request_date = models.DateTimeField(null=True, blank=True)
    login_date = models.DateTimeField(null=True, blank=True)