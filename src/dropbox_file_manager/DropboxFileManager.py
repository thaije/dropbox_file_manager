import sys
from pathlib import Path

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.exceptions import ApiError, AuthError
from dropbox.files import WriteMode


class DropboxFileManager:
    def __init__(
        self,
        token: str,
        refresh_token: str = None,
        app_key: str = None,
        app_secret: str = None,
    ):
        self.token = token
        self.refresh_token = refresh_token
        self.app_key = app_key
        self.app_secret = app_secret

        if refresh_token or app_secret or app_key:
            try:
                assert refresh_token
                assert app_key
                assert app_secret
            except AssertionError:
                raise Exception(
                    "Using a refresh token requires the app_key and app_secret to be set as well."
                )
        self.dbx = dropbox.Dropbox(
            oauth2_access_token=token,
            oauth2_refresh_token=refresh_token,
            app_key=self.app_key,
            app_secret=app_secret,
        )
        self.check_token()

    def check_token(self):
        try:
            self.dbx.users_get_current_account()
        except AuthError:
            sys.exit(
                "ERROR: Invalid access token. You can either: \n1) Re-generate a temporary "
                "access token via the app console at https://www.dropbox.com/developers/apps\n"
                "2) Run DropboxFileManager.generate_token(app_key, app_secret) to generate a "
                "new access token and refresh token that can be used to refresh access indefinetly"
            )

    def get_download_link(self, dbx_file_path):
        dbx_file_path = self.__validate_dbx_file_path(dbx_file_path)

        link = self.dbx.sharing_create_shared_link(dbx_file_path)
        dl_link = link.url.replace("dl=0", "dl=1")
        print(
            f"Generated download link for Dropbox file {dbx_file_path} valid forever (probably):",
            dl_link,
        )
        return dl_link

    def upload_file(self, local_file_path: str, dbx_file_path: str):
        assert len(local_file_path) > 0

        dbx_file_path = self.__validate_dbx_file_path(dbx_file_path)

        with open(local_file_path, "rb") as f:
            print(
                "Uploading "
                + local_file_path
                + " to Dropbox as "
                + dbx_file_path
                + "..."
            )

            self.dbx.files_upload(f.read(), dbx_file_path, mode=WriteMode("overwrite"))
            return self.get_download_link(dbx_file_path)

    def __validate_dbx_file_path(self, dbx_file_path):
        assert len(dbx_file_path) > 0

        # always start with a "/", as to navigate from root
        if dbx_file_path[0] != "/":
            dbx_file_path = "/" + dbx_file_path
        return dbx_file_path


def generate_tokens(app_key, app_secret):
    """
    This example walks through a basic oauth flow for fetching an access token and refresh token.
    It requires a user to click "allow" on the dropbox website, but afterwards the refresh token
    can be used to indefinitly extend access without user input.

    Original author: Karandeep Johar from Dropbox.
    See here: https://github.com/dropbox/dropbox-sdk-python/blob/main/example/oauth/commandline-oauth.py
    """

    auth_flow = DropboxOAuth2FlowNoRedirect(
        app_key, app_secret, token_access_type="offline"
    )

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print('2. Click "Allow" (you might have to log in first).')
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()

    try:
        oauth_result = auth_flow.finish(auth_code)

    except Exception as e:
        print("Error: %s" % (e,))
        exit(1)

    print("Testing access token..")
    with dropbox.Dropbox(oauth2_access_token=oauth_result.access_token) as dbx:
        dbx.users_get_current_account()
        print("Successfully set up client!")

    print("Your access token:", oauth_result.access_token)
    print("Your refresh token:", oauth_result.refresh_token)
    print(
        "Pass these to a DropboxFileManager class instance to use Dropbox via Python :)"
    )

    return {
        "access_token": oauth_result.access_token,
        "refresh_token": oauth_result.refresh_token,
    }
