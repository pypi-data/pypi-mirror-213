from datoso_seed_sfc_speedhacks.dats import SFCSpeedHacksDat

rules = [
    {
        'name': 'Super Famicom Speed Hacks Dat',
        '_class': SFCSpeedHacksDat,
        'seed': 'sfc_speedhacks',
        'priority': 0,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Speed Hacks'
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