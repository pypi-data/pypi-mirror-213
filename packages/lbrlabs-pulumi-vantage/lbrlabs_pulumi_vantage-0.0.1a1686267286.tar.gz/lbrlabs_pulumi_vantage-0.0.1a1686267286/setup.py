# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import errno
from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call


VERSION = "0.0.1a1686267286"
PLUGIN_VERSION = "0.0.1-alpha.1686267286+209cac5c"

class InstallPluginCommand(install):
    def run(self):
        install.run(self)
        try:
            check_call(['pulumi', 'plugin', 'install', 'resource', 'vantage', PLUGIN_VERSION, '--server', 'github://api.github.com/lbrlabs'])
        except OSError as error:
            if error.errno == errno.ENOENT:
                print(f"""
                There was an error installing the vantage resource provider plugin.
                It looks like `pulumi` is not installed on your system.
                Please visit https://pulumi.com/ to install the Pulumi CLI.
                You may try manually installing the plugin by running
                `pulumi plugin install resource vantage {PLUGIN_VERSION}`
                """)
            else:
                raise


def readme():
    try:
        with open('README.md', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "vantage Pulumi Package - Development Version"


setup(name='lbrlabs_pulumi_vantage',
      python_requires='>=3.7',
      version=VERSION,
      description="A Pulumi package to create resource in vantage.sh.",
      long_description=readme(),
      long_description_content_type='text/markdown',
      cmdclass={
          'install': InstallPluginCommand,
      },
      keywords='pulumi vantage',
      url='https://pulumi.io',
      project_urls={
          'Repository': 'https://github.com/lbrlabs/pulumi-vantage'
      },
      license='Apache-2.0',
      packages=find_packages(),
      package_data={
          'lbrlabs_pulumi_vantage': [
              'py.typed',
              'pulumi-plugin.json',
          ]
      },
      install_requires=[
          'parver>=0.2.1',
          'pulumi>=3.0.0,<4.0.0',
          'semver>=2.8.1'
      ],
      zip_safe=False)
