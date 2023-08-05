import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UzEduCorpus",
    version="0.0.4",
    author="Muhayyo Narimonova",
    author_email="muhayyonarimonova1797@gmail.com",
    description="Uzbek language Educational Corpus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://uzedu.uz/uz",
    project_urls={
        "Bug Tracker": "https://uzedu.uz/uz",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['python', 'uzbek-language', 'latin'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={"": ["*.csv"]},
)