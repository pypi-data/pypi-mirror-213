from setuptools import find_packages, setup

setup(
    name="qos_tools",
    version='0.0.3',
    author="baqis",
    author_email="baqis@baqis.ac.cn",
    url="https://gitee.com/",
    license = "MIT",
    keywords="tools for quantum lab",
    description="control, measure and visualization",
    long_description='long_description',
    long_description_content_type='text/markdown',
    packages = find_packages(),
    include_package_data = True,
    python_requires='>=3.10.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    project_urls={
        'source': 'https://gitee.com',
    },
)


