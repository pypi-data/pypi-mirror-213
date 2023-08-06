from setuptools import setup

setup(
    name='tivan-custom-ser',
    version='0.1',
    packages=[
        "lab3.serializer.src"
    ],
    entry_points={
        'console_scripts': [
            "custom-serialize = lab3.serializer.custom:main"
        ]
    },
    license='MIT',
    author='tivan',
    author_email='tenugo.v@gmail.com',
    description='Python JSON and XML serializer',
)
