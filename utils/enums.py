from enum import Enum


class StatusCodeEnum(Enum):
    """状态码枚举类"""

    OK = (0, 200, '成功')
    OTHER_ERROR = (-1, 400, '未知异常')
    SERVER_ERR = (500, 500, '服务器异常')

    METHOD_ERR = (1, 400, 'http方法错误')
    PASSWORD_BLANK_ERR = (2, 400, '密码不能为空')
    PASSWORD_WRONG_ERR = (3, 400, '密码错误')
    USER_EXIST_ERR = (4, 400, '用户名已存在')
    USER_NOT_EXIST_ERR = (5, 400, '用户不存在')
    PARAM_ERR = (6, 400, '参数错误')
    ACCOUNT_ERR = (10, 400, '账号错误')
    CODE_INFO_ERR = (11, 400, '代码信息错误')

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def status(self):
        """获取状态码"""
        return self.value[1]

    @property
    def errmsg(self):
        """获取状态码信息"""
        return self.value[2]
