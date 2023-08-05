from setuptools import setup, find_packages
setup(
    name='Bgolearn',  # 包名
    version='2.1.1',  # 版本
    description="A Bayesian global optimization package for material design",  # 包简介
    long_description=open('README.md',encoding='utf-8').read(),  # 读取文件中介绍包的详细内容
    include_package_data=True,  # 是否允许上传资源文件
    author='CaoBin',  # 作者
    author_email='bcao@shu.edu.com',  # 作者邮件
    maintainer='CaoBin',  # 维护者
    maintainer_email='binjacobcao@gmail.com',  # 维护者邮件
    license='MIT License',  # 协议
    url='https://github.com/Bin-Cao/Bgolearn',  # github或者自己的网站地址
    packages=find_packages(include=['Bgolearn', 'Bgolearn.*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # 设置编写时的python版本
    ],
    python_requires='>=3.5',  # 设置python版本要求
    install_requires=['scipy','scikit-learn','pandas','numpy','matplotlib'],  # 安装所需要的库
    entry_points={
        'console_scripts': [
            ''],
    },  # 设置命令行工具(可不使用就可以注释掉)

)
