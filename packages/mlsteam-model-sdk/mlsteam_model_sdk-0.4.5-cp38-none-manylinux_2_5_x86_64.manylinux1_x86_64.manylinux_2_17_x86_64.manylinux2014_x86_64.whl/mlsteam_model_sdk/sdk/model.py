"""Main model SDK interface"""
import base64
import contextlib
import importlib
import io
import json
import re
import shutil
import sys
import tempfile
import zipfile
from collections.abc import Callable
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any, List, Optional

from mlsteam_model_sdk.core.api_client import ApiClient
from mlsteam_model_sdk.core.encrypt import (ClientStorageModelSealer, ClientServerExchSealer,
                                            ModelImportSealer, PeerMsgKeypair, PeerMsgSealer, TrunkIO)
from mlsteam_model_sdk.core.exceptions import MLSteamException
from mlsteam_model_sdk.core.registry import Registry
from mlsteam_model_sdk.utils import config
from mlsteam_model_sdk.utils.log import logger, null_logger
from mlsteam_model_sdk.utils.typing import PathLike


class MVPackage:
    """Model version package.

    A delegator to make model operations such as prediction.
    """

    def __init__(self, model, predictor: Callable, manifest: dict, env: dict,
                 encrypted: bool = False,
                 decdir: Optional[tempfile.TemporaryDirectory] = None) -> None:
        self.__model = model
        self.__predictor = predictor
        self.__decdir = decdir
        self.__env = self._clone_dict_simple(env)
        self._manifest = self._clone_dict_simple(manifest)
        self._encrypted = encrypted
        self._closed = False

    def _clone_dict_simple(self, src_dict: dict) -> dict:
        return json.loads(json.dumps(src_dict))

    def __enter__(self) -> 'MVPackage':
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        """Manually closes the package.

        It tries to release the enclosed packaged resources.
        Nothing will happen if the package is closed twice.
        """
        # TODO: support model closing hook
        if self._closed:
            return
        self.__model = None
        self.__predictor = None
        if self.__decdir:
            self.__decdir.cleanup()
            self.__decdir = None
        self._closed = True

    @property
    def closed(self) -> bool:
        """Indicates whether the packaged is closed."""
        return self._closed

    @property
    def encrypted(self) -> bool:
        """Indicates whether the package is encrypted."""
        return self._encrypted

    @property
    def models(self) -> List[dict]:
        """Returns information for all included models."""
        return self._clone_dict_simple(self._manifest['models'])

    def get_model(self, index: int) -> dict:
        """Returns information for an included model."""
        return self._clone_dict_simple(self._manifest['models'][index])

    def predict(self, inputs, *args, **kwargs) -> Any:
        """Makes model predictions.

        Args:
          inputs: model inputs
          *args: custom arguments
          **kwargs: custom arguments

        Returns:
          model outputs
        """
        outputs = self.__predictor(
            env=self._clone_dict_simple(self.__env),
            model=self.__model, inputs=inputs, *args, **kwargs)
        return outputs


