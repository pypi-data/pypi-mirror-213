from setuptools import setup

setup(
    name='essenceApi',
    version='4.2',
    author='Toyota',
    description='Библиотка для использования анти краша',
    packages=['apiessence'],  # Укажите здесь название пакета, содержащего вашу библиотеку
    install_requires=[  # Укажите здесь зависимости вашей библиотеки, если они есть
        'requests'
    ],
)
