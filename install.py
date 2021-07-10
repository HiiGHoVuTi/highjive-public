
import os
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



SDL_PATH = "https://github.com/libsdl-org/SDL"

def execute_commands(name, commands):
    for command in commands:
        exit_code = os.system(command())
        if exit_code != 0:
            TColors.print_error("Couldn't install the dependencies.", "Failed at step: " + name, ["While executing", command(), "Read trace above."])
            return False
    TColors.print_success("Done with step: " + name)
    return True

def magic_curl(owner, repo):
    return f"curl -L -o tmp.tar.gz $(curl -s https://api.github.com/repos/{owner}/{repo}/releases/latest | grep \"tarball_url\" | cut -d : -f 2,3 | tr -d \\\" | tr -d ',')"

def glob_sdl_folder():
    return glob("libsdl*")[0]

def glob_mixer_folder():
    return glob("hunter*")[0]

def glob_aubio_folder():
    return glob("aubio*")[0]

sdl_posix_commands     = [
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
cd {glob_sdl_folder()}
cd build
make
sudo make install
"""
]
mixer_posix_commands   = [
    lambda: magic_curl("hunter-packages", "SDL_mixer"),
    lambda: "tar -xf tmp.tar.gz",
    lambda:
f"""
cd {glob_mixer_folder()}
cmake .
"""
]
sdl_windows_commands   = []
mixer_windows_commands = []
aubio_posix_commands   = [
    lambda: "pip install aubio"
]
cleanup_posix_commands = [
    lambda: "rm -rf ./*/",
    lambda: "rm tmp.tar.gz"
]


if __name__ == "__main__":
    if os.name == "posix":
        if not execute_commands("SDL Installation", sdl_posix_commands):
            exit()
        if not execute_commands("SDL Mixer Installation", mixer_posix_commands):
            exit()
        if not execute_commands("Aubio Installation", aubio_posix_commands):
            exit()
        if not execute_commands("Cleanup", cleanup_posix_commands):
            exit()
    else:
        TColors.print_error("Your OS isn't supported (yet)", "You can try to install the dependencies on your own, or wait for official support.", ["Required packages:", "- SDL", "- SDL Mixer", "- Aubio (aubioonset)"])
