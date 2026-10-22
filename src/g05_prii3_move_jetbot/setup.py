from setuptools import find_packages, setup

package_name = 'g05_prii3_move_jetbot'

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
    maintainer='pauv17',
    maintainer_email='Pauv17',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'draw_number = g05_prii3_move_jetbot.draw_number:main',
            'collision = g05_prii3_move_jetbot.collision:main',
        ],
    },
)
