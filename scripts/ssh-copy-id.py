import os
import subprocess

from secrets import PUBLICKEY_FILE, SERVER_INFO


def check_file(file):
    """Check if a file exists."""
    if not os.path.isfile(file):
        print(f"Public Key file does not exist in {file}.")
        return False
    else:
        print(f"Using Public Key in {file}:")
        return True


def push_key(user, ip, port, password):
    """Push a SSH Key to a remote server."""

    print(f"\tPushing to {user}@{ip}:{port}")

    command = f"sshpass -p {password} ssh-copy-id -i {PUBLICKEY_FILE} -p {port} {user}@{ip}"

    output = subprocess.run(command, shell=True,
                            capture_output=True)
    if output.returncode != 0:
        print(output)
        return False
    return True


def main():
    # check public key file exists
    if not check_file(PUBLICKEY_FILE):
        exit(1)

    # push keys to remote servers
    for info, password in SERVER_INFO.items():
        info = info.split(":")
        user, ip = info[0].split("@")
        port = info[1] if len(info) > 1 else 22
        if not push_key(user, ip, port, password):
            exit(1)
    print(
        f"##################################################\nSuccessfully pushed {len(SERVER_INFO)} SSH keys to remote servers\n##################################################")


if __name__ == "__main__":
    main()
