from setuptools import setup, find_packages


setup(
    name='apiTestMaid',
    version='1.0.1.dev1',
    description='A http client Testing python project',
    url='https://gitlab.wuage-inc.com/jianxing.wei/pc-url-monitor.git',
    author='Jianxing.wei',
    author_email='weijx.cpp@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    #package_data={
    # If any package contains *.txt or *.rst files, include them:
    #},
    packages=['core','ext','util'],
    keywords='apitool testMaid apiTestMaid',
    #packages=find_packages(),
    platforms = 'any',
     entry_points = {
        'console_scripts' : [
            'testmaid= core.main:main2'
        ]
    }

)
