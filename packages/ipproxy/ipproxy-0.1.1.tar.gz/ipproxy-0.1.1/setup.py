from setuptools import setup


setup(
    name='ipproxy',
    version='0.1.1',
    py_modules=['ipproxy'],
    install_requires=[],
    author='sega',
    author_email='yourname@example.com',
    description='ipproxy is a tool for obtaining and managing proxy IPs in Python. It can help crawler programs hide '
                'their real IP addresses when accessing target websites, thereby avoiding being blocked or restricted.',
    url='https://example.com/ipproxy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
