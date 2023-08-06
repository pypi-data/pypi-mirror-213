from setuptools import setup, find_packages
setup(
        name='sftpoeb',
        version='0.0.9',
        url='',
        license='MIT',
        author='Natthawut Thawisombat',
        author_email='natthawut.th@inet.co.th',
        description='To Easy create sftp for e-tax invoice & e-receive of Oneeletronicbilling',
        packages=find_packages(),
        long_description=open('README.txt').read() +  '\n\n' + open('CHANGELOG.txt').read(),
        keywords='sftp',
        install_requires=['paramiko==2.11.0','Requests==2.31.0','requests_toolbelt==0.9.1','urllib3==1.26.5']
    )