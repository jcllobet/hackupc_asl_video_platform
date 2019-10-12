from django.db import models
from datetime import datetime

# Create your models here.
class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_content = models.TextField()
    tutorial_published = models.DateTimeField('date published', default=datetime.now)

    #we override the the __str__ special method to make it a bit more readable
    #when it's being displayed in string form, which we will see soon.
    def __str__(self):
        return self.tutorial_title
