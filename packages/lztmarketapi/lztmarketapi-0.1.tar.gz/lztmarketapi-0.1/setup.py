from distutils.core import setup
setup(
  name = 'lztmarketapi',        
  packages = ['lztmarketapi'],  
  version = '0.1',    
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