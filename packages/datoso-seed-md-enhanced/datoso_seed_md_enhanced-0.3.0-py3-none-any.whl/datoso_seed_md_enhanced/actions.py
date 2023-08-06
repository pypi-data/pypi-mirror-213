from datoso_seed_md_enhanced.dats import MdEnhancedDat

actions = {
    '{dat_origin}': [
        {
            'action': 'LoadDatFile',
            '_class': MdEnhancedDat
        },
        {
            'action': 'DeleteOld'
        },
        {
            'action': 'Copy',
            'folder': '{dat_destination}'
        },
        {
            'action': 'SaveToDatabase'
        }
    ]
}

def get_actions():
    return actions
