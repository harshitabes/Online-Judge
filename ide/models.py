from django.db import models


class Problem(models.Model):
    title = models.CharField(max_length=100, default=True)
    statement = models.FileField(null=True, blank=True)

    def __str__(self):
        return f'id : {self.id} title: {self.title}'


class UserDetail(models.Model):
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default=" ")
    rating = models.IntegerField(default=1000)
    institute = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'username : {self.username} name: {self.name} rating : {self.rating} institute : {self.institute}'


class Submissions(models.Model):
    user = models.ForeignKey("UserDetail", on_delete=models.CASCADE)
    problem = models.ForeignKey("Problem", on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'problem']

# Create your models here.
