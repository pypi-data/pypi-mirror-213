# coding=utf-8
from .client import TTDataClient
from .version import __version__, version_info  # noqa
from .api import *  # noqa
from .utils import *


def auth(username, password, host=None, port=None):
    """账号认证"""
    TTDataClient.set_auth_params(host=host, port=port, username=username, password=password)


def auth_by_token(token, host=None, port=None):
    """使用 token 认证账号"""
    TTDataClient.set_auth_params(host=host, port=port, token=token)


@assert_auth
def submit(strategy_code: str, file_path: str = None, run_backtest: bool = False):
    """
    递交策略代码，并进行回测.

    :param strategy_code: 策略代号
    :param file_path: 策略文件路径，如果未指定，默认使用当前路径：<strategy_code>.py
    :param run_backtest: 递交成功后，是否马上执行回测
    :return:
    """
    kwargs = {"run_backtest": run_backtest}
    return TTDataClient.instance().submit(strategy_code=strategy_code, file_path=file_path, params=kwargs)


__all__ = [
    "auth",
    "__version__"
]
__all__.extend(api.__all__)  # noqa
