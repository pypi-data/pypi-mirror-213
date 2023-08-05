from setuptools import setup


version = '0.0.1'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='counter_solo_elements',
    version=version,

    author='OlexandrTsubera',
    author_email='bolshoygrizli@gmail.com',

    description='Tells how many elements are found only 1 time',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://git.foxminded.ua/foxstudent105136/task-4/-/merge_requests/2',

    packages=['counter_solo_elements'],
)
