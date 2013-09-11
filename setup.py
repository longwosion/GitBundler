from setuptools import setup, find_packages
import gitbundler

setup(
    name = "GitBundler",
    version=gitbundler.__version__,
    packages = ['gitbundler'],
    author=gitbundler.__author__,
    author_email=gitbundler.__author_email__,
    license=gitbundler.__license__,
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'gitb = gitbundler:main',
        ],
    }
)
