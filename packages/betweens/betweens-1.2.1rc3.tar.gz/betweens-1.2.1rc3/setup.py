from setuptools import setup, find_packages
# import betweens.python_ver_check
# 
# betweens.python_ver_check.check()
# 以上为失败的操作
from os import path
this_directory = path.abspath(path.dirname(__file__))
long_description = None
description = None
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(this_directory, 'new.txt'), encoding='utf-8') as f:
    description = f.read()

setup(name='betweens', # 包名称
      packages=find_packages(), # 需要处理的包目录
      version='1.2.1rc3', # 版本
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python', 'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: Common Public License',
          'License :: OSI Approved :: W3C License',
          'License :: OSI Approved :: Academic Free License (AFL)',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows :: Windows 8.1',
          'Operating System :: Microsoft :: Windows :: Windows 10',
          'Operating System :: Microsoft :: Windows :: Windows 11',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Environment :: Console',
          'Environment :: Console :: Curses',
          'Environment :: X11 Applications'
      ],
      description = description,
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='yuanbaoge', # 作者
      author_email='yuanbaoge@outlook.com', # 作者邮箱
      keywords='pimm source manager')
