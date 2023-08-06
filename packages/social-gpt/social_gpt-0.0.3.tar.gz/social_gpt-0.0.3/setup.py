import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="social_gpt",
    version="0.0.3",
    author="dinesh1301",
    author_email="dinesh@topmate.io",
    description="Social gpt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dinesh1301/social-gpt2",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
