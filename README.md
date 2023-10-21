# dropbox_file_manager
Simple Python package that uses the dropbox API to upload files and pass back a download link.

# How to install
- `pip install -e .`

# How to use

### Get a Dropbox access token
To get a Dropbox API access token, go to the Dropbox [`console app`](https://www.dropbox.com/developers/apps), register a new App, provide it with `files` and `sharing` permissions, and finally generate an access token. The access token is valid permanently (I think).

### Import in your Python script
```python
from dropbox_file_manager import DropboxFileManager
dfm = DropboxFileManager(token="TOKEN")

# upload and get download link
download_link = dfm.upload_file("path/to/local/file", "upload/path/to/file/in/dropbox")

# or get download link of existing file
download_link = dfm.get_download_link("path/to/dropbox/file")
```
Download links are valid permanently (I think).


# Developing on this package

## Releasing a new version
Main contains the latest version.
Always uses semantic versioning: MAJOR.MINOR.BUGFIX https://semver.org/.

## Pre-commit
To make everyone's life easier, we use pre-commit to automatically enforce consistent formatting. It will check your code before you commit it, and if it finds any issues, it will fix them for you. Then you just have to restage the fixed files and commit again.
To install pre-commit for this repo, run the following command from the root of this repo:
```
pip install pre-commit
pre-commit install
```
