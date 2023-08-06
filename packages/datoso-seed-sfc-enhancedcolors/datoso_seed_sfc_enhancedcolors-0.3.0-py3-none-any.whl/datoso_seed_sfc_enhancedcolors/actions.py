from datoso_seed_sfc_enhancedcolors.dats import SFCEnhancedColorsDat

actions = {
    '{dat_origin}': [
        {
            'action': 'LoadDatFile',
            '_class': SFCEnhancedColorsDat
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