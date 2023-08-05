# pyrchive-is

just a simple python package for archiving and finding websites with archive.is

## install

```
pip install pyrchive
```

## use

```python
from pyrchive.pyrchive import ArchiveSesh


archive_session = ArchiveSesh()
url_to_archive = "www.oatbread.org"
archived_url = archive_session.archive_url(url_to_archive)
print(f"Archived URL: {archived_url}")
```

## license
mit or summin
