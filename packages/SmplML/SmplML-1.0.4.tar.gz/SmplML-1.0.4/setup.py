from setuptools import setup, find_packages
 
# python setup.py sdist (for initial)

# python setup.py sdist bdist_wheel (for update)

# twine check dist/*
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Science/Research',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

desc = """SmplML is a user-friendly Python module for streamlined machine learning classification and regression. It offers intuitive functionality for data preprocessing, model training, and evaluation. Ideal for beginners and experts alike, SmplML simplifies ML tasks, enabling you to gain valuable insights from your data with ease."""
 
dependencies = ['pandas', 
                'numpy', 
                'scikit-learn']

setup(
  name='SmplML',
  version='1.0.4',
  description=desc,
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/JhunBrian/SmplML',  
  author='Jhun Brian Andam',
  author_email='andam.jhunbrian@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['Machine Learning', 'Classification', 'Regression'], 
  packages=find_packages(),
  install_requires=dependencies
)