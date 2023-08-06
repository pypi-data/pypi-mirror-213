# from distutils.core import setup
from setuptools import setup, find_packages
setup(
  name = 'lztmarketapi',        
  packages = find_packages(),
  include_package_data=True,
  version = '0.2.1',    
  license='apache-2.0',      
  description = 'Данная библиотека создана для взаимодействия с api lzt.market.',   
  author = 'KazariFox',                  
  author_email = '',     
  url = 'https://github.com/KazariFox/AsyncMarketLztApi',   
  keywords = ['lzt', 'lolzteam', 'lolzteam market', 'api'],  
  install_requires=[           
          'pydantic',
          'httpx',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)