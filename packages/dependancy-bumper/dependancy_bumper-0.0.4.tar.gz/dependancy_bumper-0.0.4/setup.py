import setuptools
import subprocess

# Get the version from git and save it:
package_version = subprocess.run(['git', 'describe', '--tags'], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
if "." not in package_version:
    package_version = "0.0.0"

# with open("dependancy-bumper/VERSION", "w+") as fh:
#     fh.write(str(package_version) + "\n")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dependancy_bumper",
    version=package_version,
    author="ASF Discovery Team",
    author_email="uaf-asf-discovery@alaska.edu",
    description="For testing pipelines with dependancy triggers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asfadmin/pip-updater-test.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[]
)