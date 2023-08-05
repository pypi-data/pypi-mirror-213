import setuptools

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="starmerx_url",
    version="0.1.3",
    author="yang",
    author_email="yangjuan@starmerx.com",
    description="starmerx verify url",
    license="MIT",
    url="",  # github
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        #"License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
    ],
    install_requires=[
    ],
    zip_safe=True,
)
