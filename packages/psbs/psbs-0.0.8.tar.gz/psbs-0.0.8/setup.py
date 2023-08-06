from setuptools import setup

setup(
    name='psbs',
    version='0.0.8',
    python_requires='>=3.8',
    description='PuzzleScript Build System',
    author='J.C. Miller',
    author_email='johncoreymiller@gmail.com',
    url='https://github.com/jcmiller11/PSBS',
    download_url = 'https://github.com/jcmiller11/PSBS/archive/refs/tags/0.0.8.tar.gz',
    license='MIT',
    packages=['psbs'],
    package_data={'': ['example.txt']},
    include_package_data=True,
    install_requires=[
        'jinja2',
        'pyyaml',
        'Pillow',
        'platformdirs'
    ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Software Development :: Build Tools'
    ],
    entry_points={
        'console_scripts': [
            'psbs=psbs.psbs:main'
        ],
    },
)