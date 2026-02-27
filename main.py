from core.setup import setup, set_bot_token, set_encryption_key, set_guild_id
from core.partition import partition_file, download_file_by_path
from core.tui import start_dashboard, show_stats
from core.db_manager import SQliteDB
from core.setup import BASE_DIR
from shutil import rmtree
import argparse
import os

rmtree(BASE_DIR/"files", True)

path_filters = [
    '\\__pycache__', 
    '\\.git', 
    '\\$RECYCLE.BIN'
]

def upload_file(path):

    # check if path is file or directory first
    absolute_path = os.path.abspath(path)
   
    if os.path.isdir(absolute_path):

        print("Directory provided, processing files inside the directory into it's own folder.")

        base: str = ""

        for root, _, files in os.walk(absolute_path):
            
            base += os.path.basename(root) + "/"
            
            for file in files:

                file_path:str = os.path.join(root, file).lower()

                real_path:str = os.path.realpath(file_path).lower()

                NOTIGNORED = (not any(f in root for f in path_filters))
                
                RESOLUTE = (file_path == real_path)
                
                # If the path does not contain any of the ignored strings
                if NOTIGNORED and RESOLUTE:

                    print(f'Uploading: {file_path}')

                    partition_file(file_path, base.rstrip("/"))

                else:

                    print(f'Skipped: {NOTIGNORED=} | {RESOLUTE=} | {file_path}')

    else:
        
        print(f'Uploading: {absolute_path}')
        
        partition_file(absolute_path)

def download_file(path):
    print(f"Downloading file: {path}")
    download_file_by_path(path)


def run_setup(token=None, encryption_key=None, guild_id=None):
    if token:
        set_bot_token(token)
        print("Bot token updated.")

    if encryption_key:
        set_encryption_key()
        print("Encryption passphrase updated.")

    if guild_id:
        set_guild_id(guild_id)
        print("Guild ID updated.")


if __name__ == "__main__":
    # inital setup
    database = SQliteDB()
    setup()

    parser = argparse.ArgumentParser(
        prog="syncord",
        formatter_class=argparse.RawTextHelpFormatter,
        description="""\
Syncord: Just another way of using our lovely discord!

Initial setup (only once):
syncord setup --token YOUR_DISCORD_BOT_TOKEN   - enter and save Discord bot token
syncord setup --crypto-passphrase PASS         - configure encryption passphrase (default: 'syncord1234')
""",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    setup_parser = subparsers.add_parser(
        "setup",
        help="Initial setup and change config like token/passphrase",
        description="Set or change the discord bot token and other \
config. Please make sure to have a discord bot with the \
guild access already.",
    )
    setup_parser.add_argument("--token", "-t", help="Discord bot token \
to use for uploading/downloading files.")
    setup_parser.add_argument("--encryption-key", "-e", help="Rotate \
encryption key. This is used for file encryption/decryption to \
prevent anyone from assembling your data from discord itself.\
Make sure to remember this key as without this key \
your data is lost!", action="store_true")
    setup_parser.add_argument("--guild-id", "-g", help="Set guild ID. \
        This would be the guild where all files are uploaded.")
    setup_parser.set_defaults(func="setup")

    upload_parser = subparsers.add_parser(
        "upload",
        help="Upload a file to configured discord channel",
        usage="syncord upload <file_path>",
        description="Upload a file to the configured discord channel.",
    )
    upload_parser.add_argument("file_path", help="Path to the file to upload")
    upload_parser.set_defaults(func="upload")

    download_parser = subparsers.add_parser(
        "download",
        help="Download a file from discord",
        usage="syncord download <syncord_file_path>",
        description="Download a file from discord via syncord.",
    )
    download_parser.add_argument(
        "file_path", help="Path/identifier of file to download"
    )
    download_parser.set_defaults(func="download")

    dashboard_parser = subparsers.add_parser(
        "dashboard",
        help="Open the TUI dashboard",
        description="Start the terminal user interface dashboard.",
        usage="syncord dashboard",
    )
    dashboard_parser.set_defaults(func="dashboard")

    stats_parser = subparsers.add_parser(
        "stats",
        help="Show syncord usage stats",
        description="Display usage statistics for syncord.",
        usage="syncord stats",
    )
    stats_parser.set_defaults(func="stats")

    args = parser.parse_args()

    if args.command == "setup":
        if args.token is None and args.encryption_key is None and args.guild_id is None:
            setup_parser.print_help()

        run_setup(token=args.token, encryption_key=args.encryption_key, guild_id=args.guild_id)

    if args.command == "upload":
        upload_file(args.file_path)

    if args.command == "download":
        download_file(args.file_path)

    if args.command == "dashboard":
        start_dashboard()

    if args.command == "stats":
        show_stats()
