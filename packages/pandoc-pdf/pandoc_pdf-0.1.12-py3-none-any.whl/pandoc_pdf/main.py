from pandoc_pdf_utils.functions import (
    init_config,
    init_setting,
    init_cache,
    generate_command_docker,
    generate_command_pandoc,
)
from pandoc_pdf_utils.env import CACHE_DIR, CONFIG_DIR
from pathlib import Path
import subprocess
import click
import yaml
from copy import deepcopy

init_config()
with open(CONFIG_DIR / "defaults.yml") as f:
    presets = [key_i for key_i in yaml.safe_load(f)]


@click.command()
@click.option("--debug", is_flag=True)
@click.option("-D", "--docker", type=str)
@click.option(
    "-v",
    "--volume",
    type=str,
    multiple=True,
)
@click.option("-V", "--variable", type=str, multiple=True)
@click.option("-M", "--metadata", type=str, multiple=True)
@click.option("-p", "--preset", type=click.Choice(presets), default="latex")
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default="NULL",
)
@click.argument(
    "input_file",
    type=click.Path(exists=True, path_type=Path),
)
def pandoc_pdf(
    input_file: Path, debug: bool, docker, volume, metadata, variable, preset, output
):
    """Command to generate pdf easily with pandoc."""
    output_file = deepcopy(output)
    volumes = deepcopy(volume)
    variables = deepcopy(variable)
    metadatas = deepcopy(metadata)
    if str(output_file) == "NULL":
        output_file = Path(f"{input_file.parent / input_file.stem}.pdf")
    init_cache()
    setting_obj = init_setting(docker, volumes)
    if setting_obj["docker"]["use_docker"]:
        defaults_file = Path(f"/cache/defaults_{preset}.yml")
    else:
        defaults_file = CACHE_DIR / f"defaults_{preset}.yml"

    # * ---Execute command
    args_docker = generate_command_docker(setting_obj)
    args_pandoc = generate_command_pandoc(
        setting_obj,
        defaults_file,
        input_file,
        output_file,
        preset,
        variables,
        metadatas,
    )
    if setting_obj["docker"]["use_docker"]:
        args = " ".join(args_docker) + f" \"{' '.join(args_pandoc)}\""
    else:
        args = " ".join(args_pandoc)
    result = subprocess.run(args, shell=True)

    # * ---Print result
    result_status = "Succeeded" if result.returncode == 0 else "Failed"
    result_color = "" if result.returncode == 0 else "red"
    click.secho(
        f"{result_status} to generate {str(output_file)} from {str(input_file)} by {preset}.",
        fg=result_color,
        bold=True,
    )

    if debug:
        click.secho("\n---< DEBUG >---", fg="red")
        click.secho("Executed command:")
        click.secho(f"  {result.args}", bold=True)

    return result.returncode


if __name__ == "__main__":
    pandoc_pdf()
