from django.db import models


class LlmRecord(models.Model):
    llm_record_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    question_id = models.CharField(max_length=255)
    mode = models.IntegerField()
    upload_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'llm_record'


class Detail(models.Model):
    detail_id = models.AutoField(primary_key=True)
    llm_record_id = models.IntegerField()
    io_type = models.IntegerField()
    raw = models.TextField(null=True, blank=True)
    upload_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'llm_record_detail'
