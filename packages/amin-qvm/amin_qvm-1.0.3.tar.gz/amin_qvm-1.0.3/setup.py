import twine
from setuptools import setup, find_packages

# reading long description from file
with open('DESCRIPTION.rst') as file:
	long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = [
    'numpy',
    're',
    'random',
    'itertools',
    'functools',
    'math',
    'time',
    'qiskit',
    'pennylane',
    'scikit-learn',
    'unittest'
]
setup(
    name='amin_qvm',
    version='1.0.3',
    author='Amin Alogaili',
    author_email='aminalogai@gmail.com',
    description='Amin-QVM: Quantum Computing Library',
    long_description=long_description,
    url='https://github.com/amin1029384756/QVM',
    packages=['amin_qvm'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='quantum computing library simulation amin alogaili QVM aminalogaili',
    install_requires=REQUIREMENTS,
    python_requires='>=3.4',
)
