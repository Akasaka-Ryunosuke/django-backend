from django.db import models

class CodeInfo(models.Model):
    code_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    question_id = models.IntegerField(blank=True, null=True)
    code_raw = models.CharField(max_length=255, blank=True, null=True)
    code_type = models.CharField(max_length=255, blank=True, null=True)
    score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    run_time = models.IntegerField(blank=True, null=True)
    upload_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'code_info'