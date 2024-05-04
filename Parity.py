import os


def description():
    input('This is an advance deleting and copying program.\n'
          'This program compares between two paths one called Source Path and the other Destination Path. '
          'When you provide Source and Destination Path the program generates and shows a list of files '
          'and folders that are available in the Source but not in Destination, essentially checking '
          'parities between directory tree of the two provided paths.\n'
          'The user can then choose an option among two processing modes of this program.\n\n'
          'Copy Mode:\n'
          'Under this mode the program will copy all files and folders available in Source but not in '
          'Destination to the Destination in the same directory tree format as in Source. This will essentially'
          'create a directory tree in Destination as in Source.\n'
          'Note: This will NOT delete any files or folders in Destination that may already be '
          'in the Destination.\n\n'
          'Deleting Mode:\n'
          'Under this mode the program will compare all files and folders in Source and Destination. Then the program'
          'deletes all files and folders available in the Source but not in Destination from the Source.\n\n'
          'Note on Source and Destination Path usage:\n'
          'The Source path must open the folder you want processed. For example if the folder you want'
          ' to be processed is named EXAMPLE, the provided example Source Path should be C:\\Desktop\\EXAMPLE.\n'
          'The Destination Path must open the containing folder of the folder you want to check parity with. '
          'For example if Source Path provided is C:\\Desktop\\EXAMPLE the example Destination Path may be '
          'C:\\Desktop\\DESTINATION, where folder DESTINATION may contain folder EXAMPLE.'
          ' The program will check for folder and directory tree "EXAMPLE" inside directory "DESTINATION" and'
          ' create it if not found.\n\n\n'
          'Enter any key to continue.')


os.system('cd C:\\Windows')    # Required for colours to work after compiling with pyinstaller, i don't know why
class bcolors:
    pink = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'
# Used to colour process output texts


while True:
    print(bcolors.bold + bcolors.yellow +
          'WELCOME. To learn the usage of this program please pass "help" as Source Path' +
          bcolors.end)
    sourcePath = str(input('Source path:'))
    if sourcePath.lower() == 'help':
        os.system('cls')
        description()
        os.system('cls')
    else:
        break

destPath = str(input('Destination path:'))

# defines a sourcePath in a standard format named working path
if sourcePath[-1] == '\\':
    workingPath = sourcePath[:-1]
else:
    workingPath = sourcePath

# defines a destPath in a standard format named workingDestPath
if destPath[-1] == '\\':
    workingDestPath = destPath[:-1]
else:
    workingDestPath = destPath

processResult = []
workableDirPaths = {}
workableFilePaths = {}


def name(path):
    Name = ''
    # below code extracts dir name from From path and returns it
    revPath = list(path)
    revPath.reverse()
    for elem in revPath:
        if Name == '' and elem == '\\':
            continue
        elif Name != '' and elem == '\\':
            NameInList = list(Name)
            NameInList.reverse()
            Name = ''.join(NameInList)
            # print(Name)
            break
        else:
            Name += elem
    return Name
# Returns name of the dir opened by provided path


def make_dir(From, To):
    Name = name(From)
    # below code makes the required directory
    DirMade = str(os.system('mkdir "%s"' % (To + '\\' + Name)))
    if DirMade == '0':
        processResult.append(bcolors.green +
                             'Directory "%s" made successfully' % (To + '\\' + Name) +
                             bcolors.end)
        return True
    else:
        print('An error occurred while making directory %s' % (To + '\\' + Name))
        stop = str(input('Press any key to continue. Enter X to stop and exit.'))
        if stop == 'X' or stop == 'x':
            raise SystemExit
# Uses name function on From and uses obtained Name to make dir of same name in To


def checkNmakeParentDir():
    try:
        if str(os.listdir(destPath).count(name(sourcePath))) == '0':
            make_dir(sourcePath, destPath)
            processResult.append(bcolors.green +
                                 'Parent directory "%s" made successfully at the destination' % (name(sourcePath)) +
                                 bcolors.end)
        else:
            processResult.append(bcolors.blue +
                                 'Parent directory "%s" exists at the destination' % (name(sourcePath)) +
                                 bcolors.end)
    except Exception as exc:
        input('A "' + bcolors.red + '%s' % exc + bcolors.end + '" error occurred while trying to list directories in '
                                                              'provided Destination Path.\nPress any key to Exit.')
        raise SystemExit
# Above code checks destPath for dir opened by sourcePath and makes it if not found


def get_all_dir_paths(path):
    allDirPathsInSource = []
    for root, dirs, files in os.walk("%s" % path):
        for dir in dirs:
            if dir == '':
                continue
            else:
                allDirPathsInSource.append(root + '\\%s' % dir)
    return allDirPathsInSource
# Above code returns a list of paths to all dirs in the dir tree of provided path


