from setuptools import setup, find_packages

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='maryChain',                           # should match the package folder
    version='0.0.1',                                # important for updates
    license='MIT',                                  # should match your chosen license
    description='maryChain - lightweight programming functional language for LLM',
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Alessio Ricco',
    author_email='alessio.ricco@gmail.com',
    url='https://github.com/alessioricco/maryChain', 
    project_urls = {                                # Optional
        "Bug Tracker": "https://github.com/alessioricco/maryChain/issues"
    },
    keywords=["pypi", "maryChain", "programming language", "functional", "ai", "llm"], #descriptive meta-data
    packages=find_packages(),
    classifiers=[                                   # https://pypi.org/classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Interpreters',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "ply",
    ],   
    download_url="https://github.com/DashyDashOrg/pandas-llm/releases/tag/v0.0.6",
)