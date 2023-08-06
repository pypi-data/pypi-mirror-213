import tarfile
from io import BytesIO
from typing import List, Union

from train_lib.docker_util.docker_ops import add_archive

from docker.models.images import Image


def make_docker_file(
    master_image: str,
    entrypoint_file: str,
    command: str,
    command_args: Union[List[str], str] = None,
) -> BytesIO:
    """
    Make an in memory docker file for a local train
    Args:
        master_image: identifier of the base image to build the train on
        entrypoint_file: which file to use as the entrypoint
        command:
        command_args:

    Returns:

    """

    print(master_image, entrypoint_file, command, command_args)
    docker_from = f"FROM {master_image}\n"
    directory_setup = (
        "RUN mkdir /opt/train && mkdir /opt/results && chmod -R +x /opt/train \n"
    )

    if isinstance(command_args, str):
        command_args = command_args.split(" ")
    if command_args:
        command_args = [f'"{arg}"' for arg in command_args]
        str_args = ", ".join(command_args) + ", "
    else:
        str_args = ""

    docker_command = f'CMD ["{command}", {str_args}"/opt/train/{entrypoint_file}"]\n'

    docker_file = docker_from + directory_setup + docker_command

    return BytesIO(docker_file.encode("utf-8"))


def add_train_files(train_id: str, image: Image, files):
    archive = _make_archive(files)
    print(image.id)
    add_archive(f"{train_id}:latest", archive, path="/opt/train")


def _make_archive(files: list) -> BytesIO:
    archive = BytesIO()
    tar = tarfile.open(fileobj=archive, mode="w")

    tar.close()
    # reset the archive
    archive.seek(0)

    return archive
