from django.db import models

class QuestionInfo(models.Model):
    question_id = models.CharField(max_length=255, primary_key=True)
    question_raw = models.CharField(max_length=255, null=True, blank=True)
    checkpoints_count = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'question_info'  # 指定数据库中的表名

    def __str__(self):
        return self.question_id