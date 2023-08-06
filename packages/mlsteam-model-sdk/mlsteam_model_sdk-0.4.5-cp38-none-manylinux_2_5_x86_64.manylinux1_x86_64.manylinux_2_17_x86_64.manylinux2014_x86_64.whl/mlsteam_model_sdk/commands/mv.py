import sys

import click
import texttable

from mlsteam_model_sdk.core.registry import Registry
from mlsteam_model_sdk.utils.config import get_config_path


MV_COLS = ['muuid', 'model_name', 'vuuid', 'version_name', 'puuid', 'packaged', 'encrypted', 'download_time']


@click.group(help='model version operations')
def mv():
    pass


@mv.command(name='list-local',  help='list local model versions')
def list_local():
    reg = Registry(get_config_path(check=True).parent)
    mvs = reg.list_model_versions()

    table = texttable.Texttable(max_width=0)
    table.set_deco(texttable.Texttable.HEADER)
    table.header(MV_COLS)
    for _mv in mvs.values():
        table.add_row([_mv[c] for c in MV_COLS])
    click.echo(table.draw())


@mv.command(name='get-local', help='get local model version info')
@click.option('--vuuid', help='version uuid')
@click.option('--version_name', help='version name')
@click.option('--muuid', help='model uuid')
@click.option('--model_name', help='model name')
def get_local(vuuid, version_name, muuid, model_name):
    reg = Registry(get_config_path(check=True).parent)
    _mv = reg.get_model_version_info(vuuid=vuuid,
                                     version_name=version_name,
                                     muuid=muuid,
                                     model_name=model_name)
    if _mv is None:
        click.echo('Model version not found', err=True)
        sys.exit(1)

    table = texttable.Texttable(max_width=0)
    table.set_deco(texttable.Texttable.HEADER)
    table.header(MV_COLS)
    table.add_row([_mv[c] for c in MV_COLS])
    click.echo(table.draw())


@mv.command(name='import-local', help='import a model version package')
@click.option('-f', '--pkg_file', required=True,
              type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True),
              help='model version package file')
@click.option('-k', '--enckey_file',
              type=click.Path(exists=True, file_okay=True, readable=True, resolve_path=True),
              help='model version package encryption key file (required for encrypted packages)')
@click.option('--model_name', help='model name to register (a default value is used if not given)')
@click.option('--version_name', help='version name to register (a default value is used if not given)')
def import_local(pkg_file, enckey_file, model_name, version_name):
    from mlsteam_model_sdk.sdk.model import Model
    model_sdk = Model(offline=True)
    model_sdk.import_model_version(mv_package_file=pkg_file,
                                   enckey_file=enckey_file,
                                   model_name=model_name,
                                   version_name=version_name,
                                   logging=True)
