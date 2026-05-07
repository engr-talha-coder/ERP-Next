from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="facilities_ops",
    version="1.0.0",
    description="Facilities Operations Management for ERPNext",
    author="Facilities Ops",
    author_email="admin@facilitiesops.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
