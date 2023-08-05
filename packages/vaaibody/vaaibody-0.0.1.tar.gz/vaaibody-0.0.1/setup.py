from setuptools import setup, find_packages
from os.path import basename, splitext
from glob import glob

setup(
    name='vaaibody', # 패키지 명
    version='0.0.1',
    description='VAAI-BODY gesture generation module',
    author='yoonhee',
    author_email='yhkim@ncsoft.com',
    py_modules=[splitext(basename(path))[0] for path in glob('source/*.py')],
    packages=find_packages(where='source', exclude=['*.depricated', 'depricated', '*.depricated.*', '*.testing']),
    python_requires='>=3.8',
    package_dir={'': 'source'},
    install_requires=[
        'numpy==1.23.4',
        'scipy==1.9.2'
        ], # 패키지 사용을 위해 필요한 추가 설치 패키지
)