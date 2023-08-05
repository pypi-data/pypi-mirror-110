# WebCase Geographical database

## Installation

```sh
pip install wc-django-geo-db
```

In `settings.py`:

```python
INSTALLED_APPS += [
  'pxd_lingua',

  'pxd_postgres',
  'pxd_postgres.ltree',

  'wcd_geo_db',
  'wcd_geo_db.contrib.admin',
  'wcd_geo_db_sources',
]

WCD_GEO_DBSOURCES = {
  'SOURCE_IMPORT_RUNNERS': (
    'wcd_geo_db_sources.sources.katottg.process.KATOTTGImportRunner',
    'wcd_geo_db_sources.sources.katottg_to_koatuu.process.KATOTTG_TO_KOATUUImportRunner',
  )
}
```

## Usage


```python
from wcd_geo_db.client import GeoClient
from wcd_geo_db.conf import Settings
from wcd_geo_db.modules.code_seeker import registry
from wcd_geo_db_sources.sources.koatuu import KOATUU_SEEKER
from wcd_geo_db_sources.sources.katottg import KATOTTG_SEEKER
from wcd_geo_db_sources.sources.novaposhta import NOVAPOSHTA_SEEKER


client = GeoClient(settings=Settings(), code_seeker_registry=registry)

registry.register(KOATUU_SEEKER)
registry.register(KATOTTG_SEEKER)
registry.register(NOVAPOSHTA_SEEKER)

client.bank.divisions.get(ids=(1,))

found = client.bank.divisions.find(levels=(DivisionLevel.ADMINISTRATIVE_LEVEL_1,))

descendants = client.bank.divisions.find_descendants(ids=found)
```
