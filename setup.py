from setuptools import setup

setup(
    name='mastodon_auth_example',
    version='1.0.0',
    url='http://github.com/civic/mastodon-auth-example/',
    license='',
    author='civic',
    author_email='',
    description='get matdon access token example',
    install_requires = [
        "requests>=2.0.0"
    ],
    entry_points="""
    [console_scripts]
    mastodon_get_access_token=mastodon_auth_example:main
    """,
)
