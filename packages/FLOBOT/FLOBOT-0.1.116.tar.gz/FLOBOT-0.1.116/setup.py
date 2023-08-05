import setuptools
    
setuptools.setup(
    name="FLOBOT",
    version="0.1.116",
    author="Sekkay",
    description="Lobby bot.",
    url="https://www.youtube.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'crayons',
        'fortnitepy==3.6.8',
        'BenBotAsync',
        'FortniteAPIAsync',
        'uvloop',
        'sanic==21.6.2',
        'colorama',
        'aiohttp'
    ],
)
