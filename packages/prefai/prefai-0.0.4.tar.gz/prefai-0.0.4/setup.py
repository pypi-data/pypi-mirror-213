from setuptools import setup, find_packages

setup(
    name="prefai",
    version="0.0.4",
    packages=find_packages(),
    author="Bobby Jaros",
    author_email="bobby@pref.ai",
    description="A brief description of your package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="http://github.com/prefai/pythonclient",
    license='LICENSE.txt',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        # Add your project dependencies here
    ],
    python_requires='>=3.6',
    include_package_data=True
)
