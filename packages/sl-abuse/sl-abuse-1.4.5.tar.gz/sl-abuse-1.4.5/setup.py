from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="sl-abuse",
    version="1.4.5",
    description="",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/shehan9909/whatsapp",
    author="shehan_slahiru",
    author_email="www.shehan6472@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["sl_abuse"],
    include_package_data=True,
    install_requires=["twilio"],
    entry_points={
        "console_scripts": [
            "sl-abuse=sl_abuse.__main__:main",
        ]
    },
)
