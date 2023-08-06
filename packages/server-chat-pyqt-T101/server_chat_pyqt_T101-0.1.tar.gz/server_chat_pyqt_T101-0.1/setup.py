from setuptools import setup, find_packages

setup(name='server_chat_pyqt_T101',
      version='0.1',
      description='Server package',
      packages=find_packages(),  # Будем искать пакеты тут(включаем авто поиск пакетов)
      author_email='test@mail.ru',
      author='Jackie Chan',
      # install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      # зависимости которые нужно до установить
      )
