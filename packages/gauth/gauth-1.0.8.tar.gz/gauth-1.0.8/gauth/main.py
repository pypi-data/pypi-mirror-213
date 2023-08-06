import sys
import os
import argparse
import pyotp
import tempfile
import json
import yaml
from PIL import Image
from contextlib import contextmanager
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))


def check_img(filename):
    try:
        im = Image.open(filename)
        im.verify()
        im.close()
        im = Image.open(filename)
        im.transpose(Image.FLIP_LEFT_RIGHT)
        im.close()
        return True
    except:
        return False


def check_yaml(filename):
    if filename.endswith('.yaml') or filename.endswith('.yml'):
        return True
    else:
        return False


@contextmanager
def silence_stdout():
    old_target = sys.stdout
    old_stderr = sys.stderr
    try:
        with open(os.devnull, "w") as new_target:
            sys.stdout = new_target
            sys.stderr = new_target
            yield new_target
    finally:
        sys.stdout = old_target
        sys.stderr = old_stderr


def main():
    parser = argparse.ArgumentParser(description='Tool to help migrate Google Authenticator from phone to desktop')
    parser.add_argument('-p', '--path', help='file path to the exported qr code or text file, or yaml file', required=True)
    parser.add_argument('-n', '--name', help='otp name', required=False)
    args = parser.parse_args()
    if args.path:
        if check_yaml(args.path):
            with open(args.path, "r") as yaml_file:
                config = yaml.safe_load(yaml_file)
                for e in config['keys']:
                    totp = pyotp.TOTP(e['Secret'].strip())
                    print(f"{e['Issuer'].ljust(15)} {e['Name'].ljust(38)}: {totp.now()}")
        else:
            if check_img(args.path):
                from gauth.extract import extract_otp_secrets
            else:
                with silence_stdout():
                    from gauth.extract import extract_otp_secrets
            with tempfile.NamedTemporaryFile() as tmp:
                params = [args.path, '--json', tmp.name, '--quiet', '--ignore']
                extract_otp_secrets.main(params)
                otps(json.load(tmp), args.name)


def otps(config, name):
    for e in config:
        if name is not None and name == e['name']:
            otp(e['name'], e['issuer'], e['secret'].strip())
        elif name is None:
            otp(e['name'], e['issuer'], e['secret'].strip())


def otp(totp_name, issuer, totp_secret):
    # Create a TOTP object
    totp = pyotp.TOTP(totp_secret)

    # Print the current TOTP value
    print(f"{issuer.ljust(15)} {totp_name.ljust(38)}: {totp.now()}")


if __name__ == '__main__':
    main()

