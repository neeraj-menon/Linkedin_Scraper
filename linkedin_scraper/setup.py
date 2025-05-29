from setuptools import setup, find_packages

setup(
    name="linkedin-scraper",
    version="0.1.0",
    package_dir={"":"src"},  # Tell setuptools packages are under src
    packages=find_packages(where="src"),  # Find packages in src directory
    install_requires=[
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.9.0",
        "python-dotenv>=0.19.0",
        "playwright>=1.20.0",
        "asyncio>=3.4.3",
    ],
)
