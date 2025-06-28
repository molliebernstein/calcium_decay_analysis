from setuptools import setup

setup(
    name="calcium_decay_analysis",
    version="0.1.0",
    py_modules=["preprocess", "calcium_decay_analysis"],
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
    ],
    entry_points={
        "console_scripts": [
            "preprocess-traces=preprocess:cli",
            "calcium-decay=calcium_decay_analysis:cli",
        ]
    },
)
