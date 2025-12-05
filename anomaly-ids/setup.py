from setuptools import setup, find_packages

setup(
    name="anomaly_detector",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "click"
    ],
    entry_points={
        "console_scripts": [
            "anomaly-detect=anomaly_detector.cli:cli"
        ]
    }
)
