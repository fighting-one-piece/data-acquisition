# -*- coding:utf-8 -*-

import os  
import paramiko    
  
host = '192.168.0.114'  
port = 22  
username = 'ym'  
password = 'youmeng@123'  
  
def sshConnect(host, username, password):  
    ssh = paramiko.SSHClient()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    #private_key_file = os.path.expanduser('C:/Program Files/VMware/VMware Share/id_rsa')  
    #mykey = paramiko.RSAKey.from_private_key_file(private_key_file)  
    ssh.connect(host, port, username, password, timeout = 300)  
    stdin, stdout, stderr = ssh.exec_command('ls .')  
    print stdout.read()  
    ssh.close()  
    
def copyWindowsToLinux(host, username, password, src, dest):
    ssh = paramiko.SSHClient()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    ssh.connect(host, port, username, password, timeout = 300)  
    sftpd = ssh.open_sftp()
    sftpd.put(src, dest)
    ssh.close()  

def copyLinuxToWindows(host, username, password, src, dest):
    ssh = paramiko.SSHClient()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    ssh.connect(host, port, username, password, timeout = 300)  
    sftpd = ssh.open_sftp()
    sftpd.get(src, dest)
    ssh.close()  

if __name__ == '__main__' :
    package_command = 'F: & \
        cd F:/workspace/workspace_temp_git_0/CisionDataProject/esentity & \
        mvn clean -X -U package -Dmaven.test.skip=true &'
    os.system(package_command); 
    src = 'F:/workspace/workspace_temp_git_0/CisionDataProject/esentity/target/esentity-0.0.1-SNAPSHOT.jar'
    dest = '/home/ym/DataX/datax/plugin/writer/eswriter/esentity-0.0.1-SNAPSHOT.jar'
    copyWindowsToLinux('192.168.0.114', 'ym', 'youmeng@123', src, dest)
    copyWindowsToLinux('192.168.0.108', 'ym', 'youmeng@#123', src, dest)
    print 'copy local jar package to linux finish !!!'
    os.system('git status')
    os.system('git add .')
    os.system('git commit -m \' financial logistics model modify commit\'')
    os.system('git push origin master')
    
    


