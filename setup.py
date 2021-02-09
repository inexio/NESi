import setuptools
import os


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename)[20:])
    return paths


extra_files = package_files('/opt/NESi/templates')

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
    entry_points={
        'console_scripts': [
            'nesi-cli = nesi_cli:main',
            'nesi-api = nesi_api:main',
        ]
    },
    package_data={'bootup': ['conf/*.conf', 'conf/bootstraps/*.sh', 'conf/ssh/*.pub', 'conf/ssh/id_rsa'],
                  'test_cases': ['integration_tests/alcatel/*.txt', 'integration_tests/edgecore/*.txt',
                                 'integration_tests/huawei/*.txt', 'integration_tests/keymile/*.txt',
                                 'integration_tests/zhone/*.txt', 'integration_tests/pbn/*.txt'],
                  'templates': extra_files,
                  '': ['requirements.txt']},
    packages=[
        '',
        'bootup',
        'nesi',
        'test_cases',
        'templates',
        'vendors',
        'bootup.sockets',
        'nesi.alcatel',
        'nesi.edgecore',
        'nesi.huawei',
        'nesi.keymile',
        'nesi.pbn',
        'nesi.softbox',
        'nesi.zhone',
        'nesi.alcatel.alcatel_resources',
        'nesi.alcatel.api',
        'nesi.alcatel.api.schemas',
        'nesi.edgecore.api',
        'nesi.edgecore.edgecore_resources',
        'nesi.edgecore.api.schemas',
        'nesi.huawei.api',
        'nesi.huawei.huawei_resources',
        'nesi.huawei.api.schemas',
        'nesi.keymile.api',
        'nesi.keymile.keymile_resources',
        'nesi.keymile.api.schemas',
        'nesi.pbn.pbn_resources',
        'nesi.softbox.api',
        'nesi.softbox.base_resources',
        'nesi.softbox.cli',
        'nesi.softbox.api.models',
        'nesi.softbox.api.schemas',
        'nesi.softbox.api.views',
        'nesi.zhone.api',
        'nesi.zhone.zhone_resources',
        'nesi.zhone.api.schemas',
        'test_cases.unit_tests',
        'test_cases.unit_tests.alcatel',
        'test_cases.unit_tests.edgecore',
        'test_cases.unit_tests.huawei',
        'test_cases.unit_tests.keymile',
        'test_cases.unit_tests.pbn',
        'test_cases.unit_tests.zhone',
        'vendors.Alcatel',
        'vendors.EdgeCore',
        'vendors.Huawei',
        'vendors.KeyMile',
        'vendors.Zhone'
    ]
)
