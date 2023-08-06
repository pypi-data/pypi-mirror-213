import setuptools,defy

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DefyDatabase",
    version=defy.version,
    author="Defymen",
    author_email="vmuonline@126.com",
    description="Database for personal data based on SQLite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['defy'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
six_classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]
