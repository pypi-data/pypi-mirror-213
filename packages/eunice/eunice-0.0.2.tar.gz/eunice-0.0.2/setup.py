from setuptools import setup


VERSION = "0.0.2"


with open("README.md") as f:
    readme = f.read()


setup(
    name="eunice",
    version=VERSION,
    description="eunice - a simple chatgpt cli wrapper",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="http://github.com/rob-parker-what/eunice",
    author="rob-parker-what",
    author_email="robparkerwhat.dev@gmail.com",
    license="MIT",
    packages=["eunice"],
    entry_points={
        "console_scripts": ["eunice=eunice.cmdline:main"],
    },
    install_requires=[
        "openai",
        "tomli"
    ],
    zip_safe=False,
    python_requires=">=3.8",
    keywords="chatgpt, ai, openai",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
)