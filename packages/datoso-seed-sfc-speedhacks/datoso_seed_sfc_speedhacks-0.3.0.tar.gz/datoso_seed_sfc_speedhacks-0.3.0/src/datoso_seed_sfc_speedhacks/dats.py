"""
    TranslatedEnglish Dat class to parse different types of dat files.
"""
import re
from datoso.configuration import config
from datoso.repositories.dat import XMLDatFile

class SFCSpeedHacksDat(XMLDatFile):
    """ Translated English Dat class. """
    seed: str = 'sfc_speedhacks'

    def initial_parse(self):
        # pylint: disable=R0801
        """ Parse the dat file. """
        name = self.name

        name_array = name.split(' - ')

        company, system, suffix = name_array
        self.company = company
        self.system = system
        self.suffix = suffix
        self.overrides()

        if self.modifier or self.system_type:
            self.preffix = config.get('PREFFIXES', self.modifier or self.system_type, fallback='')
        else:
            self.preffix = None

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


    def get_date(self):
        """ Get the date from the dat file. """
        if self.file:
            result = re.findall(r'\(.*?\)', self.file)
            self.date = result[len(result)-1][1:-1]
        return self.date
