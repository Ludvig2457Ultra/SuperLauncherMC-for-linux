from setuptools import setup, find_packages

setup(
    name="superlauncher",
    version="2.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt6>=6.5",
        "requests>=2.28",
        "packaging>=23.0",
        "Pillow>=9.0",
        "pypresence>=4.3",
        "tqdm>=4.64",
    ],
    extras_require={
        "full": [
            "cryptography>=39.0",
            "PyJWT>=2.6",
            "psutil>=5.9",
            "minecraft_launcher_lib>=0.20",
        ],
    },
    entry_points={
        "console_scripts": [
            "superlauncher=SuperLauncher.__main__:main",
        ],
    },
    package_data={
        "SuperLauncher": ["assets/**/*"],
    },
    author="SuperLauncher Team",
    description="Minecraft launcher with mod support and server management",
    python_requires=">=3.10",
)
