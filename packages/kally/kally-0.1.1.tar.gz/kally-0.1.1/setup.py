from setuptools import setup, find_packages

setup(
    name="kally",
    version="0.1.1",
    license='MIT',
    description="This is a clustering algorithm created based on the philosophy of competition for alliances, against the backdrop of the events of struggle for allies between warring countries. Especially the Russian-Ukrainian war.",
    author="Aslan Alwi and Munirah",
    author_email="elangbijak4@email.com",
    url="https://github.com/elangbijak4/k-ally.1.0/blob/main/k-ally.1.0",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    #packages=["kally"],
    install_requires=[
          'pandas',
          'numpy'
      ],

)