def get_all_file_paths(path):
    # Checks if path is valid
    try:
        os.listdir(path)
    except Exception as exc:
        input('A "' + bcolors.red + '%s' % exc + bcolors.end + '" error occurred while trying to list directories in '
                                                               'provided Source Path.\nPress any key to Exit.')
        raise SystemExit
    allFilePathsInSource = []
    for root, dirs, files in os.walk("%s" % path):
        for file in files:
            if file == '':
                continue
            else:
                allFilePathsInSource.append(root + '\\%s' % file)
    return allFilePathsInSource
# Above code returns a list of paths to all files in the dir tree of provided path


def checkInDest():
    for dirP in get_all_dir_paths(workingPath):
        if not os.path.isdir(workingDestPath + '\\' + name(sourcePath) + dirP[len(workingPath):]):
            workableDirPaths[dirP] = workingDestPath + '\\' + name(sourcePath) + dirP[len(workingPath):-len(name(dirP))]
        else:
            continue
    if workableDirPaths == {}:
        processResult.append(bcolors.blue +
                             'No directories available in source that are not available in destination' +
                             bcolors.end)
    for fileP in get_all_file_paths(workingPath):
        if not os.path.isfile(workingDestPath + '\\' + name(sourcePath) + fileP[len(workingPath):]):
            workableFilePaths[fileP] = workingDestPath + '\\' + name(sourcePath) + fileP[
                                                                                   len(workingPath):-len(name(fileP))]
        else:
            continue
    if workableFilePaths == {}:
        processResult.append(bcolors.blue +
                             'No files available in source that are not available in destination' +
                             bcolors.end)
    if workableDirPaths == {} and workableFilePaths == {}:
        global execution
        execution = False
    else:
        execution = True
# Appends & Returns all paths not available in Dest but Source as a dictionary in format {SourcePath:DestPath}
# Appending to variable for unavailable Dir is workableDirPaths
# Appending to variable for unavailable File is workableFilePaths


def executeCopy():
    for d in workableDirPaths:
        make_dir(d, workableDirPaths[d])
        processResult.append(bcolors.green +
                             'Directory "%s" made successfully.' % (workableDirPaths[d] + name(d)) + bcolors.end)
    for f in workableFilePaths:
        check = str(os.system('copy "%s" "%s" /Z' % (f, workableFilePaths[f])))
        if check == '0':
            processResult.append(bcolors.green +
                                 'Copied file "%s" to "%s" successfully.' % (f, workableFilePaths[f]) + bcolors.end)
        else:
            processResult.append(bcolors.red +
                                 'An error occurred while copying file "%s" to "%s"' % (f, workableFilePaths[f]) +
                                 bcolors.end)
# Executes a copying command that copies all unavailable files and dirs from source to destination


def executeDel():
    for f in workableFilePaths:
        check1 = str(os.system('del "%s"' % f))
        if check1 == '0':
            processResult.append(bcolors.green + 'Deleted "%s" successfully' % f + bcolors.end)
        else:
            processResult.append(bcolors.red + 'An error occurred while deleting "%s"' % f + bcolors.end)
    for d in workableDirPaths:
        check2 = str(os.system('rmdir "%s" /S /Q' % d))
        if check2 == '0':
            processResult.append(bcolors.green + 'Removed "%s" successfully' % d + bcolors.end)
        else:
            processResult.append(bcolors.red + 'An error occurred while removing "%s"' % d + bcolors.end)
# Executes a erasing command that deletes all unavailable files and dirs compared to source in destination


def print_workable():
    print(bcolors.bold + bcolors.blue + '\nFiles in Source not available in Destination:' + bcolors.end)
    index = 0
    if len(workableFilePaths) == 0:
        print('None')
    else:
        for f in workableFilePaths:
            index += 1
            print('%s. %s' % (index, f))

    print(bcolors.bold + bcolors.blue + '\nDirectories in Source not available in Destination:' + bcolors.end)
    index = 0
    if len(workableDirPaths) == 0:
        print('None')
    else:
        for d in workableDirPaths:
            index += 1
            print('%s. %s' % (index, d))
    print('\n\n\n')
# prints unavailable files and directories


def execute():
    while execution:
        print_workable()
        processingMode = str(input('Type "Del" to enter Erasing mode. Type "Copy" to enter Copying mode:')).upper()
        if processingMode == 'DEL':
            executeDel()
            break
        elif processingMode == 'COPY':
            executeCopy()
            break
        else:
            os.system('cls')
            print('\n\n\n\n\n\nInvalid input try again.')
# Prompts to choose a processing mode


# Execution Block
checkNmakeParentDir()


checkInDest()


execute()


print('\n\n\n----------------------------------------------------------------------------\n\n\n')
print(bcolors.bold + bcolors.yellow + 'Process Finished. Process Report:' + bcolors.end)
print('\n'.join(processResult))
print('\n\n')
input('Press any key to exit.')
