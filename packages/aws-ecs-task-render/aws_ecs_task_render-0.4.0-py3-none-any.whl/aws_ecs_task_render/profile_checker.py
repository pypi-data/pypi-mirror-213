"""Module to make checks about the AWS profile"""
import configparser
import logging
from os import environ as os_environ, path as os_path
from pathlib import Path
from sys import exit as sys_exit
from inquirer import List as inquirer_list, prompt as inquirer_prompt


class ProfileChecker:
    """Class to check or choose the AWS profile"""
    def __init__(self, profile):
        self.profile_name = profile
        self.credential_file = configparser.ConfigParser()
        self.config_file = configparser.ConfigParser()
        self.profiles_list = []
        self.sections_list = []
        self.read_profiles_files()
        self.create_section_list()
        if None is self.profile_name:
            self.choose_profile()
        self.exists()
        self.profile = self.profile_name

    def choose_profile(self):
        """Function to choose the AWS profile to use"""
        self.profiles_list = [inquirer_list('profile_name',
            message='Choose the profile from which launch the command',
            choices=self.sections_list)]
        profiles_selection = dict
        profiles_selection = inquirer_prompt(self.profiles_list)
        if profiles_selection:
            self.profile_name = profiles_selection['profile_name']

    def create_section_list(self):
        """Function to read the valid profile in the files"""
        try:
            credential_sections = self.credential_file.sections()
            for section in credential_sections:
                section_name = section.removeprefix('profile ')
                self.sections_list.append(section_name)
            if self.config_file:
                config_sections = self.config_file.sections()
                for section in config_sections:
                    section_name = section.removeprefix('profile ')
                    self.sections_list.append(section_name)
        except configparser.Error:
            logging.error('Something goes wrong during the create_section_list function')

    def exists(self):
        """Function to check if the provided profile exists"""
        if self.profile_name not in self.sections_list:
            logging.error('%s isn\'t a valid profile', self.profile_name)
            self.choose_profile()

    def read_profiles_files(self):
        """Class that manage all the stuff related to the profiles"""
        try:
          os_environ["HOME"]
          home_path = os_environ["HOME"]
        except:
          logging.warning(f'Ops, seems you do not have HOME variable defined on your machine, i\'ll try to use "{str(Path.home())}"')
          home_path = str(Path.home())
        try:
            self.credential_file.read(f'{home_path}/.aws/credentials')
            if os_path.exists(f'{home_path}/.aws/config'):
                self.config_file.read(f'{home_path}/.aws/config')
        except configparser.Error:
            logging.error('%s/.aws/credentials', home_path)
            sys_exit(1)
