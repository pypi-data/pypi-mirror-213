# python-sdk
打包方法：
1. python setup.py bdist_egg    
2. 之后将整个目录打包发给调用方

安装和使用SDK：
1. 解压，进入主目录下
2. python setup.py install 安装
3. import plateNumOCR，然后运行plateNumOCR.demo()函数，参数是待识别图片的路径，输出识别的车牌结果
