import pytest
from pytest import Module


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    out = yield
    # 获取测试报告
    report = out.get_result()
    if report.when == 'call' and report.outcome == 'passed':
        # 获取命令行 ini 配置的 runtime 参数
        config_run_time = item.__dict__['_request'].config.option.runtime
        config_run_time = float(config_run_time) if config_run_time else 0
        if isinstance(item.parent, Module):
            # 父类是 Module
            own_markers = item.__dict__['own_markers'] or item.parent.__dict__['own_markers']
        else:
            # 父类是 Class
            own_markers = item.__dict__['own_markers'] or item.parent.__dict__['own_markers'] or item.parent.parent.__dict__['own_markers']
        run_time_mark = [mark.__dict__['args'][0] for mark in own_markers if mark.__dict__.get('name') == 'runtime']
        run_time_args = run_time_mark[0] if run_time_mark else config_run_time
        if run_time_args and report.duration > run_time_args:
            report.outcome = "failed"


def pytest_addoption(parser):   # noqa
    parser.addini('runtime', default=None, help='run case timeout...')
    parser.addoption(
        "--runtime", action="store", default=None, help="run case timeout..."
    )


def pytest_configure(config):  # noqa
    config.addinivalue_line(
        "markers", "runtime: run timeout"
    )
    run_time = config.getoption("--runtime") or config.getini("runtime")
    if run_time is not None:
        config.option.runtime = run_time
