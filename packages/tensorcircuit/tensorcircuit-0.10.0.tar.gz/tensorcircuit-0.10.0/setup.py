import setuptools

from tensorcircuit import __version__, __author__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="tensorcircuit",
    version=__version__,
    author=__author__,
    author_email="shixinzhang@tencent.com",
    description="High performance unified quantum computing framework for the NISQ era",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tencent-quantum-lab/tensorcircuit",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["numpy", "scipy", "tensornetwork", "networkx"],
    extras_require={
        "tensorflow": ["tensorflow"],
        "jax": ["jax", "jaxlib"],
        "torch": ["torch"],
        "qiskit": ["qiskit"],
        "cloud": ["qiskit", "mthree"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
