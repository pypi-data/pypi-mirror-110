from setuptools import setup, find_packages
long_des = '''
```py
from handspell.handspell import spell_check as check
print(check('text'))
'''
setup(
    name='korean_handspellpy',
    version='1.0.5',
    description='handspell',
    license='MIT',
    author='hminkoo10',
    author_email='hmin.koo10@gmail.com',
    long_description=long_des,
    long_description_content_type='text/markdown',

    install_requires=[],

    packages=[],
    keywords=['맞춤법 검사','맞춥법','handspell','koreanhandspell','korean'],

    python_requires='>=3'
)
