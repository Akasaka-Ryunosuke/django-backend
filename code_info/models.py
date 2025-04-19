from django.db import models


class CodeInfo(models.Model):
    code_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    question_id = models.IntegerField()
    code_raw = models.CharField(max_length=255, blank=True)
    code_type = models.CharField(max_length=255)
    score = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    run_time = models.IntegerField()
    upload_time = models.DateTimeField()

    class Meta:
        db_table = 'code_info'
