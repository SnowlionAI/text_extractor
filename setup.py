from setuptools import setup, find_packages

setup(
    name="text_extractor",
    version="1.0",
    packages=find_packages(),
    install_requires=["openai", "python-dotenv"],
    entry_points={
        "console_scripts": [
            "text-extractor=text_extractor.cli:main",
        ],
    },
    author="Your Name",
    description="A tool to extract and replace hardcoded texts with a translation function",
    url="https://github.com/yourgithub/text-extractor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
