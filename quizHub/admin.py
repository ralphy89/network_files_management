from django.contrib import admin
from .models import Quiz, Question, MultipleChoiceAnswer, ShortAnswer, Submission, SubmissionAnswer
# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(MultipleChoiceAnswer)
admin.site.register(ShortAnswer)
admin.site.register(Submission)
admin.site.register(SubmissionAnswer)

