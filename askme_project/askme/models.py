#from django.db import models

# Create your models here.
QUESTIONS = [
    {
        'id': i,
        'title': f'Question Title {i + 1}',
        'text': f'Text of question {i + 1}',
    } for i in range(6)
]