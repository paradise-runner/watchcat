import os
import time

from logger import get_logger


LOGGER = get_logger()


class WatchCat:

    def __init__(self, watch_dir_path, func_on_detection):
        self.watch_dir_path = watch_dir_path
        self.func = func_on_detection
        self.new_folders = []
        self.old_folder_snapshot = None
        self.new_folder_snapshot = None

    def _folder_ready_for_interaction(self, folder_name):
        folder_path = os.path.join(self.watch_dir_path, folder_name)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.rename(file_path, file_path)
                except OSError:
                    LOGGER.debug(
                        f"Folder: {folder_name} has files that are unable to be renamed. Folder "
                        f"is not ready for interaction."
                    )
                    return False
        LOGGER.debug(f"All files in {folder_name} are eligible for interaction.")
        return True

    def _acquire_new_folders(self):
        if self.old_folder_snapshot is None:
            self.old_folder_snapshot = {folder for folder in os.listdir(self.watch_dir_path)}
            time.sleep(2)

        self.new_folder_snapshot = {
            folder for folder in os.listdir(self.watch_dir_path)
        }

        self.new_folders = self.new_folder_snapshot.difference(self.old_folder_snapshot)

        self.old_folder_snapshot = self.new_folder_snapshot.copy()
        self.new_folder_snapshot = None


    def _push_folders_off_ledge(self):
        ready_folders = []
        for folder_name in self.new_folders:
            # If the OS allows a every file in that folder to be renamed to itself, the folder is
            # ready to be pushed off the ledge and processed
            if self._folder_ready_for_interaction(folder_name):
                ready_folders.append(folder_name)

        if ready_folders:
            LOGGER.debug(f"{len(ready_folders)} are eligible for interaction.")
            LOGGER.debug(f"Running {self.func} on folders: {*ready_folders,}")

            for folder_name in ready_folders:
                folder_path = os.path.join(self.watch_dir_path, folder_name)
                LOGGER.debug(f"Running {self.func} on {folder_name}")
                self.func(folder_path)
        else:
            LOGGER.debug(
                f"There were no folders eligible for action. Keeping folders on the ledge."
            )

    def poll_folder(self):
        while True:
            time.sleep(2)
            self._acquire_new_folders()
            self._push_folders_off_ledge()
