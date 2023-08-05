from setuptools import setup, find_packages


with open('metalayer/README.md', 'r') as f:
    long_description = f.read()

with open('metalayer/requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='auto-obsidian',
    version='0.1.3',
    packages=find_packages(),
    package_data={'metalayer.chatgpt': ['prompts/*/*.txt']},
    description="A layer on top of your OS that understands what you're doing",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ivan Yevenko',
    author_email='iyevenko@gmail.com',
    license='MIT',
    python_requires='>=3.8',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'metalayer=metalayer.main:main',
        ],
    },
)
