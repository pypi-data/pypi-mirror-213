from datoso_seed_sfc_enhancedcolors.dats import SFCEnhancedColorsDat

rules = [
    {
        'name': 'SFCEnhancedColors Dat',
        '_class': SFCEnhancedColorsDat,
        'seed': 'sfc_ec',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Enhanced Colors'
            },
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Super Famicom'
            }
        ]
    }
]


def get_rules():
    return rules