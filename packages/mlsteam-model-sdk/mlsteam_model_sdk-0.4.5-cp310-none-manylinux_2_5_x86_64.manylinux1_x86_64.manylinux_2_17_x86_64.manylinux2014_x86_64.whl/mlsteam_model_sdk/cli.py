import click

import mlsteam_model_sdk.commands.init
import mlsteam_model_sdk.commands.install_themisdev
import mlsteam_model_sdk.commands.mv


@click.group()
def cli():
    pass


cli.add_command(mlsteam_model_sdk.commands.init.cmd, name='init')
cli.add_command(mlsteam_model_sdk.commands.install_themisdev.cmd, name='install-themisdev')
cli.add_command(mlsteam_model_sdk.commands.mv.mv, name='mv')


if __name__ == '__main__':
    cli()
