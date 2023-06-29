from setuptools import setup, find_packages

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.readlines()
requirements = [r.strip() for r in requirements if not r.startswith('#')]

# Remove version numbers
requirements = [r.split('==')[0] for r in requirements]

setup(
    name="StarRailGPS",
    version="0.0.1",
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    packages=find_packages(),
    install_requires=requirements,
    author="furacas",
    author_email="s.furacas@outlook.com",
    description="Honkai: Star Rail GPS",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/furacas/StarRailGPS",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.7',
    package_data={
        'StarRailGPS': ['resources/*'],
    },
)
