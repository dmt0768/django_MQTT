from django.db import models


class Types(models.Model):
    type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, unique=True)
    

class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    type_id = models.ForeignKey(Types, db_column='topic_id', on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=300)
    time = models.CharField(max_length=300, default='None')
