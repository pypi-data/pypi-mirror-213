# -*- coding:utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name="spacetool",
    version="1.0.7",
    description='space.top的数据管理工具',
    author="Leo Ni",
    author_email="nij6173@gmail.com",
    url='http://space.top/',
    packages=find_packages(),
    install_requires=["requests", "cos-python-sdk-v5"],
    python_requires=">=3.6,<3.11",
    keywords=['data', "spacedata"],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


# setup(name='spacetool',
#         version='0.1',
#         packages=find_packages(where='src\\'),  # 查找包的路径
#         package_dir={'': 'src'},  # 包的root路径映射到的实际路径
#         include_package_data=False,
#         package_data={'data': []},
#         description='A python lib for xxxxx',
#         long_description='',
#         author='python developer',
#         author_email='xxxxxxx@qq.com',
#         url='http://www.xxxxx.com/',  # homepage
#         license='MIT',
#         install_requires=['requests', 'selenium', 'baidu-aip', 'pillow', 'pywin32'],
#         )
# name : 打包后包的文件名
# version : 版本号
# author : 作者
# author_email : 作者的邮箱
# py_modules : 要打包的.py文件
# packages: 打包的python文件夹
# include_package_data : 项目里会有一些非py文件,比如html和js等,这时候就要靠include_package_data 和 package_data 来指定了。package_data:一般写成{‘your_package_name’: [“files”]}, include_package_data还没完,还需要修改MANIFEST.in文件.MANIFEST.in文件的语法为: include xxx/xxx/xxx/.ini/(所有以.ini结尾的文件,也可以直接指定文件名)
# license : 支持的开源协议
# description : 对项目简短的一个形容
# ext_modules : 是一个包含Extension实例的列表,Extension的定义也有一些参数。
# ext_package : 定义extension的相对路径
# requires : 定义依赖哪些模块
# provides : 定义可以为哪些模块提供依赖
# data_files :指定其他的一些文件(如配置文件),规定了哪些文件被安装到哪些目录中。如果目录名是相对路径,则是相对于sys.prefix或sys.exec_prefix的路径。如果没有提供模板,会被添加到MANIFEST文件中。

# python3 setup.py sdist
# twine upload dist/*


