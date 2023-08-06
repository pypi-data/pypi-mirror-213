from setuptools import setup

setup(
    name='generate_doc',
    version='1.0',
    packages=['generate_doc'],
    entry_points={
        'console_scripts': [
            'generate_doc = generate_doc.generate_doc:add_descriptions_to_functions',
        ],
    },
    install_requires=[
        'aiohttp==3.8.4',
        'aiosignal==1.3.1',
        'async-timeout==4.0.2',
        'attrs==23.1.0',
        'certifi==2023.5.7',
        'charset-normalizer==3.1.0',
        'frozenlist==1.3.3',
        'idna==3.4',
        'multidict==6.0.4',
        'numpy==1.24.3',
        'openai==0.27.8',
        'python-dotenv==1.0.0',
        'requests==2.31.0',
        'tqdm==4.65.0',
        'urllib3==2.0.3',
        'yarl==1.9.2',
    ],
)
