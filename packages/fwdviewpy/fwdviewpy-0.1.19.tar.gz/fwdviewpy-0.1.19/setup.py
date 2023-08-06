from setuptools import setup, find_packages

setup(
    name='fwdviewpy',
    version='0.1.19',
    description='Python package developed by FWD View - The Data Transformation Specialists.',
    long_description='Python package developed by FWD View to automate actions on both the Delphix Virtualization engine and Delphix Continuous Compliance engine.',
    packages=find_packages(),
    author='Cameron Bose & Ryan Springett',
    author_email="cameron.bose@fwdview.com",

    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
    ]
)





