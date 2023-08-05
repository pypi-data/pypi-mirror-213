from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='aries_lib',
    version='5.4.0',
    license='MIT License',
    author='Luan Souza',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='piitszkdev@outlook.com',
    keywords=['mercado pago', 'mercado', 'banco', 'sql', 'mysql', 'banco de dados', 'python', 'bot', 'discord', 'connection'],
    description=u'Biblioteca contendo sistemas importantes pra desenvolvimento',
    packages=['aries_lib'],
    install_requires=['mysql-connector-python', 'mercadopago']
)