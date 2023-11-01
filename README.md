# dropbox_file_manager
Simple Python package that uses the dropbox API to upload files and pass back a download link.

# How to install
- `pip install -e .`

# How to use

### Get a Dropbox access token
To get a Dropbox API access token first go to the Dropbox [`console app`](https://www.dropbox.com/developers/apps), register a new App, provide it with `files` and `sharing` permissions.
Next, you got to get a Dropbox access token. You can either:
1. Generate a temporary (less than a day) access token via the app console at https://www.dropbox.com/developers/apps\n"
2. Run `DropboxFileManager.generate_token(your_app_key, your_app_secret)` to generate a new access token and refresh token that can be used to automatically refresh access indefinetly once fetched.


### Import in your Python script

```python
from dropbox_file_manager import DropboxFileManager
dfm = DropboxFileManager(token="TOKEN", refresh_token="REFRESH_TOKEN", app_key="YOUR_DROPBOX_APP_KEY", app_secret="YOUR_DROPBOX_APP_SECRET")
# Or alternatively use with a temporary access token without refresh token.
# dfm = DropboxFileManager(token="TOKEN")


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
