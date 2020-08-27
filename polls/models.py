from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=300)
    pub_date=models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name="authors", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.question_text
    

class Choice(models.Model):
    choice_text = models.CharField(max_length=300, verbose_name="choices")
    question = models.ForeignKey(
        Question, related_name="question", on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
