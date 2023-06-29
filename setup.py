from setuptools import setup, find_packages

setup(
    name="star_rail_gps",
    version="0.0.1",
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    packages=find_packages(),
    author="furacas",
    author_email="s.furacas@outlook.com",
    description="Honkai: Star Rail GPS",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/furacas/StarRailGPS",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.7',
    package_data={
        'star_rail_gps': ['resources/*'],
    },
)
