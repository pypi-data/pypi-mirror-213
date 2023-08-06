from setuptools import setup, find_packages

setup(
    name='mahirodos2',
    version='1.0.4',
    description='Simple but yet powerful DoS (Denial-of-Service) PIP package',
    long_description='''mahirodos2 is a Python package that provides a simple yet powerful capability to perform DoS (Denial-of-Service) attacks. Please note that launching DoS attacks is illegal and unethical unless you have explicit permission from the target site's owner and are using it for legitimate purposes such as security testing. It's important to use such tools responsibly and within the boundaries of the law.

---

### How to use

1. Import the `spamreq` function from the `mahirodos2` package:

    ```python
    from mahirodos2 import spamreq
    ```

2. Call the `spamreq` function with the target site URL as the argument:

    ```python
    spamreq("<TARGET SITE HERE>")
    ```

3. Replace `<TARGET SITE HERE>` with the URL of the site you want to perform the DoS attack on. Make sure you have proper authorization and follow legal and ethical guidelines.

---

For more information, please refer to the package documentation and guidelines on responsible use.

''',
    author='Mahiro Chan',
    author_email='mahirochan493@gmail.com',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
