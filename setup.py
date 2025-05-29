from setuptools import setup, find_packages

setup(
    name="linkedin_scraper",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["linkedin_scraper"],
    install_requires=[
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.9.0",
        "python-dotenv>=0.19.0",
        "playwright>=1.20.0",
        "asyncio>=3.4.3",
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'linkedin_scraper=linkedin_scraper.main:main',
        ],
    },
)
