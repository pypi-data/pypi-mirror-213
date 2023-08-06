from setuptools import setup, Extension, find_packages
from os import environ
import os

if environ.get('CC') and 'clang' in environ['CC']:
    # clang
    extra_compile_args = ['-fopenmp=libomp']
    extra_link_args = ['-fopenmp=libomp']
else:
    # GNU
    extra_compile_args = ['-fopenmp']
    extra_link_args = ['-fopenmp']

MOD1 = 'kssd'
MOD2 = 'quicktree'
sources1 = ['co2mco.c',
            'iseq2comem.c',
            'command_dist_wrapper.c',
            'mytime.c',
            'global_basic.c',
            'command_dist.c',
            'command_shuffle.c',
            'command_set.c',
            'command_reverse.c',
            'command_composite.c',
            'pykssd.c']
sources2 = ['pyquicktree.c',
            'align.c',
            'cluster.c',
            'distancemat.c',
            'util.c',
            'tree.c',
            'buildtree.c',
            'sequence.c']
include_dirs1 = ['kssdheaders']
include_dirs2 = ['quicktreeheaders']

setup(
    name='kssdtree',
    version='1.0.0',
    author='yanghang',
    author_email='1090692248@qq.com',
    description='',
    url='',
    download_url='',
    ext_modules=[
        Extension(MOD1, sources=sources1, include_dirs=include_dirs1,
                  extra_compile_args=extra_compile_args,
                  extra_link_args=extra_link_args),
        Extension(MOD2, sources=sources2, include_dirs=include_dirs2)
    ],
    py_modules=['main', 'create_distance_matrix', 'kssdtree'],
    entry_points={
        "console_scripts": [
            "kssdtree = main:main",
        ]
    },
    packages=find_packages(),
    package_data={
        'kssdtree': ['kssdheaders/*.h', 'quicktreeheaders/*.h']
    },
    data_files=[
        ('/kssdtree/shuf_files', ['shuf_files/L2K8.shuf', 'shuf_files/L3K8.shuf'])
    ],
    install_requires=[
        'pandas>=1.3.5',
        'ete3>=3.1.3',
    ],
)

# python3 setup.py sdist bdist_wheel
# python3 -m twine upload kssdtree-0.0.0.tar.gz
