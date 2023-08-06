import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NinjaTools",
    version="0.67",
    author="Nikko Gonzales",
    author_email="nikkoxgonzales@gmail.com",
    description="Bunch of useful tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nikkoxgonzales/ninja-tools",
    extras_require={
        'image': [
            'opencv-python==4.5.5.62',
            'scikit-image>=0.19.2',
            'numpy>=1.18.5',
        ],

        'memory': [
            'Pymem[speed]>=1.10.0'
        ],

        'excel': [
            'openpyxl>=3.0.10',
            'webcolors>=1.12'
        ],

        'web': [
            'beautifulsoup4>=4.11.1',
            'bs4>=0.0.1',
            'certifi>=2022.9.24',
            'charset-normalizer>=2.1.1',
            'colorama>=0.4.6',
            'idna>=3.4',
            'requests>=2.28.1',
            'soupsieve>=2.3.2.post1',
            'urllib3>=1.26.12',
        ],

        'all': [
            'opencv-python==4.5.5.62',
            'scikit-image>=0.19.2',
            'openpyxl>=3.0.10',
            'webcolors>=1.12',
            'numpy>=1.22.3',
            'Pymem>=1.8.5',
            'pywin32>=303',
            'pyperclip>=1.8.2',
            'psutil>=5.9.0',
            'pyserial>=3.5',
            'beautifulsoup4>=4.11.1',
            'bs4>=0.0.1',
            'certifi>=2022.9.24',
            'charset-normalizer>=2.1.1',
            'colorama>=0.4.6',
            'idna>=3.4',
            'requests>=2.28.1',
            'soupsieve>=2.3.2.post1',
            'urllib3>=1.26.12',
            'filterpy>=1.4.5',
            'dxcam>=0.0.5',
            'matplotlib>=3.3',
            'Pillow>=7.1.2',
            'PyYAML>=5.3.1',
            'scipy>=1.4.1',
            'thop>=0.1.1 ',
            'torch>=1.7.0',
            'torchvision>=0.8.1',
            'tqdm>=4.64.0',
            'tensorboard>=2.4.1',
            'pandas>=1.1.4',
            'seaborn>=0.11.0'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7'
)
