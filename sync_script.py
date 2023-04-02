import argparse
import pathlib
import os
import time
import shutil

# Please implement a program that synchronizes two folders: source and replica. The
# program should maintain a full, identical copy of source folder at replica folder.
# Solve the test task by writing a program in Python

# sync_script.py -s source_folder -r replica_folder -i sync_interval log_file_path
# sync-script --source_folder C:\users\UserulTau\dir
def parseArgs():
    print("...Waiting to fetch options and flags...")
    Parser = argparse.ArgumentParser(
        description=""" Utillity designed to  synchronize two folders: source and replica. The
                        program should maintain a full, identical copy of source folder at replica folder.
                        """)

    Parser.add_argument(
        "logfile_path",
        help=" Name of the log file where all the file creation/copying/removal operations will be logged. ",
        type=pathlib.Path

    )

    Parser.add_argument(
        "-s", "--source_folder",
        metavar="PATH_OF_SOURCE_FOLDER",
        help=""" Source folder from which the copy will be created. """,
        type=pathlib.Path,
        default=None
    )

    Parser.add_argument(
        "-r", "--replica_folder",
        metavar="PATH_OF_REPLICA_FOLDER",
        help=""" Replica folder which will be kept in sync with the source folder, at a specified interval. """,
        type=pathlib.Path,
        default=None
    )

    Parser.add_argument(
        "-i", "--sync_interval",
        metavar="TIME_IN_MIN",
        help=""" The interval at which the sync will be done. """,
        type=float,
        default=None
    )

    args = Parser.parse_args()
    print("...Options and flags were parsed...")
    return args
def readStateOfDir(root_path):
    root_path_obj = pathlib.Path(root_path)
    files_in_source_folder = root_path_obj.rglob("*")

    dir_state = [ F"{item} {'dir' if item.is_dir() else 'file'} {os.stat(os.path.abspath(item)).st_size}" for item in files_in_source_folder ]
    return dir_state

def remove(root_path):
    # Stergem elementele din folderul destinatie care apar in lista elements_in_first_state_only
    deleteFile = root_path
    os.remove(deleteFile)

def copy(root_path_source, root_path_destionation, file_name):
    source = root_path_source + file_name
    destination = root_path_destionation + file_name
    if os.path.isfile(source):
        shutil.copy(source, destination)


if __name__ == '__main__':
    command_line_args = parseArgs()

    sync_interval = command_line_args.sync_interval * 60
    source_folder = command_line_args.source_folder
    destination_folder = command_line_args.replica_folder

    print(f'SOURCE Folder is: {source_folder}')
    print(f'REPLICA Folder is: {destination_folder}')
    print(f'Synchronization interval is: {sync_interval} seconds')
    print(f'Logfile path is: {command_line_args.logfile_path}')

    while True:
        first_state = readStateOfDir(source_folder)
        print(first_state)

        time.sleep(sync_interval)

        second_state = readStateOfDir(source_folder)
        elements_in_first_state_only = list(set(first_state)-set(second_state))
        elements_in_second_state_only = list(set(second_state)-set(first_state))

        # Ne intereseaza elementele care sunt in a doua stare daca, s a modificat un fisier
        # sau daca a aparut un fisier/director in sursa, care urmeaza sa fie
        # suprascris / creat(copiat din sursa) in destinatie
        # Ne intereseaza elementele care sunt in prima stare daca, s a sters un fisier / director din sursa
        # care urmeaza sa fie sters si din destinatie

        print(second_state)

        print(elements_in_first_state_only)
        print(elements_in_second_state_only)
        for item in elements_in_first_state_only:
            destination_folder.remove(item)
        for item in elements_in_second_state_only:
            copy(source_folder, destination_folder, elements_in_second_state_only)
