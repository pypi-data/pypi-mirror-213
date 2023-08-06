from datoso_seed_md_enhanced.dats import MdEnhancedDat

rules = [
    {
        'name': '32X MD+ Dat',
        '_class': MdEnhancedDat,
        'seed': 'md_enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': '32X'
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'MD+'
            }
        ]
    },
    {
        'name': '32X MSU-MD Dat',
        '_class': MdEnhancedDat,
        'seed': 'md_enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': '32X'
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'MSU-MD'
            }
        ]
    },
    {
        'name': 'Sega CD Hacks Dat',
        '_class': MdEnhancedDat,
        'seed': 'md_enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Mega CD Hacks'
            }
        ]
    },
    {
        'name': 'Mega Drive Enhanced Colors Dat',
        '_class': MdEnhancedDat,
        'seed': 'md_enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Mega Drive'
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Enhanced Colors'
            }
        ]
    },
    {
        'name': 'Mega Drive MD+ Dat',
        '_class': MdEnhancedDat,
        'seed': 'md_enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Mega Drive'
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'MD+'
            }
        ]
    },
    {
        'name': 'Mega Drive Mode 1 CD Dat',
        '_class': MdEnhancedDat,
        'seed': 'md_enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Mega Drive'
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Mode 1 CD'
            }
        ]
    },
    {
        'name': 'Mega Drive MSU-MD Dat',
        '_class': MdEnhancedDat,
        'seed': 'md_enhanced',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Mega Drive'
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'MSU-MD'
            }
        ]
    }
]


def get_rules():
    return rules