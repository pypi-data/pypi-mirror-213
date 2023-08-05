import argparse
import json
import os
import sys
from multiprocessing import Queue
from threading import Thread, Timer

import Quartz.CoreGraphics as cg
from AppKit import NSWorkspace, NSURL

sys.path.append('../')
from metalayer import config, CONFIG_PATH
from metalayer.consumer import CaptureConsumer
from metalayer.producer import CaptureProducer


def main():
    parser = argparse.ArgumentParser(prog='metalayer', description='metalayer command line interface.')
    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser('init', help='Knowledge repo initialization')
    parser_init.set_defaults(func=init)

    parser_run = subparsers.add_parser('run', help='Run metalayer and add to knowledge repo')
    parser_run.set_defaults(func=run)
    parser_run.add_argument('-i', '--capture-interval', type=float, default=1.,
                            help='Interval after no keyboard or mouse activity to capture a screenshot')
    parser_run.add_argument('-p', '--wait-for-power', action='store_true',
                            help='Wait until connected to external power before running OCR')
    parser_run.add_argument('-t', type=int, default=None,
                            help='Stop after T seconds. If not set, will run indefinitely.')

    parser_key = subparsers.add_parser('set-api-key', help='Set OpenAI API key')
    parser_key.set_defaults(func=set_api_key)
    parser_key.add_argument('key', type=str, help='OpenAI API key')

    parser_dir = subparsers.add_parser('set-vault-dir', help='Set Obsidian vault directory (knowledge repo root)')
    parser_dir.set_defaults(func=set_vault_dir)
    parser_dir.add_argument('dir', type=str, help='Obsidian vault directory')

    args = parser.parse_args()
    args.func(args)


def set_api_key(args):
    config.update({'openai_api_key': args.key})
    with open(os.path.join(CONFIG_PATH), 'w') as f:
        json.dump(config, f, indent=4)


def set_vault_dir(args):
    vault_dir = config.get('vault_dir')
    new_dir = os.path.expanduser(args.dir)
    if vault_dir == new_dir:
        print(f"[INFO] Vault directory already set to {args.dir}")
        return

    if vault_dir is not None:
        print(f"[INFO] Changing vault directory from {vault_dir} to {new_dir}")
        try:
            os.rename(vault_dir, new_dir)
        except Exception as e:
            print('[ERROR] Failed to move directory: {}'.format(new_dir))
            print(str(e))
            return
    else:
        print(f"[INFO] Setting vault directory to {new_dir}")
        try:
            os.makedirs(new_dir, exist_ok=True)
        except Exception as e:
            print('[ERROR] Failed to create directory: {}'.format(new_dir))
            print(str(e))
            return

    config.update({'vault_dir': new_dir})
    with open(os.path.join(CONFIG_PATH), 'w') as f:
        json.dump(config, f, indent=4)


