from setuptools import setup, find_packages
from pathlib import Path
import sys

this_directory = Path(__file__).parent

sys.path.insert(0, str(this_directory))
import langdash

long_description = (this_directory / "README.md").read_text()

setup(
    name='langdash',
    version=langdash.__version__,
    description='A simple library for interfacing with language models.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nana Mochizuki',
    author_email='nana@mysymphony.jp.net',
    url='https://git.mysymphony.jp.net/nana/langdash',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    project_urls={
        'Source': 'https://git.mysymphony.jp.net/nana/langdash',
        'Documentation': 'https://langdash.readthedocs.io/en/latest/',
    },
    # requirements
    python_requires='>=3.8',
    packages=find_packages(
        include=['langdash', 'langdash.*'], exclude=['extern']),
    install_requires=[
        'torch',
    ],
    extras_require={
        # Modules
        "embeddings": ["faiss-cpu"],

        # Backend
        "rwkv_cpp": ["tokenizers"],
        "llama_cpp": ["llama-cpp-python==0.1.57"],
        "transformers": ["transformers"],
        "sentence_transformers": ["sentence_transformers"],
    },
)
