from setuptools import setup, find_packages

setup(
    name="jadoomantar",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.5.1",
        "numpy>=1.19.5"
    ],
    entry_points={
        'console_scripts': [
            'jadoomantar=jadoomantar.main:invisibility_cloak',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for creating an invisible cloak effect using OpenCV.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/jadoomantar",  # Update this with your GitHub repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
