from setuptools import setup, find_packages
setup(
        name='sftpoeb',
        version='0.0.1',
        url='',
        license='MIT',
        author='Natthawut Thawisombat',
        author_email='natthawut.th@inet.co.th',
        description='To Easy create sftp for e-tax invoice & e-receive of Oneeletronicbilling',
        packages=find_packages(),
        long_description=open('README.txt').read() +  '\n\n' + open('CHANGELOG.txt').read(),
        keywords='sftp',
        install_requires=['paramiko','Requests','requests_toolbelt','urllib3']
    )