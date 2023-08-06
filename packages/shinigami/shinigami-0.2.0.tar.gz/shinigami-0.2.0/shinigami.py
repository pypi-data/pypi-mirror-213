"""
    Project: Shinigami (https://github.com/shinigamilib/shinigami)
    Author: azazelm3dj3d (https://github.com/azazelm3dj3d)
    License: BSD 2-Clause
"""

import os, requests, sys
import argparse

# Logging library
from faye.faye import Faye

class Shinigami:
    """
    Shinigami is an open source Python library allowing the user to generate and build Dockerfiles during runtime.
    
    `lang_os` rtype: `str` - The language or operating system you would like to pull from DockDB (Example: `ubuntu`)
    
    `version` rtype: `str` - The version of the language or operating system (Example: `22.04`)
    
    `build` rtype: `bool` - This allows you to choose if you would like to build the Docker container during runtime
    
    `verbose` rtype: `bool` - Logs information to stdout

    `color` rtype: `bool` - Add some color to your logs
    """

    def __init__(self, lang_os="", version="", build=False, verbose=False, color=False):
        self.lang_os = lang_os
        self.version = version
        self.build = build
        self.verbose = verbose
        self.color = color

    def generate_dockerfile(self):
        """
        Generate a Dockerfile in the current working directory
        """
        
        try:

            # Queries open source Dockerfile repository
            docker_data = requests.get(f"https://raw.githubusercontent.com/shinigamilib/DockDB/main/DockDB/{self.lang_os}/{self.version}/Dockerfile")

            # Checks the status code for the repository connection
            if docker_data.status_code == 200:
                with open("Dockerfile", "w") as f:
                    f.write(docker_data.text)

                if self.verbose:
                    # Grab the size of the Dockerfile
                    dockerfile_size = os.path.getsize("Dockerfile")

                    if self.verbose:
                        # Displays a progress bar for download
                        Faye.progress(total=dockerfile_size, description="Dockerfile")

                if os.path.exists("Dockerfile"):
                    if self.verbose:
                        print(Faye.log(msg="Downloading Dockerfile complete", level="INFO", color=self.color))
                    else:
                        pass

            # Allows the user to build the Docker container during runtime (+ Dockerfile generation)
            if docker_data.status_code == 200 and self.build:
                with open("Dockerfile", "w") as f:
                    f.write(docker_data.text)

                if os.path.exists("requirements.txt"):
                    # Builds the Docker container
                    # NOTE: This requires Docker to be installed on the user's system and be configured in the PATH
                    os.system(f"docker build . -t shinigami-{self.lang_os}{self.version}")

                    if self.verbose:
                        print(Faye.log(msg="Successfully built Docker container", level="INFO", color=self.color))
                else:
                    print(Faye.log(msg="Missing requirements.txt", level="WARNING", color=self.color))
                    sys.exit()

            # If the Dockerfile doesn't exist, we do a clean exit
            if docker_data.status_code != 200:
                if self.verbose:
                    print(Faye.log(msg="This Docker configuration is not currently supported", level="WARNING", color=self.color))
                
                sys.exit()
        
        except Exception as e:
            return e

    def remove_dockerfile(self):
        """
        Remove the Dockerfile in the current working directory
        """

        if os.path.exists("Dockerfile"):
            os.system("rm Dockerfile")

            if self.verbose:
                # Grab the size of the Dockerfile
                dockerfile_size = os.path.getsize("Dockerfile")

                # Displays a progress bar for removal status
                Faye.progress(total=dockerfile_size, description="Dockerfile")

        if os.path.exists("Dockerfile") != True:
            if self.verbose:
                print(Faye.log(msg="Successfully removed Dockerfile", level="INFO", color=self.color))
            else:
                pass

class CLI:
    def run():
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--image', help="Docker image to generate", default=None, required=False)
        parser.add_argument('-v', '--version', help="Version of the Docker image", default=None, required=False)
        parser.add_argument('-b', '--build', help="Build the Dockerfile after generation", action='store_true', default=False, required=False)
        parser.add_argument('-c', '--color', help="Generate a color output", action='store_true', default=False, required=False)
        parser.add_argument('-rm', '--remove', help="Remove the Dockerfile in the current working directory", action='store_true', default=False, required=False)
        args = parser.parse_args()

        v = "0.2.0"

        banner = \
        f"""
         _____ _     _       _                       _   _____  _     _____ 
        /  ___| |   (_)     (_)                     (_) /  __ \| |   |_   _|
        \ `--.| |__  _ _ __  _  __ _  __ _ _ __ ___  _  | /  \/| |     | |  
         `--. \ '_ \| | '_ \| |/ _` |/ _` | '_ ` _ \| | | |    | |     | |  
        /\__/ / | | | | | | | | (_| | (_| | | | | | | | | \__/\| |_____| |_ 
        \____/|_| |_|_|_| |_|_|\__, |\__,_|_| |_| |_|_|  \____/\_____/\___/ 
                                __/ |                                       
                               |___/                                        

        Shinigami CLI | v{v}
        Author: https://github.com/azazelm3dj3d
        Learn more: https://github.com/shinigamilib/shinigami
        """

        print(banner)

        if args.remove:
            return Shinigami().remove_dockerfile()

        if args.build:
            return Shinigami(lang_os=str(args.image), version=str(args.version), build={args.build}, color={args.color}).generate_dockerfile()

        if args.image != None or args.version != None:
            return Shinigami(lang_os=str(args.image), version=str(args.version), verbose=True, color={args.color}).generate_dockerfile()
        else:
            print("Missing one or more arguments: --image, --version (you can use -h if you need help)")
