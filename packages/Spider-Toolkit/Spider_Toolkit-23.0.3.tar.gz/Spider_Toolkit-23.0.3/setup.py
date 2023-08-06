from setuptools import setup, find_packages

setup(
    # 以下为必需参数
    name='Spider_Toolkit',  # 模块名
    version='23.0.3',  # 当前版本
    description='爬虫辅助模块',  # 简短描述
    packages=find_packages(),  # 多文件模块写法 exclude=['contrib', 'docs', 'tests']
    # 以下均为可选参数
    long_description="爬虫辅助模块0.0.3版本修复了bug",  # 长描述
    url='https://github.com/pypa/sampleproject',  # 主页链接
    author='Uncle_Ming',  # 作者名
    author_email='2462711716@qq.com',  # 作者邮箱
    classifiers=[
        'Development Status :: 1 - Planning',  # 当前开发进度等级（测试版，正式版等）
        'License :: OSI Approved :: MIT License',  # 模块的license
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='tools spider requests download',  # 模块的关键词，使用空格分割
    install_requires=['requests','pandas','PyExecJS','pymysql','redis','pymongo'],  # 依赖模块
    # extras_require={  # 分组依赖模块，可使用pip install sampleproject[dev] 安装分组内的依赖
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
    # package_data={  # 模块所需的额外文件
    #     'sample': ['package_data.dat'],
    # },
    # data_files=[('my_data', ['data/data_file'])],  # 类似package_data, 但指定不在当前包目录下的文件
    # entry_points={  # 新建终端命令并链接到模块函数
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
    # project_urls={  # 项目相关的额外链接
    #     'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
    #     'Funding': 'https://donate.pypi.org',
    #     'Say Thanks!': 'http://saythanks.io/to/example',
    #     'Source': 'https://github.com/pypa/sampleproject/',
    # },
)
