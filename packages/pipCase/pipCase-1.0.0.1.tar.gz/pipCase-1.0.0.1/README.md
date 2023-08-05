# 说明
这是一个测试包
用cmd进入到该包中，执行以下代码，会自动找到
打包
python setup.py sdist bdist_wheel
安装打包工具
python -m pip install --upgrade setup 
https://pypi.org/

安装上传工具(专门负责上传到pip的)
python -m pip install --upgrade twine
或者
pip install --upgrade twine
