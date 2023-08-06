import os

import pretty_errors
# from .widgets import timer


class Cli:
    def __init__(self):
        ...

    @staticmethod
    def save_docker_images(filedir='.', skip_exists=True, use_stream=False):
        kwargs = locals()
        from .docker import save_docker_images
        return save_docker_images(**kwargs)

    @staticmethod
    def load_docker_images(filename_pattern="./*", skip_exists=True):
        kwargs = locals()
        from .docker import load_docker_images
        return load_docker_images(**kwargs)

    @staticmethod
    def docker_gpu_stat():
        from .docker.nvidia_stat import docker_gpu_stat
        return docker_gpu_stat()

    @staticmethod
    def pack(source_path: str, target_path=None, format='gztar'):
        kwargs = locals()
        from .utils.compress import pack
        return pack(**kwargs)

    @staticmethod
    def unpack(filename: str, extract_dir=None, format=None):
        kwargs = locals()
        from .utils.compress import unpack
        return unpack(**kwargs)

    @staticmethod
    def start_server(port=50001, deque_maxlen=None):
        kwargs = locals()
        from .multiprocess import start_server
        return start_server(**kwargs)

    @staticmethod
    def kill(*ports: int, view=False):
        from .multiprocess import kill
        return kill(*ports, view)

    @staticmethod
    def clone(url: str, repo_name=None, branch=None):
        kwargs = locals()
        from .cli import clone
        return clone(**kwargs)

    @staticmethod
    def get_ip(env="inner"):
        kwargs = locals()
        from .utils.net import get_ip
        return get_ip(**kwargs)

    @staticmethod
    def create(project_name: str, out=None):
        """创建项目
        Parameter
        ---------
        project_name : str
            package name
        out : str | None
            项目生成路径
        """
        if out is None:
            out = project_name
        from .template.scaffold.core import create_project
        return create_project(project_name, out)

    @staticmethod
    def milvus(flag='start'):
        kwargs = locals()
        from .ann import milvus
        return milvus(**kwargs)

    @staticmethod
    def latexocr():
        os.system("latexocr")


def fire_commands():
    import fire
    fire.Fire(Cli)


def typer_commands():
    import typer
    app = typer.Typer()
    # [app.command()(i) for i in func_list]
    # app()


def main():
    use_fire = 1
    if use_fire:
        fire_commands()
    else:
        # Fixme *形参 传入会出错，参考这里 https://typer.tiangolo.com/tutorial/multiple-values/arguments-with-multiple-values/
        typer_commands()
