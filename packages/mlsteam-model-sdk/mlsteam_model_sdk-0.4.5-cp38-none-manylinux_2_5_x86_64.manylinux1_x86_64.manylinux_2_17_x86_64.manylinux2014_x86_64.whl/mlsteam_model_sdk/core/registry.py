"""Local model registry"""
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from mlsteam_model_sdk.core.exceptions import ModelVersionNotFoundException
from mlsteam_model_sdk.utils.log import logger


class Registry:
    """Local model registry operator"""

    LOCAL_PUUID = '__local__'
    LOCAL_MUUID = '__local__'

    def __init__(self, config_dir: Path) -> None:
        """Initializes a local model registry operator.

        Args:
          config_dir: SDK configuration base directory
        """
        self._models_dir = config_dir / 'models'
        self._download_base_dir = self._models_dir / 'download'
        self._extract_base_dir = self._models_dir / 'extract'
        self._registry_file = self._models_dir / 'reg.json'

    def get_new_local_vuuid(self) -> str:
        """Generates a new local vuuid.

        NOTE: This method is not thread-safe.
        """
        while True:
            local_vuuid = 'local-' + str(uuid.uuid4())[:8]
            if self.get_model_version_info(vuuid=local_vuuid) is None:
                return local_vuuid

    def get_download_base_dir(self, create: bool = False) -> Path:
        """Gets base path to download model version files or packages."""
        if create:
            self._download_base_dir.mkdir(parents=True, exist_ok=True)
        return self._download_base_dir

    def get_download_file(self, vuuid: str, packaged: bool, encrypted: bool,
                          create_dir: bool = False) -> Path:
        """Gets path to save a downloaded model version file or package."""
        download_dir = self.get_download_base_dir(create=create_dir)
        if encrypted:
            download_name = f'{vuuid}-enc.mlarchive'
        elif packaged:
            download_name = f'{vuuid}.mlarchive'
        else:
            download_name = f'{vuuid}.zip'
        return download_dir / download_name

    def get_extract_base_dir(self, create: bool = False) -> Path:
        """Gets base path to extract non-encrypted model version packages."""
        if create:
            self._extract_base_dir.mkdir(parents=True, exist_ok=True)
        return self._extract_base_dir

    def get_extract_dir(self, vuuid: str, create_dir: bool = False) -> Path:
        """Gets path to extract a downloaded model version package."""
        extract_dir = self.get_extract_base_dir(create=create_dir) / vuuid
        if create_dir:
            extract_dir.mkdir(parents=True, exist_ok=True)
        return extract_dir

    def list_model_versions(self) -> Dict[str, dict]:
        """Gets information of model versions in local registry.

        Returns:
          model version dict [vuuid => model version info dict]
        """
        try:
            with self._registry_file.open('rt') as reg_file:
                reg_data = json.load(reg_file)
                return reg_data
        except FileNotFoundError as e:
            logger.warning(e)
            return {}

    def _find_model_version(self, reg_data: dict, version_name: str,
                            muuid: Optional[str] = None,
                            model_name: Optional[str] = None) -> str:
        if muuid:
            def model_matcher(row): return row['muuid'] == muuid
        elif model_name:
            def model_matcher(row): return row['model_name'] == model_name
        else:
            raise ValueError('Neither muuid nor model_name are provided')
        for row in reg_data.values():
            if row['version_name'] == version_name and model_matcher(row):
                return row['vuuid']
        raise ModelVersionNotFoundException(muuid=muuid,
                                            model_name=model_name,
                                            version_name=version_name)

    def get_model_version_info(self,
                               vuuid: Optional[str] = None,
                               version_name: Optional[str] = None,
                               muuid: Optional[str] = None,
                               model_name: Optional[str] = None,
                               default_muuid: Optional[str] = None) -> Optional[dict]:
        """Gets information of a model version in local registry.

        A model version is specified in one of the following ways:
        - model version uuid (`vuuid`) alone
        - model (`muuid`, or `model_name`) combined with version (`version_name`, or `default_muuid`)

        Args:
          vuuid: model version uuid
          version_name: version name
          muuid: model uuid
          model_name: model name
          default_muuid: default model uuid

        Returns:
          model version info dict, or `None` when the model version is not found
        """
        try:
            with self._registry_file.open('rt') as reg_file:
                reg_data = json.load(reg_file)
                if not vuuid:
                    if not muuid and not model_name:
                        muuid = default_muuid
                    vuuid = self._find_model_version(
                        reg_data=reg_data, version_name=version_name,
                        muuid=muuid, model_name=model_name)
                return reg_data[vuuid]
        except (FileNotFoundError, KeyError, ModelVersionNotFoundException) as e:
            logger.warning(e)
            return None

    def set_model_version_info(self, puuid: str, muuid: str, model_name: str,
                               vuuid: str, version_name: str,
                               packaged: bool, encrypted: bool,
                               download_time: datetime):
        """Sets model version record in local registry."""
        if not self._registry_file.exists():
            with self._registry_file.open('wt') as reg_file:
                reg_file.write('{}')

        with self._registry_file.open('rt+') as reg_file:
            reg_data = json.load(reg_file)
            reg_data[vuuid] = {
                'puuid': puuid,
                'muuid': muuid,
                'model_name': model_name,
                'vuuid': vuuid,
                'version_name': version_name,
                'packaged': packaged,
                'encrypted': encrypted,
                'download_time': download_time.isoformat()
            }
            reg_file.seek(0)
            json.dump(reg_data, reg_file, indent=2)
            reg_file.write('\n')
