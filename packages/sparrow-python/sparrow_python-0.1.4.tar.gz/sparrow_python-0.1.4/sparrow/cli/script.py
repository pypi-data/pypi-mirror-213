import os
from sparrow.cli.core import command
from rich import print


def install_node(version='16.x'):
    args = f"curl -sL https://deb.nodesource.com/setup_{version} -o /tmp/nodesource_setup.sh"
    os.system(args)
    os.system("sudo bash /tmp/nodesource_setup.sh")
    print("Update nodesource success, please exec command `apt install nodejs -y` to install Node.js v{version}")

def install_node_with_nvm(version='16'):
    args = f"curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash"
    os.system(args)
    os.system(f"nvm install {version}")
    print("Install Node.js success, please exec command `nvm use {version}` to use Node.js v{version}")

def install_neovim(version="0.8.0"):
    args = f"RUN wget https://github.com/neovim/neovim/releases/download/v{version}/nvim-linux64.deb && " \
           f"sudo apt install ./nvim-linux64.deb"
    os.system(args)
    print(f"Install neovim {version} success.")
