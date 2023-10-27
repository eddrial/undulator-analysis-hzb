'''
Created on Oct 26, 2023

@author: oqb
'''

from undulator_analysis_hzb import device as dev

if __name__ == '__main__':
    a = dev.Campaign(campaign_name = 'my_campaign')
    
    print (a.name)
    