from distutils.core import setup

setup(
    name='zone_api',
    packages=['zone_api', 'zone_api.core', 'zone_api.core.actions', 'zone_api.core.devices'],
    version='0.2',
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Group Home Automation devices / sensors into zones and associate them with actions',
    author='YF',
    author_email='thorathovao@gmail.com',
    url='https://github.com/user/yfaway',
    download_url='https://github.com/yfaway/zone-apis/archive/refs/tags/v_01.tar.gz',
    keywords=['zone-api', 'home-automation', 'openhab'],
    install_requires=[
        'habapp',
        'requests',
        'schedule',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
