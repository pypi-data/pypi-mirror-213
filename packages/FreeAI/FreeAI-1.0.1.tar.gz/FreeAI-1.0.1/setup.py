from setuptools import setup, find_packages

setup(
    name='FreeAI',
    version='1.0.0',
    author='Ashiq Hussain',
    author_email='imseldrith@gmail.com',
    description='FreeAI is a powerful Python package that utilizes the advanced capabilities of GPT (Generative Pre-trained Transformer) models for text generation. It allows users to generate creative and context-aware text based on a given prompt. Whether you need to generate code snippets, creative writing pieces, or technical documentation, FreeAI has got you covered.',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)
