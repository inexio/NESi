import setuptools
import os
import re
#import pydevd_pycharm
#pydevd_pycharm.settrace('localhost', port=3001, stdoutToServer=True, stderrToServer=True)

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(re.match('.+(templates/.+$)', os.path.join(path, filename)).groups()[0])
    return paths

extra_files = package_files(os.path.dirname(os.path.abspath(__file__)) + '/nesi/templates')

with open('requirements.txt') as fl:
    requires = fl.read()

setuptools.setup(
    name='NESi',
    version='1.3.0',
    url='https://github.com/inexio/NESi',
    description='Network Equiptment Simulator (NESi)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='NESi, Network, Simulator, Device, Alcatel, Huawei, KeyMile',
    install_requires=requires,
    license='BSD-2-Clause License',
    entry_points={
        'console_scripts': [
            'nesi-cli = cli:main',
            'nesi-api = api:main',
        ]
    },
    package_data={
        'nesi':
            extra_files + ['bootup/conf/ssh/*.pub', 'bootup/conf/ssh/id_rsa',
            'test_cases/integration_tests/alcatel/*.txt', 'test_cases/integration_tests/edgecore/*.txt',
            'test_cases/integration_tests/huawei/*.txt', 'test_cases/integration_tests/keymile/*.txt',
            'test_cases/integration_tests/zhone/*.txt', 'test_cases/integration_tests/pbn/*.txt'],
        '': ['requirements.txt']
    },
    packages=[
        '',
        'nesi',
        'nesi.templates',
        'nesi.bootup',
        'nesi.bootup.sockets',
        'nesi.bootup.conf',
        'nesi.bootup.conf.bootstraps',
        'nesi.devices.alcatel',
        'nesi.devices.edgecore',
        'nesi.devices.huawei',
        'nesi.devices.keymile',
        'nesi.devices.pbn',
        'nesi.devices.softbox',
        'nesi.devices.zhone',
        'nesi.devices.alcatel.alcatel_resources',
        'nesi.devices.alcatel.api',
        'nesi.devices.alcatel.api.schemas',
        'nesi.devices.edgecore.api',
        'nesi.devices.edgecore.edgecore_resources',
        'nesi.devices.edgecore.api.schemas',
        'nesi.devices.huawei.api',
        'nesi.devices.huawei.huawei_resources',
        'nesi.devices.huawei.api.schemas',
        'nesi.devices.keymile.api',
        'nesi.devices.keymile.keymile_resources',
        'nesi.devices.keymile.api.schemas',
        'nesi.devices.pbn.pbn_resources',
        'nesi.devices.softbox.api',
        'nesi.devices.softbox.base_resources',
        'nesi.devices.softbox.cli',
        'nesi.devices.softbox.api.models',
        'nesi.devices.softbox.api.schemas',
        'nesi.devices.softbox.api.views',
        'nesi.devices.zhone.api',
        'nesi.devices.zhone.zhone_resources',
        'nesi.devices.zhone.api.schemas',
        'nesi.test_cases',
        'nesi.test_cases.unit_tests',
        'nesi.test_cases.unit_tests.alcatel',
        'nesi.test_cases.unit_tests.edgecore',
        'nesi.test_cases.unit_tests.huawei',
        'nesi.test_cases.unit_tests.keymile',
        'nesi.test_cases.unit_tests.pbn',
        'nesi.test_cases.unit_tests.zhone',
        'nesi.vendors',
        'nesi.vendors.Alcatel',
        'nesi.vendors.EdgeCore',
        'nesi.vendors.Huawei',
        'nesi.vendors.KeyMile',
        'nesi.vendors.Zhone'
    ]
)
