

import tebis
configuration = {
        'host': '10.15.239.202',
        'configfile': 'd:/tebis/Anlage/Config.txt'
    }
teb = tebis.Tebis(configuration=configuration)
df = teb.getDataAsPD([13, 14, 15, 16],  [[1626779900,1626779930],[1626779950,1626779960]],1)

print(df)


