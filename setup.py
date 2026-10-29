"""
Copyright 2026 Chronos-ID Sovereign Identity Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import setup, find_packages

setup(
    name="chronos-id",
    version="1.0.0",
    description="Post-Quantum Sovereign Passport, Lattice Cryptography & Zero-Knowledge Personhood for Pi Network",
    author="Chronos-ID Sovereign Identity Contributors",
    author_email="identity@chronos-id.io",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "chronos-id=chronos_id.cli.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
)
