# Observes what processes are doing (Windows only)

This code provides a structured and efficient approach to scan processes, gather registry data, filter files, and perform file copying. 
It simplifies the analysis of running processes and allows 
users to extract valuable information for system monitoring, security assessments, or forensic investigations.

## pip install whatdiditdo


#### Tested against Windows 10 / Python 3.10 / Anaconda 3

The scan_processes function can be useful for system administrators, security analysts, or anyone who needs to perform a comprehensive scan and analysis of running processes on a Windows system. Here are some advantages of using this code:

Process scanning: The function allows users to scan processes based on partial process names or regular expressions, providing flexibility in defining the target processes for analysis.

Registry filtering: Users can specify custom regular expression filters for registry keys, enabling them to include or exclude specific keys based on their patterns. This feature allows for fine-grained control over the registry data to be collected.

File filtering: The function supports filtering files based on forbidden folders and a string pattern. Users can exclude specific folders or files based on their paths, allowing them to focus on relevant files and ignore unnecessary ones.

File copying: The function facilitates copying files from the scanned processes to a specified destination folder. This can be valuable for further analysis or investigation of the files associated with the processes.

Data aggregation: The function collects registry data and file information from multiple processes and aggregates them into pandas DataFrames. This consolidated data can be easily analyzed, processed, or exported for further investigation.

Exception handling: The code includes exception handling to ensure that the scanning process continues even if exceptions are encountered. It provides the ability to gracefully handle errors and continue scanning other processes.



