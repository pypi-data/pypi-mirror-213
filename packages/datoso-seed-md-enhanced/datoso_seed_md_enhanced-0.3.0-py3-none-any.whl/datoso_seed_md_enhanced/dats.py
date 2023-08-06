import re
from datoso.configuration import config
from datoso.repositories.dat import XMLDatFile

class MdEnhancedDat(XMLDatFile):
    """ MegaDrive Enhanced Colors Dat class. """
    seed: str = 'md_enhanced'

    def initial_parse(self):
        # pylint: disable=R0801
        """ Parse the dat file. """
        name = self.name

        name_array = name.split(' - ')
        if len(name_array) == 2:
            company, system = name_array
        if len(name_array) == 3:
            company, system, suffix = name_array
            self.suffix = suffix
        self.company = company
        self.system = system
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
