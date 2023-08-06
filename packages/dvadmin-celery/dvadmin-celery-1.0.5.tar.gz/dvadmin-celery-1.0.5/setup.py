import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="dvadmin-celery",
    version="1.0.5",
    author="DVAdmin",
    author_email="liqiang@django-vue-admin.com",
    description="适用于 django-vue-admin 的celery异步插件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/huge-dream/dvadmin-celery",
    packages=setuptools.find_packages(),
    python_requires='>=3.7, <4',
    install_requires=["django-celery-beat>=2.5.0",
                      "tenant-schemas-celery>=2.2.0",
                      "django-redis>=5.2.0",
                      "django-celery-results>=2.5.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    data_files=[
        ('', ['./dvadmin_celery/fixtures/init_menu.json']),
    ]
)
