#!/usr/bin/env python
'''
Script to download publicly available TEC maps from
https://cddis.nasa.gov/archive/gps/products/ionex/yyyy/day/*i.Z
usage:
python url_download.py -d yyyy-mm-dd [-t type]
-d gives date of observation
-t gives type of ionex file (codg,upcg,igsg) codg maps are default option

v0.1 modified from ftpdownload.py, Charlotte Sobey 2021
'''

import datetime
import optparse as op
import requests

p=op.OptionParser()
p.add_option('--date','-d',default='NONE',type='string',help='Date (yyyy-mm-dd)')
p.add_option('--type','-t',default='codg',type='string',help='Type of ionex file (codg,upcg,igsg) [codg default]')
ops,args=p.parse_args()

# Reading the date provided
year = int(ops.date.split('-')[0])
month = int(ops.date.split('-')[1])
day = int(ops.date.split('-')[2])

dayofyear = datetime.datetime.strptime(''+str(year)+' '+str(month)+' '+str(day)+'', '%Y %m %d').timetuple().tm_yday

if dayofyear < 10:
        dayofyear = '00'+str(dayofyear)
elif dayofyear < 100 and dayofyear >= 10:
        dayofyear = '0'+str(dayofyear)

# Outputing the name of the IONEX file you require
filename = str(ops.type)+str(dayofyear)+'0.'+str(list(str(year))[2])+str(list(str(year))[3])+'i.Z'
# Due to the name change: https://igs.org/products/#ionosphere        
if ops.type == 'igsg':
        if year > 2022:
                file = f'IGS0OPSFIN_{year}{dayofyear}0000_01D_02H_GIM.INX.gz'
        else:
                file = filename
elif ops.type == 'codg':
        if year == 2022 and int(dayofyear) > 330 or year > 2022:
                file = f'COD0OPSFIN_{year}{dayofyear}0000_01D_01H_GIM.INX.gz'
        else:
               file = filename
elif ops.type == 'esag':
        if year == 2022 and int(dayofyear) > 330 or year > 2022:
                file = f'ESA0OPSFIN_{year}{dayofyear}0000_01D_02H_ION.IOX.gz'
        else:
               file = filename
elif ops.type == 'jplg':
        if year == 2023 and int(dayofyear) > 218 or year > 2022:
                file = f'JPL0OPSFIN_{year}{dayofyear}0000_01D_02H_GIM.INX.gz'
        else:
                file = filename
else:
       file = filename

# URL
url = 'https://cddis.nasa.gov/archive/gps/products/ionex/'+str(year)+'/'+str(dayofyear)+'/'+str(file)

# Makes request of URL, stores response in variable r
print(f'Requesting url {url}')
r = requests.get(url)

# Opens a local file of same name as remote file for writing to
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size=1000):
        fd.write(chunk)

# Closes local file
fd.close()