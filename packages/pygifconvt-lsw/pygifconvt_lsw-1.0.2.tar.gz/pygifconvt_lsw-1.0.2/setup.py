from setuptools import setup, find_packages

setup(
    name             = 'pygifconvt_lsw',
    version          = '1.0.2',
    description      = 'lsw\'s Test Package',
    author           = 'peterlah',
    author_email     = 'peterlah@naver.com',
    url              = '',
    download_url     = '',
    install_requires = ['pillow'],
	include_package_data=True,
	packages=find_packages(),
    keywords         = ['GIFCONVERTER', 'gifconverter'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
) 