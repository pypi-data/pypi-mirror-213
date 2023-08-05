from setuptools import setup, find_packages

setup(
    name="bert_pruners",
    version="0.0.5",
    author="xihajun",
    author_email="junfan@krai.ai",
    description="Pruning BERT models",
    url="https://github.com/xihajun/bert_pruners",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'torch',
        'transformers',
        'onnx'
    ],
    entry_points={
        'console_scripts': [
            'bert_prune=bert_pruners.main:main',
        ],
    },
)
