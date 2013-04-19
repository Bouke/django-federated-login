from django.db import models


class Association(models.Model):
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField(db_index=True)
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        unique_together = ('server_url', 'handle')


class Nonce(models.Model):
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField(db_index=True)
    salt = models.CharField(max_length=40)

    class Meta:
        unique_together = ('server_url', 'timestamp', 'salt')
