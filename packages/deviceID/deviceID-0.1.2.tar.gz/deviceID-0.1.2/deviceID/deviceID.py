from sys import platform
from subprocess import Popen, PIPE
import json
import xxhash

class Memory_Device:
  size = ''
  factor = ''
  type = ''
  detail = ''
  manufacturer = ''
  serial = ''
  pn = ''
  locator = ''

  def __init__(self):
    print()
  
  def setSize(self, size):
    self.size = size

  def setFactor(self, factor):
     self.factor = factor

  def setType(self, type):
    self.type = type

  def setDetail(self, detail):
    self.detail = detail

  def setManufacturer(self, manufacturer):
    self.manufacturer = manufacturer

  def setSerial(self, serial):
    self.serial = serial

  def setPN(self, pn):
    self.pn = pn

  def setLocator(self, locator):
    self.locator = locator

  def toJSON(self):
      return json.dumps(self, default=lambda o: o.__dict__, 
         sort_keys=True, indent=4)
def id():
  if platform == "linux" or platform == "linux2":
    disks = []
    motherboard_name = ''
    motherboard_manufacturer = ''
    motherboard_id = ''
    processor_id = ''
    processor_manufacturer = ''
    processor_family = ''
    processor_version = ''
    processor_serial = ''
    processor_socket = ''
    processor_cores = ''
    processor_threads = ''
    max_memory = ''
    ecc = ''
    memory_num = ''
    memory_devices = []
    with Popen('lsblk --nodeps -o serial,size,type'.split(' '), stdout=PIPE, universal_newlines=True) as process:
      for line in process.stdout:
        if line[-5:].replace('\n', '') == "disk":
          disks.append(line[:-5].rstrip())
    with Popen('sudo dmidecode --type baseboard'.split(' '), stdout=PIPE, universal_newlines=True) as process:
      for line in process.stdout:
        data = line.replace('\n', '').replace(' ', '')
        if 'SerialNumber:' in data:
          motherboard_id = data.split(':')[1]
        elif 'ProductName:' in data:
          motherboard_name = data.split(':')[1]
        elif 'Manufacturer:' in data:
         motherboard_manufacturer = data.split(':')[1]
    with Popen('sudo dmidecode --type processor'.split(' '), stdout=PIPE, universal_newlines=True) as process:
      for line in process.stdout:
        data = line.replace('\n', '').replace(' ', '')
        if 'SerialNumber:' in data:
          processor_serial = data.split(':')[1]
        elif 'ID:' in data:
          processor_id = data.split(':')[1]
        elif 'Manufacturer:' in data:
         processor_manufacturer = data.split(':')[1]
        elif 'Family:' in data:
         processor_family = data.split(':')[1]
        elif 'Version:' in data:
         processor_version = data.split(':')[1]
        elif 'Socket:' in data:
         processor_socket = data.split(':')[1]
        elif 'CoreCount:' in data:
         processor_cores = data.split(':')[1]
        elif 'ThreadCount:' in data:
         processor_threads = data.split(':')[1]
    with Popen('sudo dmidecode --type memory'.split(' '), stdout=PIPE, universal_newlines=True) as process:
      isSystemMemory = False
      isDone = False
      tempDevice = Memory_Device()
      for line in process.stdout:
        data = line.replace('\n', '').replace(' ', '')
        if isDone:
          if 'Size:' in data:
            tempDevice.setSize(data.split('Size:')[1])
          if 'FormFactor:' in data:
            tempDevice.setFactor(data.split('FormFactor:')[1])
          if 'Locator:' in data:
            tempDevice.setLocator(data.split('Locator:')[1])
          if 'Type:' in data:
            tempDevice.setType(data.split('Type:')[1])
          if 'TypeDetail:' in data:
            tempDevice.setDetail(data.split('TypeDetail')[1])
          if 'Manufacturer:' in data:
            tempDevice.setManufacturer(data.split('Manufacturer')[1])
          if 'SerialNumber:' in data:
            tempDevice.setSerial(data.split('SerialNumber:')[1])
          if 'PartNumber:' in data:
            tempDevice.setPN(data.split('PartNumber')[1])
            memory_devices.append(tempDevice.toJSON())
            tempDevice = Memory_Device()
        else: 
          if isSystemMemory:
            if 'ErrorCorrectionType:' in data:
              ecc = data.split('ErrorCorrectionType:')[1]
            elif 'MaximumCapacity:' in data:
              max_memory = data.split('MaximumCapacity')[1]
            elif 'NumberOfDevices:' in data:
              memory_num = data.split('NumberOfDevices:')[1]
              isDone = True
          else:
            if 'Location:' in data:
              if ('SystemBoard' in data.split('Location:')[1]):
                isSystemMemory = True
    return xxhash.xxh64(';'.join(disks) + ';'.join(memory_devices) + ';' + ecc + ',' + max_memory + ',' + memory_num + ';' + processor_serial + ';' + processor_id + ';' + processor_manufacturer + ';' + processor_family + ';' + processor_version + ';' + processor_socket + ';' + processor_cores + ';' + processor_threads + ';' + motherboard_id + ';' + motherboard_name + ';' + motherboard_manufacturer).hexdigest()
  elif platform == "darwin":
    print('os x')
  elif platform == "win32":
  import wmi
  c = wmi.WMI()
  hddSerialNumber = c.Win32_PhysicalMedia()[0].wmi_property('SerialNumber').value.strip()
  print(hddSerialNumber)
