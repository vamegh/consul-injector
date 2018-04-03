#!/usr/bin/python

### (c) Vamegh Hedayati LGPL License please read the License file for more info.
from setuptools import setup

setup(
    name='consul-injector',
    version='0.0.1',
    description='consul-injector a tool to inject KV values into consul via its api, to help with automation',
    author='Vamegh Hedayati',
    author_email='gh_vhedayati@ev9.io',
    url='https://github.com/vamegh',
    include_package_data=True,
    packages=['vstdlib'],
    install_requires=[
        "futures",
        "futurist",
        "httplib2",
        "PyYAML",
        "requests",
        "requests-futures",
        "sh",
        "urllib3",
    ],
    scripts=[
        'bin/consul-injector',
    ],
    package_data={'vstdlib': ['Copying', 'LICENSE', 'README.md'], },
    data_files=[('/etc/consul-injector', ['configs/color_map.yaml',
                                          'configs/config.yaml',
                                          'configs/consul_config.yaml',
                                          'configs/git_config.yaml',
                                          'Copying',
                                          'LICENSE',
                                          'README.md']),
                ('/etc/consul-injector/data', ['configs/data/inject1.yaml',
                                               'configs/data/inject2.yaml',
                                               'configs/data/inject3.yaml',
                                               'configs/data/inject4.yaml',
                                               'configs/data/inject5.yaml'])]
)
