from setuptools import find_packages, setup

package_name = 'image_flipper_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Herschenglime',
    maintainer_email='herschenglime@gmail.com',
    description='simple package to flip camera topic',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'image_flipper = image_flipper_pkg.image_flipper:main'
        ],
    },
)