```python
# Example: Monitoring BlueStacks Instances (Press CTRL+C when you want to stop the observation)
# This code example showcases how to monitor BlueStacks instances by scanning specific folders for executable files,
# filtering registry keys, and detecting file changes. It provides flexibility in including or excluding processes
# based on their process IDs and enables customization of the scanning process through various parameters.
# The resulting data, including registry information and copied files, can be further analyzed or utilized
# for system monitoring, security assessments, or forensic investigations.

import os
import re

from whatdiditdo import scan_processes, get_all_exe_files_from_folders

# I wanted to find out what happens when I create a new BlueStacks instance, so
# I used this code:

# Folders to scan for BlueStacks executable files
folders = [
    r"C:\ProgramData\BlueStacks_nxt",
    r"C:\ProgramData\BlueStacks",
    r"C:\Program Files\BlueStacks_nxt",
    r"C:\Program Files\BlueStacks",
    r"C:\Users\hansc\AppData\Local\Temp\7zSC3B9E9A3",
]

# Retrieve all executable files within the specified folders
allexefiles = get_all_exe_files_from_folders(
    folders
)  # '(?:(?:HD-DiskFormatCheck.exe)|(?:HD-MultiInstanceManager.exe)|(?:BstkVMMgr.exe)|(?:HD-DiskCompaction.exe)|(?:HD-Player.exe)|(?:HD-CheckCpu.exe)|(?:HD-Hvutl.exe)|(?:HD-Agent.exe)|(?:HD-XapkHandler.exe)|(?:Bluestacks.exe)|(?:HD-DataManager.exe)|(?:HD-GLCheck.exe)|(?:HD-ComRegistrar.exe)|(?:HD-Aapt.exe)|(?:HD-GuestCommandRunner.exe)|(?:HD-Adb.exe)|(?:HD-LogCollector.exe)|(?:HD-ConfigHttpProxy.exe)|(?:HD-ForceGPU.exe)|(?:HD-SslCertificateTool.exe)|(?:HD-QuitMultiInstall.exe)|(?:BlueStacksAppplayerWeb.exe)|(?:BstkSVC.exe)|(?:HD-VmManager.exe)|(?:BlueStacksUninstaller.exe)|(?:HD-ApkHandler.exe)|(?:BlueStacksHelper.exe)|(?:HD-ServiceInstaller.exe)|(?:HD-png2ico.exe)|(?:HD-RunApp.exe)|(?:DiskCompactionTool.exe)|(?:HD-Quit.exe)|(?:7zr.exe))'


# Interpret `allexefiles` as a regular expression
use_regex = True

# Optional: Include specific process IDs (pids) in the analysis
pidlist = ()

# Specify the maximum file size (in MB) for copied files

sizelimit_mb = 1200

# Define regular expression filters for registry keys to exclude
regex_reg_filter = [
    (True, r"HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft.*", re.I),
    (
        False,
        r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer",
        0,
    ),
    (True, r"^[^\\]+\\Software\s*$", re.I),
    (True, r"SOFTWARE$", re.I),
    (True, r"^[^\\]+\\?[^\\]+$", re.I),
    (True, r"Microsoft", re.I),
]

# Specify the minimum depth of registry keys to check
mindepth = 2

# Exclude certain folders from file change detection
forbiddenfolders = (
    r"C:\program files (x86)",
    r"C:\programdata",
    r"C:\program files",
    r"c:\windows",
    os.path.normpath(os.environ.get("USERPROFILE")).lower(),
)

# Exclude folders that match the provided regex pattern
exclude_folders_with_string = r"c:\\windows|nvidia"

# Destination folder to store the copied files
destfolder = "c:\\testcopyxaxyxa"


allregdfs, allreadycopied = scan_processes(
    allexefiles,
    use_regex,
    pidlist,
    regex_reg_filter,
    mindepth,
    sizelimit_mb,
    forbiddenfolders,
    exclude_folders_with_string,
    destfolder,
)


# print(allregdfs[194:204].to_string())
#                          Process    PID                   User      Handle Type ShareFlags                                                                      Name                                                AccessMask                                                                                                               aa_regkey       aa_key aa_type                           aa_value  aa_id       aa_time
# 194  HD-MultiInstanceManager.exe  16824  XXXXXXXXXXXXXXXXXXXXXXX  0x000008BC  Key             HKLM\SYSTEM\ControlSet001\Services\WinSock2\Parameters\Protocol_Catalog9  READ_CONTROL|DELETE|WRITE_DAC|WRITE_OWNER|KEY_ALL_ACCESS    HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries\000000000006  LibraryPath  REG_SZ   %SystemRoot%\system32\NLAapi.dll     11  1.686274e+09
# 195  HD-MultiInstanceManager.exe  16824  XXXXXXXXXXXXXXXXXXXXXXX  0x000008BC  Key             HKLM\SYSTEM\ControlSet001\Services\WinSock2\Parameters\Protocol_Catalog9  READ_CONTROL|DELETE|WRITE_DAC|WRITE_OWNER|KEY_ALL_ACCESS    HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries\000000000007  LibraryPath  REG_SZ   %SystemRoot%\system32\wshbth.dll     11  1.686274e+09
# 196  HD-MultiInstanceManager.exe  16824  XXXXXXXXXXXXXXXXXXXXXXX  0x000008BC  Key             HKLM\SYSTEM\ControlSet001\Services\WinSock2\Parameters\Protocol_Catalog9  READ_CONTROL|DELETE|WRITE_DAC|WRITE_OWNER|KEY_ALL_ACCESS               HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries64                                                             11  1.686274e+09
# 197  HD-MultiInstanceManager.exe  16824  XXXXXXXXXXXXXXXXXXXXXXX  0x000008BC  Key             HKLM\SYSTEM\ControlSet001\Services\WinSock2\Parameters\Protocol_Catalog9  READ_CONTROL|DELETE|WRITE_DAC|WRITE_OWNER|KEY_ALL_ACCESS  HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries64\000000000001  LibraryPath  REG_SZ  %SystemRoot%\system32\napinsp.dll     11  1.686274e+09
# 198  HD-MultiInstanceManager.exe  16824  XXXXXXXXXXXXXXXXXXXXXXX  0x000008BC  Key             HKLM\SYSTEM\ControlSet001\Services\WinSock2\Parameters\Protocol_Catalog9  READ_CONTROL|DELETE|WRITE_DAC|WRITE_OWNER|KEY_ALL_ACCESS  HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries64\000000000002  LibraryPath  REG_SZ  %SystemRoot%\system32\pnrpnsp.dll     11  1.686274e+09
# 199  HD-MultiInstanceManager.exe  16824  XXXXXXXXXXXXXXXXXXXXXXX  0x000008BC  Key             HKLM\SYSTEM\ControlSet001\Services\WinSock2\Parameters\Protocol_Catalog9  READ_CONTROL|DELETE|WRITE_DAC|WRITE_OWNER|KEY_ALL_ACCESS  HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries64\000000000003  LibraryPath  REG_SZ  %SystemRoot%\system32\pnrpnsp.dll     11  1.686274e+09
# 200  HD-MultiInstanceManager.exe  16824  XXXXXXXXXXXXXXXXXXXXXXX  0x000008BC  Key             HKLM\SYSTEM\ControlSet001\Services\WinSock2\Parameters\Protocol_Catalog9  READ_CONTROL|DELETE|WRITE_DAC|WRITE_OWNER|KEY_ALL_ACCESS  HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries64\000000000004  LibraryPath  REG_SZ  %SystemRoot%\System32\mswsock.dll     11  1.686274e+09
# 201  HD-MultiInstanceManager.exe  16824  XXXXXXXXXXXXXXXXXXXXXXX  0x000008BC  Key             HKLM\SYSTEM\ControlSet001\Services\WinSock2\Parameters\Protocol_Catalog9  READ_CONTROL|DELETE|WRITE_DAC|WRITE_OWNER|KEY_ALL_ACCESS  HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries64\000000000005  LibraryPath  REG_SZ   %SystemRoot%\System32\winrnr.dll     11  1.686274e+09
# 202  HD-MultiInstanceManager.exe  16824  XXXXXXXXXXXXXXXXXXXXXXX  0x000008BC  Key             HKLM\SYSTEM\ControlSet001\Services\WinSock2\Parameters\Protocol_Catalog9  READ_CONTROL|DELETE|WRITE_DAC|WRITE_OWNER|KEY_ALL_ACCESS  HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries64\000000000006  LibraryPath  REG_SZ   %SystemRoot%\system32\NLAapi.dll     11  1.686274e+09
# 203  HD-MultiInstanceManager.exe  16824  XXXXXXXXXXXXXXXXXXXXXXX  0x000008BC  Key             HKLM\SYSTEM\ControlSet001\Services\WinSock2\Parameters\Protocol_Catalog9  READ_CONTROL|DELETE|WRITE_DAC|WRITE_OWNER|KEY_ALL_ACCESS  HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\WinSock2\Parameters\NameSpace_Catalog5\Catalog_Entries64\000000000007  LibraryPath  REG_SZ   %SystemRoot%\system32\wshbth.dll     11  1.686274e+09

#                                                       filepath      st_atime          st_atime_ns      st_ctime          st_ctime_ns      st_dev st_file_attributes st_gid             st_ino st_mode      st_mtime          st_mtime_ns st_nlink st_reparse_tag st_size st_uid
# 0  C:\ProgramData\BlueStacks_nxt\Engine\Manager\BstkServer.log  1.686274e+09  1686274447539238400  1.684418e+09  1684418198786032700  3067733448                 32      0  44191571343922300   33206  1.686274e+09  1686274447539238400        1              0    4271      0

```	