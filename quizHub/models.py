from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Quiz(models.Model):
    STATUS_CHOICES = [
        ('P', 'Published'),
        ('D', 'Draft'),
        ('A', 'Archived'),
        ('S', 'Scheduled')
    ]
    quiz_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='D')
    start = models.DateTimeField()
    duration = models.PositiveIntegerField(default=30)
    submissions = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return f"{self.title} - {self.author.username} ({self.created.strftime('%Y-%m-%d')})"
class Question(models.Model):
    TYPE_CHOICES = [
        ('MC', 'Multiple Choice'),
        ('SA', 'Short Answer')
    ]
    question_id = models.BigAutoField(primary_key=True)
    question_text = models.TextField()
    question_type = models.CharField(max_length=5, choices=TYPE_CHOICES, default='MC')
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    points = models.PositiveIntegerField(default=1)

    def get_answers(self):
        if self.question_type == 'MC' or self.question_type == 'Multiple Choice':
            return self.multiplechoiceanswer_set.all()
        return None
    class Meta:
        ordering = ['-question_id']
    def __str__(self):
        return f"{self.question_text}"


class MultipleChoiceAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


class ShortAnswer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    correct_answer = models.TextField()



