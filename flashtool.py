import os,re
from multiprocessing import Pool
import time, random
"""
nexus 5 python自动化刷机脚本
1.fastboot批量线刷
2.adb 传输xpods文件
3.批量执行自定义shell脚本
"""


#执行shell命令
def execCmd(cmd):
	r = os.popen(cmd)
	text = r.read()
	r.close()
	return text

#获取fastboot设备列表
def getFastbootDecicesList():
	cmd = "fastboot devices"
	result = execCmd(cmd)
	pat1 = "(.*)\tfastboot"
	fastboot_id = re.findall(pat1,result)
	print ("fastbootID_list= %s"%(fastboot_id))
	return fastboot_id

#获取adb设备列表
def getADBDevicesList():
        cmd = "adb devices"
        result = execCmd(cmd)
        pat = "(.*)\tdevice"
        adb_id = re.findall(pat,result)
        print ("adbID_list= %s"%(adb_id))
        return adb_id

#执行fastboot批量刷机
def startFastbootFlash(fastboot_id):
        flash_boot(fastboot_id)
        flash_twrp(fastboot_id)
        flash_cache(fastboot_id)
        flash_system(fastboot_id)
        flash_userdata(fastboot_id)
        fastboot_reboot(fastboot_id)
        return
#执行adb批量发送xpods文件
def adbSendXpods(adb_id):
        send_xpods(adb_id)
        adb_rebootToRecovery(adb_id)
        return

#fastboot重启手机
def fastboot_reboot(fastboot_id):
        cmd = "fastboot -s "+fastboot_id+" reboot"
        result = execCmd(cmd)
        return result

#1.刷入fastboot-flash-boot.img  
def flash_boot(fastboot_id):

        cmd = "fastboot -s "+fastboot_id+" flash boot imgs/boot.img"
        print(cmd)
        result = execCmd(cmd)
        return result
#2.刷入twrp.img
def flash_twrp(fastboot_id):
        cmd = "fastboot -s "+fastboot_id+" flash recovery imgs/twrp.img"
        result = execCmd(cmd)
        return result
#3.刷入cache.img
def flash_cache(fastboot_id):
        cmd = "fastboot -s "+fastboot_id+" flash cache imgs/cache.img"           
        result = execCmd(cmd)
        return result

#4.刷入system.img
def flash_system(fastboot_id):
        cmd = "fastboot -s "+fastboot_id+" flash system imgs/system.img"           
        result = execCmd(cmd)
        return result

#5.刷入userdata.img
def flash_userdata(fastboot_id):
        cmd = "fastboot -s "+fastboot_id+" flash userdata imgs/userdata.img"           
        result = execCmd(cmd)
        return result

#发送xpods文件
def send_xpods(adb_id):
        cmd = "adb -s "+adb_id+" push imgs/xposed-v87-sdk23-arm.zip /sdcard/"
        print(cmd)
        result = execCmd(cmd)
        return result

#adb重启手机到recovery
def adb_rebootToRecovery(adb_id):
        cmd = "adb -s "+adb_id+" reboot recovery"
        result = execCmd(cmd)
        return result


def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    startFastbootFlash(name)
    end = time.time()

    print('Task %s runs %0.2f seconds.' % (name, (end - start)))
#主功能1.批量执行fastboot线刷
def startAllFastbootFlash():
		fastboot_array = getFastbootDecicesList()
		print(fastboot_array)
		print('Parent process %s.' % os.getpid())
		p = Pool(60)
		for fastboot_id in fastboot_array:
			p.apply_async(long_time_task, args=(fastboot_id,))
		print('Waiting for all subprocesses done...')
		p.close()
		p.join()
		print('All subprocesses done.')
		
#主功能2.批量adb发送xpods数据
def sendAllXpods():
		adb_array = getADBDevicesList()
		for adb_id in adb_array:
			adbSendXpods(adb_id)



while True :
        code = input("欢迎使用自动化刷机工具:\n输入以下指令执行功能\n1.批量执行fastboot线刷\n2.批量adb发送xpods数据\n3.批量执行自定义指令\n")
        if code == "1":
                print ("正在执行批量线刷......")
                startAllFastbootFlash()
        elif code == "1 list":
                print ("正在查看fastboot设备列表......")
    	
        elif code == "2":
                print ("正在批量发送xpods文件......")
                sendAllXpods()
        elif code == "2 list":
                print ("正在查看adb设备列表......")
    		    #getADBDevicesList()
        elif code == "3":
                print ("输入需要执行的自定义命令：\n")
                ##暂未开发
       















