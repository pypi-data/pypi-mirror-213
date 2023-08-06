#sotest-utils-python
`sotest-utils-python`是提供给sotest平台用户自定义python函数所使用的辅助包，内置了打印、断言、加锁等一系列函数

###打包发布方法

1. 
2. 修改代码并更新`setup.py`中的版本号 
3. 执行`python3 setup.py sdist build`打包代码
4. 执行`twine upload dist/* --config-file .pypirc`上传打包的代码到pypi