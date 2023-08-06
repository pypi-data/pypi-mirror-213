from setuptools import setup

"""The setup script.
# 作者-上海悠悠 微信wx:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/
"""

setup(
    name='pytest-runtime-yoyo',
    url='https://gitee.com/yoyoketang/pytest-runtime-yoyo',
    version='v1.0.1',
    author="上海-悠悠",
    author_email='283340479@qq.com',
    description='run case mark timeout',
    long_description=open("README.rst", encoding='utf-8').read(),
    package_dir={"": "src"},
    packages=["pytest_runtime_yoyo"],
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.8',
    ],
    license='proprietary',
    keywords=[
        'pytest', 'py.test', 'pytest-runtime', 'pytest-runtime-yoyo',
    ],
    python_requires=">=3.8",
    install_requires=[
        'pytest>=7.2.0'
    ],
    entry_points={
        'pytest11': [
            'pytest-runtime-yoyo = pytest_runtime_yoyo.plugin',
        ]
    }
)
