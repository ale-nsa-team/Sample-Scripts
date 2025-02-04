import paramiko
import os
import stat
import argparse
import textwrap
import time
import keyring

class SFTPdtClient(paramiko.SFTPClient):
    def __init__(self, *args, **kwargs):
        super(SFTPdtClient, self).__init__(*args, **kwargs)
        self.dir_count = 0
        self.file_count = 0
        self.fail_count = 0
    def download_data(self, remote_dir, local_path):
        for item_attr in self.listdir_attr(remote_dir):
             if stat.S_ISDIR(item_attr.st_mode):
                 target_path=os.path.join(local_path,str(item_attr.filename))
                 try:
                     os.mkdir(target_path)
                     self.dir_count +=1
                 except OSError:
                     pass
                 new_remote_dir = os.path.join(remote_dir,str(item_attr.filename))
                 self.download_data(new_remote_dir,target_path)
             else:
                 try:
                     sftp_source = os.path.join(remote_dir,item_attr.filename)
                     sftp_target = os.path.join(local_path,item_attr.filename)
                     self.get(sftp_source,sftp_target)
                     self.file_count +=1
                     log('[Success - File Copy] ' + sftp_source,"l")
                     if (verbose_flag):
                         log('[Success - File Copy] ' + sftp_source,"p")
                 except:
                     log('[Failure - File Copy] ' + sftp_source,"lp")
                     self.fail_count +=1
                     pass

def log(log_content,action):
    log_file = "sftpdt.log"
    if "p" in action:
        print(log_content)
    if "l" in action and nolog_flag == False:
        log_file = open(log_file,"a")
        log_file.write(log_content + "\n")
        log_file.close()
    if "c" in action and nolog_flag == False:
        log_file = open(log_file,"w")
        log_file.write(log_content)
        log_file.close()
def calc_exec_time(start_time,end_time):
    execution_elapsed_time = end_time - start_time
    hours, rem = divmod(execution_elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    exec_duration  = ("{:0>2}:{:0>2}:{:0>2}".format(int(hours),int(minutes),int(seconds)))
    return exec_duration
def start_download(ip,port,remote_dir,local_path):
    start_text = "###########################################################\n"
    start_text +=" ________________ SFTP Download Tool ______________________\n"
    start_text +=" ___________________ Ver 2.0 Dev __________________________\n"
    start_text +="###########################################################\n"
    start_text +=""
    start_text +="Connecting to remote server @ " + ip + "..."
    log("","c")
    log(start_text,"pl")
    try:
        username='cliadmin'
        password=keyring.get_password('cliadmin','xkcd')
        transport = paramiko.Transport((ip, port))
        transport.connect(username=username, password=password)
        sftpdt = SFTPdtClient.from_transport(transport)
        target_path=os.path.join(local_path,remote_dir)
        try:
            os.mkdir(target_path)
        except OSError:
            pass
        log("Connected to remote server.Downloading...","pl")
        start_time = time.time()
        sftpdt.download_data(remote_dir,target_path)
        end_time = time.time()
        elapsed_time = calc_exec_time(start_time,end_time)
        log("","lp")
        log(" " + str(sftpdt.dir_count) + ' Directories Created | ' + str(sftpdt.file_count) + ' files copied | ' + str(sftpdt.fail_count) + ' files failed |' + " Execution time: " + elapsed_time,"pl")
        log("","lp")
        sftpdt.close()
    except:
        print("Error connecting to remote server ! Please Check remote server IP and credentials.")
def main():
    global start_time
    global end_time
    global nolog_flag
    global verbose_flag
    parser = argparse.ArgumentParser(
        prog='SFTPdt',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
           SFTP Download Tool V2.0
           Developed by Kaveh Majidi @ ALE
           ---------------------------------------------------
           This tool can be used to download a directory from
           a remote server to a local machine using SFTP.
           The credentials to login to target machine (OV) need to be set through keyring before running the script.
           Please see example.

           Example : python3 sftpdt.py --ip=10.10.10.10 --remote_dir="backups" --local_path="/home/user/localbackup" -v

           '''))
    parser.add_argument('--ip', metavar='IP ADDRESS',required=True,
                        help='IP address of the remote server')
    parser.add_argument('--remote_dir',metavar='DIR',required=True,
                        help='directory on the remote server to be downloaded, Ex. "backups"')
    parser.add_argument('--local_path',metavar='PATH',required=True,
                        help='local path as the destination for download, Ex. "/home/user/backup" this directory needs to be created on local system and  the user running the script should have write permission on this directory' )
    parser.add_argument('--port',default=22,
                        help='SFTP port number, default is 22')
    parser.add_argument('-nolog',action="store_true",
                        help='disables logging , by default logging is enabled')
    parser.add_argument('-v',action="store_true",
                        help='enables verbose mode')
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    args = parser.parse_args()
    nolog_flag = args.nolog
    verbose_flag=args.v
    start_download(args.ip,args.port,args.remote_dir,args.local_path)
main()
