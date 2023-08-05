import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Kyak2-systemd",
    version="0.3.3",
    author="UnbalancedSkunk",
    author_email="turkishanhur@gmail.com",
    description="Openbox(WM-Window Manager) Logout screen with Tkinter, for users who use systemd \n ",
    license="GPLv3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UnbalancedSkunk/Kyak2",
    project_urls={
        "Bug Tracker": "https://github.com/UnbalancedSkunk/Kyak2",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)