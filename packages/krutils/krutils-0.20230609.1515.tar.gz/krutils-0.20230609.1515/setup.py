import setuptools

setuptools.setup(
    name="krutils",
    version="0.20230609.1515",
    author="bonfireof",
    author_email="bonfireof@gmail.com",
    description="Some utils for me.",
    project_urls={
        "Bug Tracker": "https://github.com/bonfireof/krutils",
        "Documentation": "https://github.com/bonfireof/krutils",
        "Source Code": "https://github.com/bonfireof/krutils",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    # package_dir={"": "krutils"},
    # packages=setuptools.find_packages(where="krutils"),
    package_dir={"krutils": "krutils"},
    packages=["krutils"],
    python_requires=">=3.0",
    install_requires=[
        "PyMySQL>=1.0.3",
        'python-telegram-bot'
    ]
)
