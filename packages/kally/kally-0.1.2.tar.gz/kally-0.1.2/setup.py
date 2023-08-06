from setuptools import setup, find_packages

setup(
    name="kally",
    version="0.1.2",
    license='MIT',
    description="This is a clustering algorithm created based on the philosophy of competition for alliances, against the backdrop of the events of struggle for allies between warring countries. Especially the Russian-Ukrainian war.",
    author="Aslan Alwi and Munirah",
    author_email="elangbijak4@email.com",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/elangbijak4/k-ally.1.0/blob/main/k-ally.1.0",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
          'pandas',
          'numpy'
      ],

)