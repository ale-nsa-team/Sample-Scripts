import os
import fnmatch
import re
import zipfile
from zipfile import ZipFile
import argparse
import textwrap
import time
import shutil

def unzip_files(zipfile_name):
    unzip_directory=zipfile_name.replace(".zip","")
    with ZipFile(zipfile_name, 'r') as zip:
        zip.extractall(unzip_directory)

def zip_files(zipfile_name):
    zip_directory=zipfile_name.replace(".zip","")
    new_zipfile_name=zip_directory + "_cleaned.zip"
    file_paths = []
    for root, directories, files in os.walk(zip_directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    with ZipFile(new_zipfile_name,'w') as zip:
        for file in file_paths:
            zip.write(file)
    return(new_zipfile_name)

def find_replace_keys(zipfile_name):
    filePattern="*.log"
    search_items=["key","sa-encryption","sa-authentication","password","community-map","community map","community-string"]
    directory=zipfile_name.replace(".zip","")
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            if (verbose_flag):
                print("Checking--> " + filepath)
            with open(filepath) as target_file:
                target_file_lines = target_file.readlines()
                found_key_list=[]
                for line in target_file_lines:
                    for search_item in search_items:
                        item_start_location=line.find(search_item)
                        line_end_location=line.find("\n")
                        linkagg_location=line.find("linkagg")
                        lacp_location=line.find("lacp")
                        ntp_location=line.find("ntp")
                        if(item_start_location >  -1 and linkagg_location == -1 and ntp_location ==-1 and lacp_location == -1):
                            found_key=(line[item_start_location+len(search_item)+1:line_end_location])
                            if (found_key):
                                found_key_list.append(found_key)
                #print(found_key_list)
            with open(filepath) as target_file:
                 file_content = target_file.read()
            for the_key in found_key_list:
                file_content = file_content.replace(the_key, "XXXX")
            with open(filepath, "w") as target_file:
                target_file.write(file_content)

def calc_exec_time(start_time,end_time):
    execution_elapsed_time = end_time - start_time
    hours, rem = divmod(execution_elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    exec_duration  = ("{:0>2}:{:0>2}:{:0>2}".format(int(hours),int(minutes),int(seconds)))
    return exec_duration

def start_cleanup(zipfile_name):
    start_time = time.time()
    start_text = "###########################################################\n"
    start_text +=" _____ AOS Configuration Log File Cleaner Tool  ____________\n"
    start_text +=" ___________________ Ver 1.0 Dev __________________________\n"
    start_text +="###########################################################\n"
    start_text +=""
    print(start_text)
    print("")
    print("Unpacking " + zipfile_name + "...")
    print("")
    unzip_files(zipfile_name)
    print("Unpacking done.Cleaning configuration files... ")
    print("")
    find_replace_keys(zipfile_name)
    print("")
    print("Zipping cleaned files...")
    print("")
    new_zipfile_name=zip_files(zipfile_name)
    temp_dir=zipfile_name.replace(".zip","")
    shutil.rmtree (temp_dir)
    print("All file are cleaned and zipped in a new file: " + new_zipfile_name)
    print("")
    end_time = time.time()
    elapsed_time = calc_exec_time(start_time,end_time)
    print("Operation completed. Total execution time:" + elapsed_time)
    print("")

def main():
    global start_time
    global end_time
    global verbose_flag
    parser = argparse.ArgumentParser(
        prog='Confcleaner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
           Confcleaner V1.0
           Developed by Kaveh Majidi @ ALE
           ---------------------------------------------------
           This tool can be used to clean up AOS configuration files from hashed keys. The
           Configuration log files should be provided as a zip package. Configuration log files
           should have .log extention.

           Example : python3 confcleaner.py --zipfile=myconfigs.zip -v

           '''))
    parser.add_argument('--zipfile',required=True,
                        help='Name of the Zip package containing configuration files')
    parser.add_argument('-v',action="store_true",
                        help='enables verbose mode')
    parser.add_argument('--version', action='version', version='%(prog)s V1.0')
    args = parser.parse_args()
    verbose_flag=args.v
    zipfile_name=args.zipfile
    if(zipfile.is_zipfile(zipfile_name)):
        start_cleanup(zipfile_name)
    else:
        print("The provided file name is not a zip package. Please provide a Zip package file.")
main()
