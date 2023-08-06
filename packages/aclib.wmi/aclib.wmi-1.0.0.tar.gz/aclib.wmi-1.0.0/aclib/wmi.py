import os
from comtypes.client import CoGetObject

class WMI(object):
    def __init__(self):
        self.__wmi = CoGetObject('winmgmts:')

    def instancesof(self, objecname:str):
        instances = []
        for instance in self.__wmi.InstancesOf(objecname):
            content = {}
            for prop in instance.Properties_:
                content[prop.Name] = prop.Value
            instances.append(content)
        return instances

    def get_harddisk_serial(self, drive_letter="C:"):
        for disk2partition in self.Win32_LogicalDiskToPartition_List():
            if disk2partition.get('Dependent','').split('"',1)[-1][:-1] != drive_letter: continue
            sysdiskindex = disk2partition.get('Antecedent','').split('"',1)[-1].split(',')[0][6:]
            for diskdrive in self.Win32_DiskDrive_List():
                if diskdrive.get('Index',-1) == int(sysdiskindex):
                    return diskdrive.get('SerialNumber', '')
            return ''

    def get_osharddisk_serial(self):
        return self.get_harddisk_serial(os.getenv('SystemDrive'))

    def Win32_LogicalDiskToPartition_List(self):
        return self.instancesof('Win32_LogicalDiskToPartition')

    def Win32_DiskDrive_List(self):
        return self.instancesof('Win32_DiskDrive')

    def Win32_Volume_List(self):
        return self.instancesof('Win32_Volume')

    def Win32_Process(self):
        return self.instancesof('Win32_Process')
