import shutil
from pathlib import Path
from typing import List, Optional

from qwak_sdk.exceptions import QwakSuggestionException
from qwak_sdk.tools.files import copytree

from ...common import get_git_commit_id
from ..strategy import Strategy, get_ignore_pattern


class FolderStrategy(Strategy):
    def fetch(
        self,
        src: str,
        dest: str,
        custom_dependencies_path: Optional[str],
        main_dir: str,
        dependency_path: str,
        dependency_required_folders: List[str],
        **kwargs,
    ) -> Optional[str]:
        try:
            self.notifier.debug(f"Fetching Model code from local directory -  {src}")

            ignore_patterns, patterns_for_printing = get_ignore_pattern(
                src, main_dir, self.notifier
            )
            self.notifier.debug(
                f"Will ignore the following files: {patterns_for_printing}."
            )

            copytree(
                src=Path(src) / main_dir,
                dst=Path(dest) / main_dir,
                ignore=ignore_patterns,
            )
            for folder in dependency_required_folders:
                if (Path(src) / folder).exists():
                    copytree(
                        src=Path(src) / folder,
                        dst=Path(dest) / folder,
                        ignore=ignore_patterns,
                    )
                else:
                    self.notifier.warning(
                        'Folder "{}" does not exist. Skipping it.'.format(folder)
                    )
            if (Path(src) / "tests").exists():
                copytree(
                    src=Path(src) / "tests",
                    dst=Path(dest) / "tests",
                    ignore=ignore_patterns,
                )
            if dependency_path:
                shutil.copy(
                    src=Path(src) / dependency_path, dst=Path(dest) / dependency_path
                )

            # Copy custom dependencies path
            if custom_dependencies_path and Path(custom_dependencies_path).is_file():
                shutil.copy(
                    src=custom_dependencies_path,
                    dst=Path(dest) / Path(custom_dependencies_path).name,
                )
            # Get git commit id if exists
            return get_git_commit_id(src, self.notifier)
        except Exception as e:
            raise QwakSuggestionException(
                message="Unable to copy model.",
                src_exception=e,
                suggestion=f"Please make sure that {src} has read permissions.",
            )
