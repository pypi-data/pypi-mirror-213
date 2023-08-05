#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.dialog_box import DialogBox


class Choose(Configs):
    """ Choose packages with dialog utility and -S, --search flag. """

    def __init__(self, repository: str):
        super(Configs, self).__init__()
        self.repository: str = repository

        self.utils = Utilities()
        self.dialogbox = DialogBox()

        self.choices: list = []
        self.height: int = 10
        self.width: int = 70
        self.list_height: int = 0

        self.is_binary: bool = self.utils.is_binary_repo(repository)

    def packages(self, data: dict, packages: list, method: str) -> list:
        if self.dialog:
            title: str = f' Choose packages you want to {method} '

            if method in ('remove', 'find'):
                self.choose_from_installed(packages)
            elif method == 'upgrade':
                self.choose_for_upgraded(data, packages)
            else:
                self.choose_for_others(data, packages)

            if not self.choices:
                return packages

            text: str = f'There are {len(self.choices)} packages:'
            code, packages = self.dialogbox.checklist(text, title, self.height, self.width,
                                                      self.list_height, self.choices)
            if code == 'cancel' or not packages:
                os.system('clear')
                raise SystemExit()

            os.system('clear')

        return packages

    def choose_from_installed(self, packages: list):
        """ Choose installed packages for remove or find. """
        installed_packages: list = list(self.utils.installed_packages.values())

        for package in installed_packages:
            package_name: str = self.utils.split_package(package)['name']
            package_version: str = self.utils.split_package(package)['version']

            for pkg in packages:
                if pkg in package or pkg == '*':
                    self.choices.extend([(package_name, package_version, False, f'Package: {package}')])

    def choose_for_upgraded(self, data: dict, packages: list):
        """ Choose packages that they will going to upgrade. """
        for pkg in packages:
            for package in data.keys():

                if pkg == package:
                    inst_package: str = self.utils.is_package_installed(package)
                    inst_package_version: str = self.utils.split_package(inst_package)['version']
                    inst_package_build: str = self.utils.split_package(inst_package)['build']
                    repo_ver: str = data[package]['version']

                    if self.is_binary:
                        binary_package: str = data[package]['package']
                        repo_build_tag: str = self.utils.split_package(binary_package[:-4])['build']
                    else:
                        repo_location: str = data[package]['location']
                        repo_build_tag: str = self.utils.read_slackbuild_build_tag(
                            package, repo_location, self.repository)
                    self.choices.extend(
                        [(package, f'{inst_package_version} -> {repo_ver}', True,
                          f'Installed: {package}-{inst_package_version} Build: {inst_package_build} -> '
                          f'Available: {repo_ver} Build: {repo_build_tag}')])

    def choose_for_others(self, data: dict, packages: list):
        """ Choose packages for others methods like install, tracking etc. """
        for pkg in packages:
            for package in data.keys():

                if pkg in package or pkg == '*':
                    version: str = data[package]['version']
                    self.choices.extend([(package, version, False, f'Package: {package}-{version} '
                                                                   f'> {self.repository}')])
