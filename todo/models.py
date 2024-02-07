from django.db import models

# Create your models here.


class Todo(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    priority = models.IntegerField(default=1)
    is_done = models.BooleanField()

    def __str__(self):
        return f'{self.title} / is done :{self.is_done}'

    class Meta:
        db_table = 'todos'

