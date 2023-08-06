import setuptools
# from setuptools.command.develop import develop
# from setuptools.command.install import install
# from subprocess import check_call
# from pathlib import Path
# import os
#
#
#
# class PostDevelopCommand(develop):
#     """Post-installation for development mode."""
#     def run(self):
#         develop.run(self)
#         # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
#
#
# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     def run(self):
#         install.run(self)
#         home_path = str(Path.home())
#         check_call(("cp -r bp_agent "+home_path+"/bp_agent").split())
#         check_call(("celery multi start worker  -Q:poll_scm_bp_agent poll_scm_bp_agent -c:poll_scm_bp_agent 10 -P:poll_scm_bp_agent gevent -Q:bp_agent bp_agent -c 5 -P prefork -n bpagent").split())
#         # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION


with open('requirements.txt') as f:
    required = f.read().splitlines()


setuptools.setup(
    name="bpctl-test",
    version="1.3.2",
    author="BP Team",
    author_email="shikhar.maheshwari@opstree.com",
    description="It is private package of bpctl",
    url="https://bitbucket.org/okts/bpctl/src/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    scripts=['bin/bpctl'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    # cmdclass={
    #     'develop': PostDevelopCommand,
    #     'install': PostInstallCommand,
    # },
    python_requires='>=3.6',
    install_requires=required
)
