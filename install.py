
import os
import platform
from glob import glob

class TColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print_error(header, text, trace):
        print("\n" + TColors.HEADER + TColors.UNDERLINE + TColors.FAIL + header + TColors.ENDC)
        print("\n" + text)
        print("\n" + TColors.WARNING + "\n".join(trace) + TColors.ENDC + "\n")

    @staticmethod
    def print_success(text):
        print(TColors.OKBLUE + "SUCCESS: " + text + TColors.ENDC)


def execute_commands(name, commands):
    for command in commands:
        exit_code = os.system(command())
        if exit_code != 0:
            TColors.print_error("Couldn't install the dependencies.", "Failed at step: " + name, ["While executing:", command(), "Read trace above."])
            return False
    TColors.print_success("Done with step: " + name)
    return True

def magic_curl(owner, repo):
    return f"curl -L -o tmp.tar.gz $(curl -s https://api.github.com/repos/{owner}/{repo}/releases/latest | grep \"tarball_url\" | cut -d : -f 2,3 | tr -d \\\" | tr -d ',')"

def glob_sdl_folder():
    return glob("libsdl*")[0]

def glob_mixer_folder():
    return glob("hunter*")[0]

sdl_linux_commands     = [
    lambda: magic_curl("libsdl-org", "SDL"),
    lambda: "tar -xf tmp.tar.gz",
    lambda:
f"""
cd {glob_sdl_folder()}
mkdir build
cd build
../configure
""",
    lambda:
f"""
cd {glob_sdl_folder()}/build
make
sudo make install
"""
]
mixer_linux_commands   = [
    lambda: magic_curl("libsdl-org", "SDL_mixer"),
    lambda: "tar -xf tmp.tar.gz",
    lambda:
f"""
cd {glob_mixer_folder()}
mkdir build
cd build
../configure
""",
    lambda:
f"""
cd {glob_mixer_folder()}/build
make
sudo make install
"""
]
sdl_windows_commands   = []
mixer_windows_commands = []
aubio_linux_commands   = [
    lambda: "pip install aubio"
]
cleanup_linux_commands = [
    lambda: "rm -rf " + glob_sdl_folder(),
    lambda: "rm -rf " + glob_mixer_folder(),
    lambda: "rm tmp.tar.gz"
]


if __name__ == "__main__":
    if platform.system() == "Linux":
        release = platform.release().upper()

        if "UBUNTU" in release or "DEBIAN" in release:
            execute_commands("Dependencies collection", [lambda: "sudo apt-get install libgtk2.0-dev libpango1.0-dev libglib2.0-dev libcairo2-dev libpangocairo-1.0-0 libsdl2-dev libsdl2-mixer-*-dev"])
            execute_commands("Aubio Installation", aubio_linux_commands)
            exit()

        if "MANJARO" in release or "ARCH" in release:
            execute_commands("SDL Installation", [lambda: "sudo pacman -S sdl2"])
            execute_commands("Mixer Installation", [lambda: "sudo pacman -S sdl2_mixer"])
            execute_commands("Aubio Installation", aubio_linux_commands)
            exit()

        if not execute_commands("SDL Installation", sdl_linux_commands):
            exit()
        if not execute_commands("SDL Mixer Installation", mixer_linux_commands):
            exit()
        if not execute_commands("Aubio Installation", aubio_linux_commands):
            exit()
        if not execute_commands("Cleanup", cleanup_linux_commands):
            exit()
    else:
        TColors.print_error("Your OS isn't supported (yet)", "You can try to install the dependencies on your own, or wait for official support.", ["Required packages:", "- SDL", "- SDL Mixer", "- Aubio (aubioonset)"])
