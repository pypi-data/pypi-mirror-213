from setuptools import setup, find_packages

setup(name='GTNLib',
      version='0.1',
      author="KeyDevS",
      packages=find_packages(),
      description='Lib for project Guess The Number by KeyDevS (KeyDevelops)',
      author_email='rumaevvadim@gmail.com',
      install_requires=[
        'requests',
      ],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
      zip_safe=False)