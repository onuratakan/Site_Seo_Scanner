from setuptools import setup

setup(name='Site_Seo_Scanner',
version='0.1.1',
description="""The site seo scanner.
""",
long_description="""
# Site Seo Scanner | ![Made_with_python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg) ![Licence](https://img.shields.io/github/license/onuratakan/Site_Seo_Scanner)
# Installing
```console
pip install Site-Seo-Scanner
```
# Import
```python
from ssc import SSC
```
""",
long_description_content_type='text/markdown',
url='https://github.com/onuratakan/Site_Seo_Scanner',
author='Onur Atakan ULUSOY',
author_email='atadogan06@gmail.com',
license='MIT',
packages=["ssc"],
package_dir={'':'src'},
install_requires=[
    "beautifulsoup4==4.9.3",
    "bs4==0.0.1",
    "soupsieve==2.2.1",
    "lxml==4.6.3",
    "fpdf==1.7.2",
],
python_requires='>=3',
zip_safe=False)