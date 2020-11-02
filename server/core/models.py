from django.db import models


class Topics(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=100, unique=True)
    

class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    topic_id = models.ForeignKey(Topics, db_column='topic_id', on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=300)
    time = models.CharField(max_length=300, default='None')
