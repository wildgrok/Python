# import win32com.client as com
#
# def TotalSize(drive):
#     """ Return the TotalSize of a shared drive [GB]"""
#     try:
#         fso = com.Dispatch("Scripting.FileSystemObject")
#         drv = fso.GetDrive(drive)
#         return drv.TotalSize/2**30
#     except:
#         return 0
#
# def FreeSpace(drive):
#     """ Return the FreeSpace of a shared drive [GB]"""
#     try:
#         fso = com.Dispatch("Scripting.FileSystemObject")
#         drv = fso.GetDrive(drive)
#         return drv.FreeSpace/2**30
#     except:
#         return 0
#
# workstations = ['CCLTSTECOSQLDB1', 'CCLUATECOSQLDB1']
# print ('Hard drive sizes:')
# for compName in workstations:
#     drive = '\\\\' + compName + '\\c$'
#     print('*************************************************\n')
#     print(compName)
#     print('TotalSize of %s = %f GB' % (drive, TotalSize(drive)))
#     print('FreeSpace on %s = %f GB' % (drive, FreeSpace(drive)))
#     print('*************************************************\n')

# import subprocess
# import string
#
# #define alphabet
# alphabet = []
# for i in string.ascii_uppercase:
#     alphabet.append(i + ':')
#
# #get letters that are mounted somewhere
# mounted_letters = subprocess.Popen("wmic logicaldisk get name", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# #erase mounted letters from alphabet in nested loop
# for line in mounted_letters.stdout.readlines():
#     # if "Name" in line:
#     #     continue
#     for letter in alphabet:
#         if letter in line:
#             print ('Deleting letter %s from free alphabet %s' % letter)
#             alphabet.pop(alphabet.index(letter))
#
# print(alphabet)
