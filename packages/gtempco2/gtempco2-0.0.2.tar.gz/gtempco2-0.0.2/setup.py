import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gtempco2",
    version="0.0.2",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="A package for displaying global temperature and co2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ytakefuji/gtempco2",
    project_urls={
        "Bug Tracker": "https://github.com/ytakefuji/gtempco2",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['gtempco2'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'gtempco2 = gtempco2:main'
        ]
    },
)
