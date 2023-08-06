from setuptools import setup, find_packages

setup(name='client_chat_pyqt_T101',
      version='0.2',
      description='Client packet',
      packages=find_packages(),  # ,Будем искать пакеты тут(включаем авто поиск пакетов)
      author_email='nicola@mail.ru',
      author='Jackie Chan',
      #install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      # зависимости которые нужно до установить
      )
