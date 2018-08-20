#strain rate prep
import pandas as pd

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/strain/'

def exportRow(row):
    with open(target+'strain_export.txt','a') as output:
        output.write(row)
        print row

with open(target+'global_strain_rate.txt','r') as file:
    for row in file:
        new_row = row.replace('        ',' ')
        new_row = new_row.replace('       ',' ')
        new_row = new_row.replace('      ',' ')
        new_row = new_row.replace('     ',' ')
        new_row = new_row.replace('    ',' ')
        new_row = new_row.replace('   ',' ')
        new_row = new_row.replace('  ',' ')
        new_row = new_row.replace(' ',',')
        exportRow(new_row)