def init(args):
    globe_string = """\

  ,ad8888ba,   88           ,ad8888ba,    88888888ba   88888888888  
 d8"'    `"8b  88          d8"'    `"8b   88      "8b  88           
d8'            88         d8'        `8b  88      ,8P  88           
88             88         88          88  88aaaaaa8P'  88aaaaa      
88      88888  88         88          88  88""\""\""8b,  88""\"""
Y8,        88  88         Y8,        ,8P  88      `8b  88
 Y8a.    .a88  88          Y8a.    .a8P   88      a8P  88
  `"Y88888P"   88888888888  `"Y8888Y"'    88888888P"   88888888888
  K N O W L E D G E   S O L U T I O N S   I N C O R P O R A T E D

"""
    print(globe_string)

    print('Before you begin, we need you to enable some permissions.')
    print("You should get some pop-ups asking you to enable settings in your privacy tab.")
    print("Once you enable the settings, quit and restart Terminal, then rerun metalayer init")
    print("Press ENTER to continue.")
    input()

    capture_enabled = cg.CGRequestScreenCaptureAccess()
    if not capture_enabled:
        print('Screen Capture not enabled for Terminal. If you did not get a pop-up, please enable manually\n'
              'in System Preferences > Security & Privacy > Privacy > Screen Recording')
        print('Press ENTER once you have enabled screen recording. Choose to restart "later".')
        input()

    listen_enabled = cg.CGRequestListenEventAccess()
    if not listen_enabled:
        print('Input Monitoring not enabled for Terminal. If you did not get a pop-up, please enable manually\n'
              'in System Preferences > Security & Privacy > Privacy > Input Monitoring')
        print('Press ENTER once you have enabled input monitoring. Choose to restart "later".')
        input()

    post_enabled = cg.CGRequestPostEventAccess()
    if not post_enabled:
        print('Accessibility not enabled for Terminal. If you did not get a pop-up, please enable manually\n'
              'in System Preferences > Security & Privacy > Privacy > Accessibility')
        print('Press ENTER once you have enabled accessibility. Choose to restart "later".')
        input()


    print("If you're using Google Chrome, you'll need to grant Terminal Automation access to \nGoogle Chrome.")
    print('Press ENTER to open Automation settings')
    print("Press ENTER once you have checked the Google Chrome box under Terminal.")
    url = "x-apple.systempreferences:com.apple.preference.security?Privacy_Automation"
    shared_workspace = NSWorkspace.sharedWorkspace()
    shared_workspace.openURL_(NSURL.URLWithString_(url))
    input()

    if not all([capture_enabled, listen_enabled, post_enabled]):
        print("Once you've enabled all permissions, quit and restart Terminal")
        return

    vault_dir = os.path.join(os.path.expanduser('~'), 'Knowledge-Repo')
    vault_dir = config.get('vault_dir', vault_dir)

    print('\nWelcome to the metalayer. Your knowledge repo will live in:\n')
    print(vault_dir)
    print("\nIf you'd like to change this, you can run the following command:")
    print('\nmetalayer set-vault-dir <path>\n')
    print("Now let's create some folders to filter what goes into your repo\n")

    for _ in range(5):
        print("Enter a topic you'd like to index in your knowledge repo:")
        print("ex. Linear Algebra, Biology, Music Theory\n")
        folder_name = input().strip()
        print("\nNow, create a 1-3 sentence description of what you want to put in this folder (type ENTER to complete):")
        print("ex. Everything I've learned about linear algebra, including the basics of matrix multiplication, eigenvectors, and eigenvalues\n")
        folder_description = input().strip()
        print()

        try:
            folder_path = os.path.join(vault_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            with open(os.path.join(folder_path, '_description.md'), 'w') as f:
                f.write(folder_description)
        except Exception as e:
            print('Error creating folder: ' + str(e))

        print('Create another folder? [y/N]')
        if input().strip().lower() != 'y':
            break
    print('Done creating folders! You can add more or modify their descriptions later in your knowledge repo. '
          'Any time you make a new folder remember to make a _description.md file so metalayer can decide what to put there.\n')
    print("You're all set! Now you can run the metalayer with:")
    print('\nmetalayer run\n')

    config.update({'vault_dir': vault_dir})
    with open(os.path.join(CONFIG_PATH), 'w') as f:
        json.dump(config, f, indent=4)


def run(args):
    buffer = Queue()
    backend = 'macos' if sys.platform == 'darwin' else 'easyocr'
    producer = CaptureProducer(args.capture_interval, buffer)
    consumer = CaptureConsumer(buffer, backend, wait_for_power=args.wait_for_power)

    # Soft-stop: finish OCR before exiting program
    def soft_stop():
        producer.stop()
        consumer.wait_for_power = False

    def wait_for_quit():
        while input() != 'q':
            pass
        soft_stop()

    stop_thread = Thread(target=wait_for_quit, daemon=True)

    producer.start()
    consumer.start()

    stop_thread.start()
    if args.t:
        timer = Timer(args.t, soft_stop)
        timer.start()

    producer.join()
    consumer.join()

    if args.t:
        timer.cancel()


if __name__ == '__main__':
    main()
