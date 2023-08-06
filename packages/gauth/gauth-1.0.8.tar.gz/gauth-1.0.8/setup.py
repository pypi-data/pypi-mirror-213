from setuptools import setup
with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read().splitlines()
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gauth",
    version="1.0.8",
    license='MIT',
    description="Tool to help migrate Google Authenticator from phone to desktop",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Damon Yuan",
    author_email="damon.yuan.dev@gmail.com",
    url="https://github.com/damonYuan/gauth",
    packages=['gauth', 'gauth.extract', 'gauth.extract.protobuf_generated_python'],
    include_package_data=True,
    entry_points="""
    [console_scripts]
    gauth = gauth.main:main
    """,
    install_requires=REQUIREMENTS,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6"
)