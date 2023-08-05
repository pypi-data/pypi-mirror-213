from distutils.core import setup


setup(
    name='fastapi_module_register',
    version='0.0.1',
    author='stan',
    author_email='gd19920125@hotmail.com',
    description='通过将fastapi的模型自动注册路由',
    url='https://github.com/dcshoecousa',
    packages=["src"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)