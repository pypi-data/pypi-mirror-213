from setuptools import setup, find_packages

setup(
    name='vt_ratio',
    version='1.7',
    packages=find_packages(),
    install_requires=['vt'],
    author='Adrian Tarver',
    description='A Python3 package for calculating VirusTotal scan malicious ratios.',
    keywords='VirusTotal scan malicious ratio',
    url='https://github.com/th3tr1ckst3r/vt_ratio',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    data_files=[
        ('', [
            'LICENSE',
            'README.md'
        ])
    ],
    package_data={
        'vt_ratio': ['vt_client.py', 'utils.py', 'vt_api_key.py'],
    }
)
