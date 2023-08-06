import os
import shutil


class folders_handler:
    def __init__(self, path_ref):
        self.path_ref = path_ref

    def clear_folder(self, folder_path_to_clear, quiet=False):
        """
        Clear the folder, or file

        :param folder_path_to_clear: The path of the folder to clear
        :type folder_path_to_clear: string
        :param quiet: Disable print of messages along code
        :type quiet: boolean

        :return: void
        """
        path_to_clear = os.path.join(self.path_ref, folder_path_to_clear)
        if not quiet:
            print(f"Clearing: {path_to_clear}")

        if os.path.exists(path_to_clear) and os.path.isdir(path_to_clear):
            shutil.rmtree(path_to_clear, ignore_errors=True)
        elif os.path.exists(path_to_clear) and os.path.isfile(path_to_clear):
            os.remove(path_to_clear)

    def verify_and_create_folder(self, folder_path_to_create, message="", quiet=False):
        """
        Verify and Create a Folder

        :param folder_path_to_create: The path of the folder to create
        :type folder_path_to_create: string
        :param message: Custom message when creating folder
        :type message: string
        :param quiet: Disable print of messages along code. This overhaul the "message" parameter
        :type quiet: boolean

        :return: If the folder not exists create the folder and returns True, if exists returns False
        :type: boolean
        """
        path_to_create = os.path.join(self.path_ref, folder_path_to_create)
        if not quiet:
            print(f"Verifying and creating folder: {path_to_create}")
        if not os.path.exists(path_to_create):
            if not quiet:
                print(message)
            os.makedirs(path_to_create)
            return True
        return False
