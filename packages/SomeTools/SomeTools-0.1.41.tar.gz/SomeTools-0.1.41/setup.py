from setuptools import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='SomeTools',
      version='0.1.41',
      description="Some python tools",
      author="zhangkun",
      author_email="zk.kyle@foxmail.com",
      project_urls={
          'Documentation': 'https://github.com/584807419/SomeTools',
          'Funding': 'https://github.com/584807419/SomeTools',
          'Source': 'https://github.com/584807419/SomeTools',
          'Tracker': 'https://github.com/584807419/SomeTools',
      },
      keywords=("Python", "Tools"),
      license='',
      long_description=long_description,  # 包的详细介绍，一般在README.md文件内
      long_description_content_type="text/markdown",
      url="https://pypi.org/project/SomeTools/",  # 自己项目地址，比如github的项目地址
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.8',  # 对python的最低版本要求
      packages=find_packages(),
      install_requires=[
          # "orjson",  # 底层使用了rust，Python下最快的json库,比 ujson 快 3 倍，比 json 快 6 倍
          "aiomysql==0.1.1",
          "aioredis==2.0.1",
          "async-timeout==4.0.2",
          "bleach==6.0.0",
          "certifi==2023.5.7",
          "chardet==5.1.0",
          "charset-normalizer==3.1.0",
          "colorama==0.4.6",
          "DateTime==5.1",
          "DBUtils==3.0.3",
          "docutils==0.20.1",
          "idna==3.4",
          "importlib-metadata==6.6.0",
          "jaraco.classes==3.2.3",
          "keyring==23.13.1",
          "loguru==0.7.0",  # 高效优雅的日志显示
          "lxml==4.9.2",
          "markdown-it-py==2.2.0",
          "mdurl==0.1.2",
          "more-itertools==9.1.0",
          "mysqlclient",  # dependency_library/windows/mysqlclient-2.1.1-cp39-cp39-win_amd64.whl
          "opencc-python-reimplemented==0.1.7",  # 繁体简体转换
          "Pillow",  # dependency_library/windows/Pillow-9.5.0-cp39-cp39-win_amd64.whl
          "pkginfo==1.9.6",
          "psutil==5.9.5",
          "pyasn1==0.5.0",
          "pycryptodome==3.18.0",
          "Pygments==2.15.1",
          "pytz==2023.3",
          "pywin32-ctypes==0.2.0",
          "readme-renderer==37.3",
          "redis==4.5.5",
          "requests==2.31.0",
          "requests-toolbelt==1.0.0",
          "rfc3986==2.0.0",
          "rich==13.4.1",
          "rsa==4.9",
          "six==1.16.0",
          "twine==4.0.2",
          "typing_extensions==4.6.3",
          "urllib3==2.0.3",
          "webencodings==0.5.1",
          "win32-setctime==1.1.0",
          "zipp==3.15.0",
          "zope.interface==6.0",

      ],
      py_modules=['sometools'],
      include_package_data=True,
      platforms="any",
      scripts=[],
      )

# 上传pypi
# python -m pip install --upgrade twine
# python -m twine upload --repository pypi dist/*

# 打包
# https://blog.csdn.net/yifengchaoran/article/details/113447773
# python -m pip install --upgrade pip
# python -m pip install  --upgrade setuptools wheel
# python setup.py sdist bdist_wheel
