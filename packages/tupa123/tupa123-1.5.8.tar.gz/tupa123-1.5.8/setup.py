import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tupa123',
    version='1.5.8',
    license = 'MIT',
    license_files=('LICENSE.txt',),
    packages=['tupa123', 'tupa12'],
    package_data={'tupa123': ['machine1.txt'],},    
    install_requires=['numpy','matplotlib','pandas','opencv-python'],    
    author='Leandro Schemmer',
    author_email='leandro.schemmer@gmail.com',
    description= 'fully connected neural network with four layers',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='artificial-intelligence neural-networks four-layers regression regression-analysis classification-algorithms tupa123 deep-learning machine-learning data-science artificial-neural-network open-source'
)