class Model:
    """Provides high-level model operations."""

    def __init__(self,
                 api_client: Optional[ApiClient] = None,
                 default_puuid: Optional[str] = None,
                 default_project_name: Optional[str] = None,
                 default_muuid: Optional[str] = None,
                 default_model_name: Optional[str] = None,
                 offline: bool = False) -> None:
        """Initilizes a model operator.

        Default project is determined with the following precedence:
          - default_puuid [argument]
          - default_project_name [argument]
          - default_puuid [config]
          - default_project_name [config]
          - None

        Default muuid is determined with the following precedence:
          - default_muuid [argument]
          - default_model_name [argument]
          - default_muuid [config]
          - default_model_name [config]
          - None

        Args:
          api_client: API client. Creates a new API client if it is not given and not in offline mode.
          default_puuid: default project uuid
          default_project_name: default project name
          default_muuid: default model uuid
          default_model_name: default model name
          offline: offline mode. Only offline operations could be used in offline mode if api_client is not given.
        """
        if not api_client and not offline:
            api_client = ApiClient()
        self.api_client = api_client
        self._registry = None
        self.offline = offline

        self.__init_default_puuid(
            default_puuid=default_puuid,
            default_project_name=default_project_name)
        self.__init_default_muuid(
            default_muuid=default_muuid,
            default_model_name=default_model_name)

    def __init_default_puuid(self,
                             default_puuid: Optional[str] = None,
                             default_project_name: Optional[str] = None):
        if False:
            default_project_name = default_puuid = NotImplemented

        def _walrus_wrapper_default_project_name_13f8be9a95384e71b2de0f5566fec111(expr):
            """Wrapper function for assignment expression."""
            nonlocal default_project_name
            default_project_name = expr
            return default_project_name

        def _walrus_wrapper_default_puuid_b0a027b0b80a409cb215a02ad6fd4583(expr):
            """Wrapper function for assignment expression."""
            nonlocal default_puuid
            default_puuid = expr
            return default_puuid

        if default_puuid:
            self.default_puuid = default_puuid
        elif default_project_name:
            self.default_puuid = self.to_puuid(default_project_name)
        elif (_walrus_wrapper_default_puuid_b0a027b0b80a409cb215a02ad6fd4583(config.get_value(config.OPTION_DEFAULT_PUUID))):
            self.default_puuid = default_puuid
        elif (_walrus_wrapper_default_project_name_13f8be9a95384e71b2de0f5566fec111(config.get_value(config.OPTION_DEFAULT_PROJECT_NAME))):
            self.default_puuid = self.to_puuid(default_project_name)
        else:
            self.default_puuid = None

    def __init_default_muuid(self,
                             default_muuid: Optional[str] = None,
                             default_model_name: Optional[str] = None):
        if False:
            default_model_name = default_muuid = NotImplemented

        def _walrus_wrapper_default_model_name_4d1dfc59e0b44b0eadd06dd94d79878e(expr):
            """Wrapper function for assignment expression."""
            nonlocal default_model_name
            default_model_name = expr
            return default_model_name

        def _walrus_wrapper_default_muuid_c9d2a6454f24461baef79a1f84d5b812(expr):
            """Wrapper function for assignment expression."""
            nonlocal default_muuid
            default_muuid = expr
            return default_muuid

        if default_muuid:
            self.default_muuid = default_muuid
        elif default_model_name:
            self.default_muuid = self.to_muuid(default_model_name, puuid=self.default_puuid)
        elif (_walrus_wrapper_default_muuid_c9d2a6454f24461baef79a1f84d5b812(config.get_value(config.OPTION_DEFAULT_MUUID))):
            self.default_muuid = default_muuid
        elif (_walrus_wrapper_default_model_name_4d1dfc59e0b44b0eadd06dd94d79878e(config.get_value(config.OPTION_DEFAULT_MODEL_NAME))):
            self.default_muuid = self.to_muuid(default_model_name, puuid=self.default_puuid)
        else:
            self.default_muuid = None

    def _get_registry(self) -> Registry:
        if not self._registry:
            config_dir = config.get_config_path(check=True).parent
            self._registry = Registry(config_dir=config_dir)
        return self._registry

    def _get_puuid(self, puuid: Optional[str] = None, check: bool = False) -> Optional[str]:
        if not puuid:
            puuid = self.default_puuid
        if check and not puuid:
            raise ValueError('Invalid project specification')
        return puuid

    def _get_muuid(self, puuid: str,
                   muuid: Optional[str] = None,
                   model_name: Optional[str] = None,
                   check: bool = False) -> Optional[str]:
        if not muuid:
            if model_name:
                muuid = self.to_muuid(model_name, puuid=puuid)
            else:
                muuid = self.default_muuid
        if check and not muuid:
            raise ValueError('Invalid model specification')
        return muuid

    def _get_vuuid(self, puuid: str, muuid: str,
                   vuuid: Optional[str] = None,
                   version_name: Optional[str] = None,
                   check: bool = False) -> Optional[str]:
        if not vuuid:
            vuuid = self.to_vuuid(version_name, muuid=muuid, puuid=puuid)
        if check and not vuuid:
            raise ValueError('Invalid model version specification')
        return vuuid

    @lru_cache(maxsize=10)
    def to_puuid(self, project_name: str) -> str:
        """Converts project name to project uuid."""
        project = self.api_client.get_project(project_name=project_name)
        return project['uuid']

    @lru_cache(maxsize=100)
    def to_muuid(self, model_name: str, puuid: Optional[str] = None) -> str:
        """Converts model name to model uuid."""
        model = self.api_client.get_model(
            puuid=self._get_puuid(puuid),
            model_name=model_name)
        return model['uuid']

    @lru_cache(maxsize=100)
    def to_vuuid(self,
                 version_name: str,
                 muuid: Optional[str] = None,
                 puuid: Optional[str] = None) -> str:
        """Converts model version name to model version uuid."""
        version = self.api_client.get_model_version(
            puuid=self._get_puuid(puuid),
            muuid=muuid or self.default_muuid,
            version_name=version_name)
        return version['uuid']

    def list_models(self, puuid: Optional[str] = None) -> List[dict]:
        """Lists models.

        Args:
          puuid: optional, project uuid to use rather than the default project

        Returns:
          models

        Raises:
          ValueError: An error occurred determining the project.
        """
        puuid = self._get_puuid(puuid, check=True)
        models = self.api_client.list_models(puuid=puuid)
        return models

    def get_model(self,
                  muuid: Optional[str] = None,
                  model_name: Optional[str] = None,
                  puuid: Optional[str] = None) -> dict:
        """Gets model info.

        The model should be given and is determined with the following precedence:
          - muuid
          - model_name
          - default model

        Args:
          muuid: model uuid
          model_name: model name
          puuid: optional, project uuid to use rather than the default project

        Returns:
          model info

        Raises:
          ValueError: An error occurred determining the project or the model.
        """
        puuid = self._get_puuid(puuid, check=True)
        muuid = self._get_muuid(puuid, muuid=muuid, model_name=model_name, check=True)
        model = self.api_client.get_model(puuid=puuid, muuid=muuid)
        return model

    def list_model_versions(self,
                            muuid: Optional[str] = None,
                            model_name: Optional[str] = None,
                            puuid: Optional[str] = None) -> List[dict]:
        """Lists model versions.

        The model should be given and is determined in the same way as in `get_model()`.

        Args:
          muuid: model uuid
          model_name: model name
          puuid: optional, project uuid to use rather than the default project

        Returns:
          model versions

        Raises:
          ValueError: An error occurred determining the project or the model.
        """
        puuid = self._get_puuid(puuid, check=True)
        muuid = self._get_muuid(puuid, muuid=muuid, model_name=model_name, check=True)
        versions = self.api_client.list_model_versions(puuid=puuid, muuid=muuid)
        return versions

    def get_model_version(self,
                          vuuid: Optional[str] = None,
                          version_name: Optional[str] = None,
                          muuid: Optional[str] = None,
                          model_name: Optional[str] = None,
                          puuid: Optional[str] = None) -> dict:
        """Gets model version info.

        The model version should be given and is determined with the following precedence:
          - muuid
          - model_name

        The model should be given and is determined in the same way as in `get_model()`.

        Args:
          vuuid: model version uuid
          version_name: model version name
          muuid: model uuid
          model_name: model name
          puuid: optional, project uuid to use rather than the default project

        Returns:
          model version

        Raises:
          ValueError: An error occurred determining the project, the model, or the model version.
        """
        puuid = self._get_puuid(puuid, check=True)
        muuid = self._get_muuid(puuid, muuid=muuid, model_name=model_name, check=True)
        vuuid = self._get_vuuid(puuid, muuid, vuuid=vuuid, version_name=version_name, check=True)
        version = self.api_client.get_model_version(puuid=puuid, muuid=muuid, vuuid=vuuid)
        return version

    @lru_cache(maxsize=1)
    def _get_download_keypair(self) -> PeerMsgKeypair:
        return PeerMsgKeypair()

    def _get_download_req(self) -> bytes:
        req_plain = {
            'client_pubkey': base64.b64encode(self._get_download_keypair().pubkey).decode(),
            'time': datetime.now(tz=timezone.utc).isoformat()
        }
        req_enc = ClientServerExchSealer().encrypt(json.dumps(req_plain).encode())
        req_enc = base64.b64encode(req_enc).decode()
        return req_enc

    def _extract_package(self, package_file, extract_dir):
        with zipfile.ZipFile(package_file, mode='r') as package_zip:
            package_zip.extractall(path=extract_dir)

    def _get_enc_package_file(self, extract_dir: Path) -> Path:
        return extract_dir / 'model-enc.mlarchive'

    def download_model_version(self,
                               vuuid: Optional[str] = None,
                               version_name: Optional[str] = None,
                               muuid: Optional[str] = None,
                               model_name: Optional[str] = None,
                               puuid: Optional[str] = None,
                               overwrite: bool = False,
                               logging: bool = False) -> str:
        """Downloads and extracts model version files or packages.

        The model version should be given and is determined in the same way as in `get_model_version()`.

        The model should be given and is determined in the same way as in `get_model()`.

        Args:
          vuuid: model version uuid
          version_name: model version name
          muuid: model uuid
          model_name: model name
          puuid: optional, project uuid to use rather than the default project
          overwrite: overwrite the existing downloaded files if there is any
          logging: enable logging

        Returns:
          path of model version extraction directory

        Raises:
          ValueError: An error occurred determining the project, the model, or the model version.
          FileExistsError: Model version exists and `overwrite` is not set.
        """
        puuid = self._get_puuid(puuid, check=True)
        muuid = self._get_muuid(puuid, muuid=muuid, model_name=model_name, check=True)
        vuuid = self._get_vuuid(puuid, muuid, vuuid=vuuid, version_name=version_name, check=True)
        _logger = logger if logging else null_logger

        mv = self.get_model_version(vuuid=vuuid, muuid=muuid, puuid=puuid)
        mv_packaged = mv['meta'].get('package', False)
        mv_encrypted = mv['meta'].get('encrypt', False)

        registry = self._get_registry()
        download_file = registry.get_download_file(
            vuuid=vuuid, packaged=mv_packaged, encrypted=mv_encrypted, create_dir=True)
        extract_dir = registry.get_extract_dir(vuuid=vuuid)
        if not overwrite and \
                extract_dir.exists() and registry.get_model_version_info(vuuid=vuuid):
            raise FileExistsError(f'Model version directory {extract_dir} already exists;'
                                  ' set overwrite=True to overwrite existing files')

        req = None
        if mv_encrypted:
            req = self._get_download_req()
        job = self.api_client.prepare_download_model_version(
            puuid=puuid, muuid=muuid, vuuid=vuuid, req=req)

        download_id = None
        if 'job_id' in job:
            prep_download_rsp = self.api_client.poll(job['job_id'], interval=10)
            download_id = prep_download_rsp['result']['download_id']
        elif 'download_id' in job:
            # After mlsteam async api job finished will return actual result.
            download_id = job['download_id']
        else:
            raise Exception(f'Downlaod model {model_name} {version_name} failed')

        _logger.info('Starts to download model version %s', vuuid)
        download_time = datetime.now()
        self.api_client.download_model_version(
            puuid=puuid, muuid=muuid, vuuid=vuuid,
            download_id=download_id, download_path=download_file)

        _logger.info('Starts to extract model version %s', vuuid)
        shutil.rmtree(extract_dir, ignore_errors=True)
        extract_dir.mkdir(parents=True, exist_ok=True)

        if mv_encrypted:
            with download_file.open('rb') as download_file_fp, \
                    self._get_enc_package_file(extract_dir).open('wb') as stor_file_fp:
                server_pubkey = ClientServerExchSealer().decrypt_file_trunk(download_file_fp)
                peer_sealer = PeerMsgSealer(self_privkey=self._get_download_keypair().privkey,
                                            peer_pubkey=server_pubkey)
                stor_sealer = ClientStorageModelSealer()
                peer_sealer.trunk_io.proc_file_in_trunks(
                    src_file=download_file_fp, dst_file=stor_file_fp,
                    read_mode=TrunkIO.Mode.LEN_BYTES, write_mode=TrunkIO.Mode.LEN_BYTES,
                    proc_func=lambda trunk: stor_sealer.encrypt(peer_sealer.unwrap(trunk)))
        elif mv_packaged:
            self._extract_package(package_file=download_file, extract_dir=extract_dir)
        else:
            with zipfile.ZipFile(download_file, mode='r') as download_zip:
                download_zip.extractall(path=extract_dir)

        _logger.info('Model version %s extraction is complete', vuuid)
        download_file.unlink()
        registry.set_model_version_info(
            puuid=puuid,
            muuid=muuid,
            model_name=model_name if model_name else self.get_model(muuid=muuid)['name'],
            vuuid=vuuid,
            version_name=mv['version'],
            packaged=mv_packaged,
            encrypted=mv_encrypted,
            download_time=download_time)

        return str(extract_dir.absolute())

    def import_model_version(self, mv_package_file: PathLike,
                             enckey_file: Optional[PathLike] = None,
                             model_name: Optional[str] = None,
                             version_name: Optional[str] = None,
                             logging: bool = False) -> str:
        """Imports a model version package from local files.

        This method could be used offline.

        `enckey_file` should be given if the package is encrypted.

        When `model_name` or `version_name` is not given, the corresponding fields
        in the package manifest are used instead.

        Args:
          mv_package_file: model version package file path
          enckey_file: enckey file path
          model_name: model name to register
          version_name: model version name to register
          logging: enable logging

        Returns:
          local vuuid for the imported model version

        Raises:
          ValueError: An error occurred determining the the model name or the version name.
        """
        _logger = logger if logging else null_logger
        mv_packaged = True
        mv_encrypted = bool(enckey_file)

        registry = self._get_registry()
        local_vuuid = registry.get_new_local_vuuid()
        download_file = registry.get_download_file(
            vuuid=local_vuuid, packaged=mv_packaged, encrypted=mv_encrypted, create_dir=True)
        extract_dir = registry.get_extract_dir(vuuid=local_vuuid)

        _logger.info('Starts to import model version %s', local_vuuid)
        download_time = datetime.now()
        shutil.copy2(mv_package_file, download_file)

        _logger.info('Starts to extract model version %s', local_vuuid)
        shutil.rmtree(extract_dir, ignore_errors=True)
        extract_dir.mkdir(parents=True, exist_ok=True)

        if mv_encrypted:
            with open(enckey_file, 'rb') as enckey_file_fp:
                enckey_exch = enckey_file_fp.read()
                enckey_raw = ClientServerExchSealer().decrypt(enckey_exch)
                import_sealer = ModelImportSealer.from_bytes(io.BytesIO(enckey_raw))

            with download_file.open('rb') as download_file_fp, \
                    tempfile.TemporaryFile('wb+') as temp_file_fp, \
                    self._get_enc_package_file(extract_dir).open('wb') as stor_file_fp:
                import_sealer.decrypt_file_from_trunks(download_file_fp, temp_file_fp)
                temp_file_fp.seek(0)
                with zipfile.ZipFile(temp_file_fp) as temp_zipfile:
                    with temp_zipfile.open('manifest.json') as manifest_fp:
                        manifest = json.load(manifest_fp)
                        default_model_name = manifest['models'][0]['name']
                        default_version_name = manifest['models'][0]['version']
                temp_file_fp.seek(0)
                ClientStorageModelSealer().encrypt_file_in_trunks(temp_file_fp, stor_file_fp)
        else:
            self._extract_package(package_file=download_file, extract_dir=extract_dir)
            with (extract_dir / 'manifest.json').open('rt') as manifest_fp:
                manifest = json.load(manifest_fp)
                default_model_name = manifest['models'][0]['name']
                default_version_name = manifest['models'][0]['version']

        _logger.info('Model version %s extraction is complete', local_vuuid)
        registry.set_model_version_info(
            puuid=registry.LOCAL_PUUID,
            muuid=registry.LOCAL_MUUID,
            model_name=model_name if model_name else default_model_name,
            vuuid=local_vuuid,
            version_name=version_name if version_name else default_version_name,
            packaged=mv_packaged,
            encrypted=mv_encrypted,
            download_time=download_time
        )

        return local_vuuid

    def get_model_version_dir(self,
                              vuuid: Optional[str] = None,
                              version_name: Optional[str] = None,
                              muuid: Optional[str] = None,
                              model_name: Optional[str] = None) -> str:
        """Gets model version storage path.

        This method could be used offline. It assumes has been downloaded by `download_model_version()`.
        NOTE: It only supports plaintext or plaintext-packaged model versions.

        It suffices to specify only vuuid to determine the model version. Otherwise, both
        the model and the model version should be given.

        Args:
          vuuid: model version uuid
          version_name: model version name
          muuid: model uuid
          model_name: model name

        Returns:
          model version storage path

        Raises:
          ValueError: An error occurred determining the project or the model or
            an encrypted model version is specified.
          MLSteamException: Illegal operation.
        """
        registry = self._get_registry()
        mv = registry.get_model_version_info(vuuid=vuuid, version_name=version_name,
                                             muuid=muuid, model_name=model_name,
                                             default_muuid=self.default_muuid)
        vuuid = mv['vuuid']
        if mv['encrypted']:
            raise MLSteamException(f'Cannot get the storage path for an encrypted model version (vuuid={vuuid})')
        return str(registry.get_extract_dir(vuuid=vuuid).absolute())

    def _update_sys_paths_modules(self, abs_syspath: Path, abs_pkgbase: Path):
        if False:
            abs_syspath_str = NotImplemented

        def _walrus_wrapper_abs_syspath_str_465f8854d63040b4ac43a25ee1fc625e(expr):
            """Wrapper function for assignment expression."""
            nonlocal abs_syspath_str
            abs_syspath_str = expr
            return abs_syspath_str

        if (_walrus_wrapper_abs_syspath_str_465f8854d63040b4ac43a25ee1fc625e(str(abs_syspath))) not in sys.path:
            sys.path.insert(0, abs_syspath_str)
            # attempt to cleanup the Python module cache for previous module loading
            rel_pkgbase = abs_pkgbase.relative_to(abs_syspath)
            _sep = r'[/\\]'
            cleanup_matcher = re.compile(f'(^|.*{_sep}){str(rel_pkgbase)}($|{_sep}.*)')
            for _mod_key in list(sys.modules.keys()):
                with contextlib.suppress(Exception):
                    _path = sys.modules[_mod_key].__file__
                    if cleanup_matcher.match(_path):
                        del sys.modules[_mod_key]
            for _path_idx in range(len(sys.path) - 1, 0, -1):
                with contextlib.suppress(Exception):
                    _path = sys.path[_path_idx]
                    if cleanup_matcher.match(_path):
                        del sys.path[_path_idx]
            importlib.invalidate_caches()

    def _load_hooks_module(self, module_name: str, syspath_dir: Path, pkgbase_dir: Path) -> ModuleType:
        self._update_sys_paths_modules(syspath_dir.absolute(), pkgbase_dir.absolute())

        mod_path = '.'.join(
            list(pkgbase_dir.relative_to(syspath_dir).parts) +
            ['hooks', module_name])
        mod = importlib.import_module(mod_path)
        return mod

    def _get_hooks_env(self, pkgbase_dir: Path) -> dict:
        env = {
            'MLSTEAM_MODEL_DIR': str(pkgbase_dir / 'models')
        }
        return env

    def load_model_version(self,
                           vuuid: Optional[str] = None,
                           version_name: Optional[str] = None,
                           muuid: Optional[str] = None,
                           model_name: Optional[str] = None,
                           *args, **kwargs) -> MVPackage:
        """Loads model version package.

        This method could be used offline. It assumes the model version is packaged and
        has been downloaded by `download_model_version()`.

        It suffices to specify only vuuid to determine the model version. Otherwise, both
        the model and the model version should be given.

        NOTE: When an encrypted model version packaged gets loaded twice, all previous loded
        hook modules for that package will be wiped out to avoid module loading errors.
        That is, all previous returned model version packages for that module are no longer
        usable. Make sure not to keep and use more than one model version package for a certain
        model version at the same time.

        Args:
          vuuid: model version uuid
          version_name: model version name
          muuid: model uuid
          model_name: model name
          *args: custom arguments
          **kwargs: custom arguments

        Returns:
          model version package

        Raises:
          ValueError: An error occurred determining the project or the model.
          MLSteamException: Illegal operation.
        """
        registry = self._get_registry()
        mv = registry.get_model_version_info(vuuid=vuuid, version_name=version_name,
                                             muuid=muuid, model_name=model_name,
                                             default_muuid=self.default_muuid)
        vuuid, packaged, encrypted = [mv[k] for k in ('vuuid', 'packaged', 'encrypted')]
        syspath_dir = registry.get_extract_base_dir().absolute()
        extract_dir = registry.get_extract_dir(vuuid).absolute()
        dec_dir = None

        if not packaged:
            raise MLSteamException(f'Cannot load a non-packaged model version (vuuid={vuuid}); '
                                   f'the files are at {self.get_model_version_dir(vuuid=vuuid)}')

        if encrypted:
            with self._get_enc_package_file(extract_dir).open('rb') as enc_package_fp:
                with tempfile.TemporaryFile('wb+') as package_fp:
                    stor_sealer = ClientStorageModelSealer()
                    stor_sealer.decrypt_file_from_trunks(src_file=enc_package_fp, dst_file=package_fp)
                    package_fp.seek(0)

                    dec_dir = tempfile.TemporaryDirectory()
                    syspath_dir = Path(dec_dir.name).absolute()
                    extract_dir = syspath_dir / vuuid
                    extract_dir.mkdir(parents=True, exist_ok=True)
                    self._extract_package(package_file=package_fp, extract_dir=extract_dir)

        load_mod = self._load_hooks_module('load', syspath_dir=syspath_dir, pkgbase_dir=extract_dir)
        predict_mod = self._load_hooks_module('predict', syspath_dir=syspath_dir, pkgbase_dir=extract_dir)
        with (extract_dir / 'manifest.json').open('rt') as manifest_file:
            manifest = json.load(manifest_file)
        env = self._get_hooks_env(pkgbase_dir=extract_dir)
        model = load_mod.load(env=env, *args, **kwargs)
        mv_package = MVPackage(model=model, predictor=predict_mod.predict,
                               manifest=manifest, env=env,
                               encrypted=encrypted, decdir=dec_dir)

        return mv_package
