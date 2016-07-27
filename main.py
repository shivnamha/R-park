#!/usr/bin/python

import paramiko
import config as cfg
from os import path, mkdir
from scp import SCPClient
from shutil import copyfile, move

def copy_file(local_file_path, dest_path, host=cfg.HOST_CONF['HOST'], port=cfg.HOST_CONF['PORT'], user=cfg.HOST_CONF['USER'], password=cfg.HOST_CONF['PASSWORD'], mode = 'PUT'):

        transport = None
        if not path.exists(local_file_path):
                if mode is 'GET':
                        mkdir(local_file_path)
                else:
		        print "Local file path doesnt exist %s" %(local_file_path) 
	
        paramiko.util.log_to_file(cfg.PARAMIKO_LOG)
        transport = paramiko.Transport((host, port))
        try:
               transport.connect(username=user, password=password)
               transport.get_exception()
               scp = SCPClient(transport)
        except:
               print "Error while connecting to host %s:%s" %(host, port)
        #scp.put('test_eth.sh', 'test_eth_1.sh')
        #scp.get('test_eth_1.sh')
        if mode is 'PUT':
                #print "copying file from %s to %s on host %s " %(local_file_path, dest_path, host)
                scp.put(local_file_path, dest_path)
        else:
                #print scp.get(dest_path,local_file_path, recursive=True)
                scp.get(dest_path, recursive=True)
                #print scp.get(dest_path, local_path="path_to_directory where store this directory", recursive= True)
                
        scp.close()

def execute_cmd(command, host=cfg.HOST_CONF['HOST'], port=cfg.HOST_CONF['PORT'], user=cfg.HOST_CONF['USER'], password=cfg.HOST_CONF['PASSWORD']):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, port=port, username=user, password=password)
        #ssh.exec_command("cd " + prefix)
        (stdin, stdout, stderr) = ssh.exec_command(command)
        #for line in stdout.readlines():
        #       print line
	out = stdout.readlines()
        if len(out):
                return out
        else:
                return stderr.readlines()
        ssh.close()

def prepare_path(prefix, command):
        return path.join(prefix, cfg.SCRIPT_CONF[command])

def cmd_args(command, dev):
        if cfg.DEV_CONF.has_key(dev) and cfg.DEV_CONF.has_key(command):
                print "%s device with %s test is not valid" %(dev, command)
                return "" 
        return cfg.DEV_CONF[dev][command]

def update_conf(auto_tests=[], int_tests=[]):
        fa = open("automated.conf", 'w')
        fi = open("interactive.conf", 'w')
        fa.write('#run_test "Test Name" "Test Command" "Test Parameters"\n')
        fi.write('#run_test "Test Name" "Test Command" "Test Parameters" "Pre-test Prompt" "Post-test Prompt"\n')
        for (name, test, dev) in auto_tests:
                cmd = prepare_path(cfg.DEFAULT_PATH_PREFIX, test)      
                fa.write('run_test "%s" %s "%s"\n' %(test, cmd, cmd_args(test, dev))) 

        for name, test, dev in int_tests:
                cmd = prepare_path(cfg.DEFAULT_PATH_PREFIX, test)      
                fi.write('run_test "%s" %s "%s"\n' %(test, cmd, cmd_args(test, dev))) 
        fa.close()
        fi.close()

def parse_results(result):
        test_result = {}
        if len(result) > 2:
                res = str(result[2]).rstrip()
                
        if res:
                path = cfg.BOARD_LOG_DIR_PATH + res
                copy_file(cfg.LOCAL_LOG_DIR_PATH, path, mode="GET")
                move(res, cfg.LOCAL_LOG_DIR_PATH)

        for i in range(14, len(result)):
                if result[i] and str(result[i]).split(':') and  len(str(result[i]).split(':')) > 1:
                        if str(result[i]).split(':')[1].find('SUCCESS') > -1:
                                test_result[str(result[i]).split(':')[0].strip()] = 'SUCCESS'
                        else:
                                test_result[str(result[i]).split(':')[0].strip()] = 'FAILED'
        print test_result        

def execute_tests(host=cfg.HOST_CONF['HOST'], port=cfg.HOST_CONF['PORT'], user=cfg.HOST_CONF['USER'], password=cfg.HOST_CONF['PASSWORD']):
        #copy automated and interactive conf on destination host
        test = 'TEST_SCRIPT'
        copy_file("automated.conf", cfg.DEFAULT_PATH_PREFIX, host, port, user, password)
        copy_file("interactive.conf", cfg.DEFAULT_PATH_PREFIX, host, port, user, password)

        cmd = prepare_path(cfg.DEFAULT_PATH_PREFIX, test)
        cmd = "cd " + cfg.DEFAULT_PATH_PREFIX + ";" + cmd
	#print host, port, user , password
        parse_results( execute_cmd(cmd, host, port, user, password) )
