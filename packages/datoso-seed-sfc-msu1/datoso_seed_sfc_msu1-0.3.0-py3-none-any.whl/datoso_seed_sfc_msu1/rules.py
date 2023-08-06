from datoso_seed_sfc_msu1.dats import SFCMSU1Dat

rules = [
    {
        'name': 'Super Famicom - MSU1 Dat',
        '_class': SFCMSU1Dat,
        'seed': 'sfc_msu1',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'MSU1'
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