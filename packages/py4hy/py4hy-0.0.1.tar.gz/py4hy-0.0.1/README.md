# Python interface to Helsingin yliopisto

Collection of tools to collect information from various University of Helsinki data sources via their public (unofficial) APIs.

## People search

This pulls data from the [People Finder](https://www.helsinki.fi/en/people/people-finder).

```
from pyhy import people
matti = people.search('Matti Nelimarkka')
print( "Call Matti", matti['mobileNumber'] )
print( "Matti works at", matti['researchOrganization'][-1]['name'])

csds_org_id = matti['researchOrganization'][-1]['id']
csds = people.by_organisation( csds_org_id  )

for member in csds:
  print('Also working at CSCS:', member['firstnames'] + ' ' + member['lastname'])
```
