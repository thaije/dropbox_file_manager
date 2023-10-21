import sys
from pathlib import Path

import dropbox
from dropbox.exceptions import ApiError, AuthError
from dropbox.files import WriteMode


class DropboxFileManager:
    def __init__(self, token: str):
        self.token = token
        self.dbx = dropbox.Dropbox(self.token)
        self.check_token()

    def check_token(self):
        try:
            self.dbx.users_get_current_account()
        except AuthError:
            sys.exit(
                "ERROR: Invalid access token; try re-generating an "
                "access token from the app console on the web."
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
