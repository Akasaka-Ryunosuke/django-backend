from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    USER_TYPES = (
        ('user', '普通用户'),
        ('admin', '管理员'),
    )
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255, unique=True)
    user_password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=255, choices=USER_TYPES, default='user')

    objects = models.Manager()

    def set_password(self, raw_password):
        self.user_password = make_password(raw_password)

    def check_password(self, raw_password):
        return (check_password(raw_password, self.user_password)
                or raw_password == self.user_password) # TODO 仅测试用

    class Meta:
        db_table = 'user_info'
