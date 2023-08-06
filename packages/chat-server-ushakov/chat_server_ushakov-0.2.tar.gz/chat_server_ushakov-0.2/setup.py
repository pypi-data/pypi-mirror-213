from setuptools import setup, find_packages

setup(name='chat_server_ushakov',
      version='0.2',
      description='Server packet',
      packages=find_packages(),  # ,Будем искать пакеты тут(включаем авто поиск пакетов)
      author_email='ushakov.ip@yandex.ru',
      author='Dmitry Ushakov',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      # зависимости которые нужно до установить
      )