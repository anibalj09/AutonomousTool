import os
import sys
import threading
import subprocess
import platform
import json
import time
import httplib
import random
import Queue
import select
import logging
import datetime
import re
import pyautogui
import mechanize

def initializeLogging(mOS):
    """Create log file with logging information."""
    dateAndTime = datetime.datetime.now()
    aFileName = "Log_" + dateAndTime.strftime("%Y-%m-%d_%H-%M") + ".log"
    currentPath = os.path.dirname(os.path.abspath(__file__))

    if mOS == "Linux":
        currentPath += "/logs/"
    elif mOS == "Windows":
        currentPath += "\\logs\\"

    print currentPath
    if not os.path.isdir(currentPath):
        try:
            print "Inside try..."
            os.makedirs("logs")
            print currentPath
            currentPath += aFileName
            logging.basicConfig(filename=currentPath, level=logging.DEBUG)
        except OSError as e:
            print "Inside except.."
            logging.warning("Error in creating directory. Creating log file in current directory.")
            currentPath += aFileName
            logging.basicConfig(filename=currentPath, level=logging.DEBUG)
    else:
        print "Inside else..."
        #logPath += aFileName
        currentPath += aFileName
        print "This is the logpath: " + currentPath
        logging.basicConfig(filename=currentPath, level=logging.DEBUG)
    logging.info("Log file created with name: " + aFileName)


def getOSMachine():
    """Get Operating System of the machine."""
    machineOS = ""
    machineOS = platform.system()
    print "This is the machine's Operating System: " + machineOS
    return machineOS

class KeybrdMouseBrowserAutomationClass:
#TODO: ADD INFO ON BROWSER
#TODO: CHECK/ADD FUNCTIONALITY FOR BROWSER IN MENU.
    """
    This is a class for controling the keyboard and mouse using the PyAutoGUI module.

    PyAutoGUI link: https://pyautogui.readthedocs.io/en/latest/

    Class Variables:
        mousePositionX: Integer that contains the x-coordinate position of the mouse.
        mousePositionY: Integer that contains the y-coordinate position of the mouse.
        screenWidth: Integer that contains the width of the screen.
        screenHeight: Integer that contains the height of the screen.

    Instance Variables:

    Methods:
        setMousePosition: Gets current mouse position and saves it to
        mousePositionX and mousePositionY.
        setScreenSize: Gets screen size and save it to screenWidth and screenHeight.
        clickOnBrowserElements:
    """

    mousePositionX = 0
    mousePositionY = 0
    screenWidth = 0
    screenHeight = 0
    mOS = ""
    websiteListFile = ""
    MachinePassword = "toor"
    browserName = "firefox"
    linksInBrowser = 0

    def __init__(self, OSparameter, downloadFP):
        """Initialize variables."""
        print "Starting KeyboardMouseAutomation Class constructor..."
        self.mOS = OSparameter
        self.setScreenSize()
        self.setMousePosition()
        self.downloadFolderPath = downloadFP
        print "Constructor Finished."
        print "This is the initial links in browser: " + str(self.linksInBrowser)

    def setWebsiteList(self, aFilePath):
        """ """
        
        self.websiteListFile = aFilePath

    def setMousePosition(self):
        """Get current mouse position and save it to mousePositionX and mousePositionY."""
        print "Getting Mouse Position..."

        # Get current mouse position.
        self.mousePositionX, self.mousePositionY = pyautogui.position()
        print "Position X: " + str(self.mousePositionX) + " ; Position Y: " + str(self.mousePositionY)

    def setScreenSize(self):
        """Get screen size and save it to screenWidth and screenHeight."""
        print "Getting Screen Size..."
        # Gets screen size.
        self.screenWidth, self.screenHeight = pyautogui.size()

        print "Screen Width: " + str(self.screenWidth) + " ; Screen Height: " + str(self.screenHeight)

    def openBrowserAndFocus(self, aUrl):
        """ """
        if self.mOS == "Linux":
            subprocess.Popen(["xdg-open", aUrl])
        elif self.mOS == "Windows":
            os.system("start " + aUrl)
        time.sleep(3)
        
    def closeBrowserInstances(self):
        """ """
        if self.mOS == "Linux":
            try:
                browserIdList = []
                browserIdString = subprocess.check_output(["pgrep", self.browserName])
                browserIdList = tempString.split()
                for item in browserIdList:
                    os.system("echo " + self.MachinePassword + " | sudo -S kill " + item)
            except:
                print "Exception occured with trying to close browser."
        elif self.mOS == "Windows":
            pass
            #TODO: add for closing browsers in windows

    def getLinksInBrowser(self, aUrl):
        """"""
        tempBrowser = mechanize.Browser()
        aResponse = tempBrowser.open(aUrl)
        print "This is the response: " + str(aResponse.getcode())
        if aResponse.getcode() >= 400:
            logging.error("Error. Problem in getting to website.")
            tempBrowser.close()
            return
        else:
            keywordList=[".ps1", ".zip", ".py", ".txt", ".exe",".tar.gz",".png",".jpg",".jpeg",".gif",".svg"]
            myFiles=[]
            fileTypes=[]
            aCount = 0

            for aLink in tempBrowser.links():
                for aType in keywordList:
                    if aType in str(aLink):
                        aCount += 1
                        
            self.linksInBrowser = aCount
            print "THIS IS THE NUMBER OF LINKS IN THE PAGE: " + str(self.linksInBrowser)
            tempBrowser.close()       

    def clickOnBrowserElements(self):
        """ """
        pyautogui.moveTo(self.screenWidth/2, self.screenHeight/2)
        # Click on center to focus keyboard on browser window
        pyautogui.click()
        
        if self.mOS == "Linux":
            pyautogui.press('tab')
            # pyautogui.keyDown('shift')
            # pyautogui.press('tab')
            # pyautogui.keyUp('shift')
            # pyautogui.press('enter')
            # time.sleep(2)
            # pyautogui.press('tab')
            # pyautogui.press('enter')
            # time.sleep(2)
            
            #for iteration in range(self.linksInBrowser - 1):
            for iteration in range(self.linksInBrowser):
                # 000webhosting has a clickable element on the lower corner, 
                # which is clicked by default by tab. Shift tab is used to
                # click on the elements needed before that.
                pyautogui.keyDown('shift')
                pyautogui.press('tab')
                pyautogui.keyUp('shift')
                time.sleep(2)
                pyautogui.press('enter')
                
        elif self.mOS == "Windows":
            for iteration in range(self.linksInBrowser):
                # Chrome starts in the first element when tab is pressed.
                pyautogui.press('tab')
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)
            
    def downloadLinksOnPage(self, br, downloadLinks, fileTypes):
        """ """
        rootFolder = os.path.expanduser('~')
        #print "This is the machine OS from inside class: " + self.mOS
        if self.mOS == "Linux":
            rootFolder += "/TempFiles/"
        elif self.mOS == "Windows":
            rootFolder += "\\TempFiles\\"
            
        for x,aLink in enumerate(downloadLinks):
            time.sleep(1)
            
            fileToSave = rootFolder + aLink.text + fileTypes[x]
            print "This is the file to save " + fileToSave
            downloadFile=open(fileToSave, "w")
            br.follow_link(aLink)
            downloadFile.write(br.response().read())
            print aLink.text + " has been downloaded"
            br.back(1)
            time.sleep(1)

    def getDownloadLinksInPage(self, webpageLink):
        """ """
        browserObject = mechanize.Browser()
        aResponse = browserObject.open(webpageLink)
        print "This is the response: " + str(aResponse.getcode())
        if aResponse.getcode() >= 400:
            logging.error("Error. Problem in getting to website.")
            return
        else:
            keywordList=[".ps1", ".zip", ".py", ".txt", ".exe",".tar.gz",".png",".jpg",".jpeg",".gif",".svg"]
            myFiles=[]
            fileTypes=[]

            for aLink in browserObject.links():
                for aType in keywordList:
                    if aType in str(aLink):
                        myFiles.append(aLink)
                        fileTypes.append(aType)
            #return myfiles
            self.downloadLinksOnPage(browserObject, myFiles, fileTypes)
    

class FileActionsClass:
    """
    This is a class for reading and writing into a text file. It will check the
    contents of the Download folder, and run any new file with its default
    program when they appear.

    Class Variables:
        -DownloadFolderPath: This string variable will contain the full path of
            the Download folder in the computer.
        -DownloadFolderList: This list will contain the names of the contents in
            the Download folder.
        -allowedList: This list contains the same amount of elements as
            DownloadFolderList, where each element is a flag that 
            indicates if a script is allowed to run or not.
        -mOS: This string contains the Operating System name.

    Instance Variables:
        -aTextFile: A File variable that is used for creating, reading, and editing
            the text file that will contain the contents of the DownloadFolderList list.

    Methods:
        -setCustomFolder: Checks if path sent exists (or is permitted).
        -setDefaultAllowedList: Updates allowedList to all as allowed.
        -setDownloadFolderList: Gets the names of the files in the download list
            into the DownloadFolderList list.
        -saveAllContentToFiles: Gets the names of the files in the download aList
            into the text file.
        -runSentFile: Gets a file path as a parameter, and runs the file.
        -checkAndRunNewFiles: Check which files are new in the folder,
            and run them all.
    """

    DownloadFolderPath = ""
    DownloadFolderList = []
    allowedList = []
    mOS = ""

    def __init__(self, OSparameter):
        """
        Inialize variables and create the DownloadFolder text file.
        """
        logging.info("Initializing FileActionsClass instance.")
        #print "This is the OSparameter: " + OSparameter
        self.mOS = OSparameter
        # Get Home directory.
        print "Getting home folder path..."
        self.DownloadFolderPath = os.path.expanduser('~')
        logging.debug("Home directory without download folder path extension: " + self.DownloadFolderPath)
        #print "This is the machine OS from inside class: " + self.mOS
        if self.mOS == "Linux":
            self.DownloadFolderPath += "/Downloads/"
        elif self.mOS == "Windows":
            self.DownloadFolderPath += "\\Downloads\\"
        #print "This is the DownloadFolderPath: " + self.DownloadFolderPath
        logging.debug("Full download folder path: " + self.DownloadFolderPath)
        print "Creating text file..."
        self.aTextFile = open("DownloadFolder.txt", 'w')
        self.aTextFile.close()
        logging.info("Text File created for download folder list.")
        logging.info("setDownloadFolderList called.")
        self.setDownloadFolderList()
        logging.info("saveAllContentToFiles called.")
        self.saveAllContentToFiles()

    def setCustomFolder(self, aPath):
        """Gets path of folder to override default download folder."""
        try:
            logging.info("Trying to set custom folder path.")
            if (os.path.isdir(aPath)) and (os.access(aPath, os.R_OK)) and (os.access(aPath, os.R_OK)):
                print "Path is valid, assigning path..."
                self.DownloadFolderPath = aPath
                logging.debug("Custom folder path set.")
                self.setDownloadFolderList()
                self.saveAllContentToFiles()
                return True
            else:
                logging.warning("Custom folder could not be set. Either path is incorrect or permissions are incorrect.")
                print "Path is not valid, or is not permitted."
                return False
        except:
            logging.warning("Exception ocurred while trying to set custom folder.")
            print "Exception occurred. Path may not be valid."
            return False

    def setDefaultAllowedList(self):
        """
        Empty allowedList and append True elements until its the same length
        as DownloadFolderList
        """
        self.allowedList = []

        for item in self.DownloadFolderList:
            self.allowedList.append(True)

        logging.info("Allowedlist all set to True.")

    def setDownloadFolderList(self):
        """
        Get contents of Downloads folder and save them to
        the DownloadFolderList.
        """
        DownloadListString = ""
        if self.mOS == "Linux":
            # DownloadListString = subprocess.check_output(["ls", self.DownloadFolderPath])
            # This prints out the full path of the file.
            DownloadListString = subprocess.check_output("find " + self.DownloadFolderPath + " -type f", shell=True)
            logging.debug("Download folder list (Linux) of files found.")
            self.DownloadFolderList = DownloadListString.split('\n')
        elif self.mOS == "Windows":
            DownloadListString = subprocess.check_output(["dir", self.DownloadFolderPath, "/W"], shell=True)
            logging.debug("Download folder list (Windows) of files found.")
			
			# Removes information added at beginnig of cmd output,
			# by removing everything before the two ']' character instances.
            cutIndex = DownloadListString.find(']')
            if cutIndex > 0:
                cutIndex += 1
                DownloadListString = DownloadListString[cutIndex:]
                cutIndex = DownloadListString.find(']')
                if cutIndex > 0:
                    cutIndex += 1
                    DownloadListString = DownloadListString[cutIndex:]
                else:
                    print "ERROR. Could not process download list output."
                    logging.warning("cutIndex was not greater than 0, output from checking download folder unexpected.")
                    return
            else:
                print "ERROR. Could not process download list output."
                logging.warning("cutIndex was not greater than 0, output from checking download folder unexpected.")
                return
				
			# Splits string by all characters that count as whitespace (\t\n\r\f\v).
            resultList = re.split('\s', DownloadListString)
            logging.debug("This is the resulting list when first splitted: " ''.join(resultList))
			# After splitting, remove all empty elements.
            whiteSpaceCount = resultList.count('')
            while whiteSpaceCount > 0:
                resultList.remove('')
                whiteSpaceCount = whiteSpaceCount - 1
            logging.debug("This is the resulting list when whitespace removed: " ''.join(resultList))
			# Removes information on how many files and space left on directory added by Windows.
            for index in range(9):
                resultList.pop()
            self.DownloadFolderList = resultList	
		
        #self.DownloadFolderList = DownloadListString.split('\n')
        logging.info("Download folder list splitted, with value: " + ''.join(self.DownloadFolderList))

        for index,item in enumerate(self.DownloadFolderList):
            if not item:
                self.DownloadFolderList.pop(index)

       

        if len(self.DownloadFolderList) > len(self.allowedList):
            newLength = len(self.DownloadFolderList) - len(self.allowedList)
            while newLength != 0:
                self.allowedList.append(True)
                newLength -= 1
        
        logging.debug("Allowed List has been updated, with values: " + ''.join(str(x) for x in self.allowedList))

    def saveAllContentToFiles(self):
        """Save content in DownloadFolderList into both text files."""

        self.aTextFile = open("DownloadFolder.txt", 'w')
        json.dump(self.DownloadFolderList, self.aTextFile)
        self.aTextFile.close()
        logging.info("All contents of DownloadFolderList saved to file.")

    def runSentFile(self, aFilePath):
        """Run file in path sent as parameter."""
        logging.info("Sent file path to runSentFile: " + aFilePath)
        if self.mOS == "Linux":
            print "Opening file..."
            # os.system("bash -c \"xdg-open " + self.DownloadFolderPath+item + "\" 2> /dev/null")
            try:
                #anOutput = os.system("bash -c \"xdg-open " + aFilePath + "\" 2> /dev/null")
                #anOutput = subprocess.check_output(["bash -c \"xdg-open " + aFilePath + "\""], shell=True)
                anOutput = os.system("bash -c \"xdg-open \'" + aFilePath + "\'\" 2> /dev/null")
                #print anOutput
                #findError = anOutput.find("No application is registered as handling this file")
                
                # If the output was not zero (there was an error), raise an exception.
                if anOutput == 0:
                    logging.info("File ran succesfully")
                else:
					# Raise exception with description of most probable error.
                    logging.warning("Error in running file, raising CalledProcessError exception.")
                    raise subprocess.CalledProcessError("File could not be run. Most probable cause is that it was an executable, which cannot be run the same way.",None)
            except subprocess.CalledProcessError:            
                logging.info("Opening file with subprocess.Popen, other method failed.")
                #subprocess.Popen(aFilePath, shell=True, stdin=None, stdout=None, stderr=None)
                subprocess.call(["gnome-terminal", "-x", aFilePath])
        elif self.mOS == "Windows":
            print "Opening file..."
            os.system("start " + self.DownloadFolderPath+aFilePath)

    def runAllFilesInFolder(self, aPath):
        #TODO: ADD TO CREATE FOLDER FOR NEW FILES IN SECOND MECHANIZE STAGE.
        #TODO: 
        """Run all files in folder."""
        logging.info("Running all files in folder...")
        if aPath == "" or aPath == None:
            for item in self.DownloadFolderList:
                self.runSentFile(item)
        else:
            DownloadListString = ""
            tempFolderItems = []
            
            if self.mOS == "Linux":
                DownloadListString = subprocess.check_output("find " + aPath + " -type f", shell=True)
                tempFolderItems = DownloadListString.split('\n')
            elif self.mOS == "Windows":
                DownloadListString = subprocess.check_output(["dir", aPath, "/W"], shell=True)
                cutIndex = DownloadListString.find(']')
                if cutIndex > 0:
                    cutIndex += 1
                    DownloadListString = DownloadListString[cutIndex:]
                    cutIndex = DownloadListString.find(']')
                    if cutIndex > 0:
                        cutIndex += 1
                        DownloadListString = DownloadListString[cutIndex:]
                    else:
                        print "ERROR. Could not process download list output."
                        logging.warning("cutIndex was not greater than 0, output from checking download folder unexpected.")
                        return
                else:
                    print "ERROR. Could not process download list output."
                    logging.warning("cutIndex was not greater than 0, output from checking download folder unexpected.")
                    return
                    
                # Splits string by all characters that count as whitespace (\t\n\r\f\v).
                resultList = re.split('\s', DownloadListString)
                logging.debug("This is the resulting list when first splitted: " ''.join(resultList))
                # After splitting, remove all empty elements.
                whiteSpaceCount = resultList.count('')
                while whiteSpaceCount > 0:
                    resultList.remove('')
                    whiteSpaceCount = whiteSpaceCount - 1
                logging.debug("This is the resulting list when whitespace removed: " ''.join(resultList))
                # Removes information on how many files and space left on directory added by Windows.
                for index in range(9):
                    resultList.pop()
                tempFolderItems = resultList	
            
            
            for index,item in enumerate(tempFolderItems):
                if not item:
                    tempFolderItems.pop(index)
            print "This is the downloadFolderList now: "+ ''.join(str(x) for x in tempFolderItems)
            for item in tempFolderItems:
                self.runSentFile(item)

    def checkAndRunNewFiles(self):
		#TODO: Add so it runs the files using runsentfile function.
        """Check what files are new in the Download folder and run the new files."""
        logging.info("setDownloadFolderList called.")
        self.setDownloadFolderList()
        tempList = []
        print "Opening and loading JSON content from text file..."
        doesExist = False
        newFileFound = False
		
        # Check if text file is not empty before opening.
        if os.stat("DownloadFolder.txt").st_size > 0:
            print "DownloadFolder.txt is not empty!"
            logging.info("Downloadfolder.txt is not empty.")
            self.aTextFile = open("DownloadFolder.txt", 'r')
            # Save contents of the text file into a list.
            tempList = json.load(self.aTextFile)
            self.aTextFile.close()

            # Compares contents in file to contents in actual Downloads folder.
            print "Starting loop for checking Download folder for new content"
            for item in self.DownloadFolderList:
                for item2 in tempList:
                    #print "This is item1: " + item + " ; And this is item2: " + item2
                    if item == item2:
                        doesExist = True
                        break

                if doesExist == False:
                    newFileFound = True
                    print "New file found! Opening file " + item
                    runSentFile(item)
                    
                doesExist = False

        else:
            # Run everything in Downloads folder.
            newFileFound = True
            logging.info("DownloadFolder.txt is empty.")
            print "DownloadFolder.txt is empty!"
            for item in self.DownloadFolderList:
				print "New file found! Opening file " + item
				runSentFile(item)

        #print "Checking if newFileFound is false. " + str(newFileFound)
        if newFileFound == False:
            logging.info("No new file found in FTP folder.")
            print "No new file found."
        
        logging.info("saveAllContentToFiles is called.")
        self.saveAllContentToFiles()
        
			


class UtilityClass:
    """
    This is a class for managing the class objects and additional functionality
    that are beyond the scope of the other classes. It will create threads with
    timers for running the functions of the other classes, and check what processes
    are running.

    Class Variables:
        -mOS: String that saves the Operating System of the machine.
        -windowsVersion: Integer that saves the Windows version.
        -MachinePassword: String that contains the password of the machine
            (for Linux machines).
            
    Methods:
        -setTimerStartScript: Assigns custom set value to timerStartScript.
        -setTimerCheckFolder: Assigns custom set value to timerCheckFolder.
        -initializeMachinePassword: Assigns password to MachinePassword.
        -setTimersDefault: Sets all timers to -1 to mark them as
            randomly generated.
        -checkWindowsVersion: Checks what's the version of the Windows machine.
    """

    mOS = ""
    windowsVersion = 0
    MachinePassword = "toor"


    def __init__(self, OSparameter):
        """Initialize the class and the instances of the other classes."""
        logging.info("Initializing UtilityClass instance.")
        self.mOS = OSparameter

    def initializeMachinePassword(self, aPassword):
        """Set password to user input string."""
        self.MachinePassword = aPassword

    def checkWindowsVersion(self):
        """Check Windows OS version."""
        self.windowsVersion = sys.getwindowsversion().major
        logging.debug("Windows version is: " + str(self.windowsVersion))


#######################################################
# WORKER THREADS-----------------------------------
######################################################

class checkFolderWorker(threading.Thread):
    """
    This is a threading class so that threads for checking folder
    for new scripts be assigned to it and have a overriden run function.
    """
    def __init__(self, queue, aLock):
        """Initialize thread and queue."""
        logging.info("Initializing checkFolderWorker instance.")
        threading.Thread.__init__(self)
        self._queue = queue
        self.lockObject = aLock

    def run(self):
        """
        Acquire lock object, check folder for new scripts, and
        update folderList. Release lock at end.
        """
        classObject = self._queue.get()
        self.lockObject[0].acquire()
        logging.info("setDownloadFolderList is called.")
        classObject.setDownloadFolderList()
        logging.info("saveAllContentToFiles is called.")
        classObject.saveAllContentToFiles()
        self.lockObject[0].release()
        print "CHECK FOLDER: Thread has finished."

class clickLinkWorker(threading.Thread):
    """
    """
    def __init__(self, queue, aLock, anUrl):
        """Initialize thread and queue."""
        logging.info("Initializing checkFolderWorker instance.")
        threading.Thread.__init__(self)
        self.url = anUrl
        self._queue = queue
        self.lockObject = aLock

    def run(self):
        """
        Acquire lock object, check folder for new scripts, and
        update folderList. Release lock at end.
        """
        classObject = self._queue.get()
        self.lockObject[0].acquire()
        
        classObject.getLinksInBrowser(self.url) 
        classObject.openBrowserAndFocus(self.url)
        classObject.clickOnBrowserElements()
        #classObject.closeBrowserInstances()
        
        self.lockObject[0].release()
        print "CHECK FOLDER: Thread has finished."
        
class downloadLinkWorker(threading.Thread):
    """
    """
    def __init__(self, queue, aLock, anUrl):
        """Initialize thread and queue."""
        logging.info("Initializing checkFolderWorker instance.")
        threading.Thread.__init__(self)
        self.url = anUrl
        self._queue = queue
        self.lockObject = aLock

    def run(self):
        """
        Acquire lock object, check folder for new scripts, and
        update folderList. Release lock at end.
        """
        classObject = self._queue.get()
        self.lockObject[0].acquire()
        classObject.getDownloadLinksInPage(self.url)
        self.lockObject[0].release()
        print "CHECK FOLDER: Thread has finished."

class runScriptWorker(threading.Thread):
    """
    This is a threading class so that threads for running random scripts
     be assigned to it and have a overriden run function.
    """
    def __init__(self, queue, aLock, aPath):
        """Initialize Script Worker class."""
        logging.info("Initializing runScriptWorker instance.")
        threading.Thread.__init__(self)
        self._queue = queue
        self.lockObject = aLock
        self.NewPath = aPath

    def run(self):
        """
        Acquire lock object, and run random script.
        Release lock at end.
        """
        classObject = self._queue.get()
        self.lockObject[0].acquire()
        logging.info("runRandomScript is called.")
        # TODO: Change so its for running all files in the folder.
        #classObject.runRandomScript()
        classObject.runAllFilesInFolder(self.NewPath)
        self.lockObject[0].release()
        print "RUN SCRIPT: Thread has finished."

#######################################################
# WORKER THREADS-----------------------------------
######################################################

class MenuActionClass:
	#TODO: When changing folders for FTP, arrays of files has to be updated
	#      to get the ones from the new folder, they are not updating.
    """
    This is a class for the menu actions in the terminal. It will allow
    users to select different actions for changing the behaviour of the
    autonomous tool.

    Class Variables:
        -mOS: String that contains the name of the machine's Operating System.
        -utilityClassObject: Class instance of the UtilityClass.
        -fileActionsClassObject: Class instance of the FileActionsClass.

    Instance Variables:
        -checkFolderTask: String for indicating if task is to check folder.
        -stopAVTask: String for indicating if task is to stop AV software.
        -startScriptTask: String for indicating if task is to run random script.
		-utilityClassObject: Object for accessing utilityClass elements.
		-fileActionsClassObject: Object for accessing fileActionsClass elements.
		
    Methods:
        -printMenu: This function will print the Main Menu of the tool.
        -mainMenuLoop: This function will start the loop of the main menu.
        -setTimers: Function for asking user for set timers for
            the different behaviours.
        -behaviourList: Lists the different action this application can do,
            and allows user to select one to execute for testing.
        -checkAndRunDownloadFolder: Checks download folder for new scripts,
            and runs them.
        -createWorkerThread: Create thread object, assign them to
            correct task, and start them.
        -algorithmLoop: Function that loops, running all thread until the user
            stops it.

    """

    mOS = ""
    utilityClassObject = None
    fileActionsClassObject = None
    keybrdMouseClassObject = None

    def __init__(self, tempOSParam):
        """Initialize the tool. Print the menu and start the menu loop."""
        logging.info("Initializing MenuActionClass instance.")
        self.mOS = tempOSParam
        self.clickLinkTask = "click-link"
        self.downloadMechanizeTask = "download-mechanize"
        self.startScriptTask = "start-script"
        self.checkFolderTask = "check-folder"
        logging.info("Initializing utilityClassObject and fileActionsClassObject instances.")
        self.utilityClassObject = UtilityClass(tempOSParam)
        self.fileActionsClassObject = FileActionsClass(tempOSParam)
        self.keybrdMouseClassObject = KeybrdMouseBrowserAutomationClass(tempOSParam, self.fileActionsClassObject.DownloadFolderPath)
        logging.info("printMenu is called.")
        logging.info("mainMenuLoop is called.")
        #self.mainMenuLoop()


    def printMenu(self):
        """ Print the menu of the functions that the user can select from."""

        print """
        +-------------------------------------------------+
        Autonomous tool for replicating human actions
        in a virtual network.

        Enter one of the following letters (lower/uppercase)
        to access its functions.


        s  --> See the different behaviours of this tool.
        h  --> Print this window again.
        d  --> Set everything to default.
        a  --> Read the About file for this application.
        f  --> Change the folder for FTP.
        p  --> Change the default password.
        v  --> Change default Antivirus name.
        dc --> Download files from website by clicking links
        db --> Download files from website within Python
        r  --> Run application with current configuration.

        e  --> Exit this application


        +-------------------------------------------------+
        """

    def mainMenuLoop(self):
        """Start infinite loop for receiving input from user."""
        returnString = ""
        logging.info("Starting menu loop.")
        self.printMenu()
		
        while True:
            returnString = raw_input("Enter your command -->")

            if returnString == "s" or returnString == "S":
                self.behaviourList()
            elif returnString == "h" or returnString == "H":
                self.printMenu()
            elif returnString == "r" or returnString == "R":
                self.algorithmLoop()
            elif returnString == "f" or returnString == "F":
                print "Current FTP folder path: " + self.fileActionsClassObject.DownloadFolderPath
                newFTPPath = raw_input("Enter path for FTP folder: ")
                self.fileActionsClassObject.setCustomFolder(newFTPPath)
            elif returnString == "p" or returnString == "P":
				newPassword = raw_input("Enter new password: ")
				if newPassword and newPassword.isalnum():
					logging.debug("Password string is valid. Changing default password.")
					print "Changing password..."
					self.utilityClassObject.initializeMachinePassword(newPassword)
					print "Changed!"
				else:
					logging.warning("Password string was incorrect.")
					print "ERROR. Password input was not a valid input. Try again."
            elif returnString == "v" or returnString == "V":
				print "Current antivirus name: " + self.utitlityClassObject.defaultAntivirus
				newAVName = raw_input("Enter the new Antivirus Name: ")
				if newAVName and newAVName.isalnum():
					logging.debug("New Antivirus name entered: " + newAVName)
					print "Changing Antivirus Name..."
					self.utilityClassObject.changeDefaultAntivirus(newAVName)
					print "Changed!"
				else:
					logging.warning("New Antivirus name input was incorrect, null or not alphanumeric.")
					print "ERROR! Antivirus name was not valid. Try again."
            elif returnString == "dc" or returnString == "DC" or returnString == "Dc" or returnString == "dC":
                self.getWebsiteForDownloadClick()
            elif returnString == "db" or returnString == "DB" or returnString == "Db" or returnString == "dB":
                self.getWebsiteForDownloadMechanize()
            elif returnString == "d" or returnString == "D":
                print "Refreshing script list..."
                logging.info("setDownloadFolderList is called.")
                self.fileActionsClassObject.setDownloadFolderList()
                logging.info("saveAllContentToFiles is called.")
                self.fileActionsClassObject.saveAllContentToFiles()
                print "Setting all scripts as allowed..."
                logging.info("setDefaultAllowedList is called.")
                self.fileActionsClassObject.setDefaultAllowedList()
                print "Done!"
            elif returnString == "e" or returnString == "E":
                print "Exiting the application..."
                break
            else:
                print "Error. Command was not recognized, try again."

            print "\n"
            logging.info("printMenu is called.")
            self.printMenu()

    def getWebsiteForDownloadClick(self):
        """Get input from user of website address to download files from."""       
        aLock = [threading.Lock()]
        queue = Queue.Queue()
        worker_threads = []
        
        aWebsite = ""
        aWebsite = raw_input("Enter the full address of the website to download files from: ")
        if aWebsite == None or aWebsite == "":
            logging.info("Website is invalid.")
            print "Error. Website is invalid."
            return

        logging.info("createWorkerThread called with task: " + self.clickLinkTask)
        aWorker = self.createWorkerThread(queue, 1, self.clickLinkTask, aLock, aWebsite)
        if aWorker:
            print "Running thread to check folder..."
            worker_threads.append(aWorker)
            logging.info("Worker thread appended.")
            queue.put(self.keybrdMouseClassObject)
        else:
            pass
        time.sleep(3)
        logging.info("createWorkerThread called with task: " + self.checkFolderTask)
        aWorker = self.createWorkerThread(queue, 1, self.checkFolderTask, aLock, "")
        if aWorker:
            print "Running thread to check folder..."
            worker_threads.append(aWorker)
            logging.info("Worker thread appended.")
            queue.put(self.fileActionsClassObject)
        else:
            pass
        time.sleep(3)
        logging.info("createWorkerThread called with task: " + self.startScriptTask)
        aWorker = self.createWorkerThread(queue, 1, self.startScriptTask, aLock, "")
        if aWorker:
            print "Running thread to start script..."
            worker_threads.append(aWorker)
            logging.info("Worker thread appended.")
            queue.put(self.fileActionsClassObject)
        else:
            pass
        time.sleep(3)
        

        for worker in worker_threads:
            #print "Waiting for threads to finish..."
            worker.join()
            time.sleep(1)
        
            
    def getWebsiteForDownloadMechanize(self):
        """Get input from user of website address to download files from."""
        aLock = [threading.Lock()]
        queue = Queue.Queue()
        worker_threads = []
        
        aWebsite = ""
        aWebsite = raw_input("Enter the full address of the website to download files from: ")
        if aWebsite == None or aWebsite == "":
            logging.info("Website is invalid.")
            print "Error. Website is invalid."
            return
        
        logging.info("createWorkerThread called with task: " + self.downloadMechanizeTask)
        aWorker = self.createWorkerThread(queue, 1, self.downloadMechanizeTask, aLock, aWebsite)
        if aWorker:
            print "Running thread to start script..."
            worker_threads.append(aWorker)
            logging.info("Worker thread appended.")
            queue.put(self.keybrdMouseClassObject)
        else:
            pass
        time.sleep(3)
        logging.info("createWorkerThread called with task: " + self.checkFolderTask)
        aWorker = self.createWorkerThread(queue, 1, self.checkFolderTask, aLock, "")
        if aWorker:
            print "Running thread to check folder..."
            worker_threads.append(aWorker)
            logging.info("Worker thread appended.")
            queue.put(self.fileActionsClassObject)
        else:
            pass
        time.sleep(3)
        logging.info("createWorkerThread called with task: " + self.startScriptTask)

        print "Getting home folder path..."
        rootFolder = os.path.expanduser('~')
        #print "This is the machine OS from inside class: " + self.mOS
        if self.mOS == "Linux":
            rootFolder += "/TempFiles/"
        elif self.mOS == "Windows":
            rootFolder += "\\TempFiles\\"
        
        aWorker = self.createWorkerThread(queue, 1, self.startScriptTask, aLock, rootFolder )
        if aWorker:
            print "Running thread to start script..."
            worker_threads.append(aWorker)
            logging.info("Worker thread appended.")
            queue.put(self.fileActionsClassObject)
        else:
            pass
        time.sleep(3)

        
        for worker in worker_threads:
            #print "Waiting for threads to finish..."
            worker.join()
            time.sleep(1)
    

    def behaviourList(self):
        """Print the different actions of this tool."""

        returnString = ""
        aLink = ""
        subNumber = ""
        anInt = 0

        while True:
            anOutput = ""
            aTempList = []
            if self.mOS == "Linux":
                for index,item in enumerate(self.fileActionsClassObject.DownloadFolderList):
                    aTempList = item.split("/")
                    anOutput += "\t2." + str(index + 1) + " " + aTempList[(len(aTempList))-1] + " - " + str(self.fileActionsClassObject.allowedList[index]) + "\n"
            elif self.mOS == "Windows":
                for index,item in enumerate(self.fileActionsClassObject.DownloadFolderList):
                    anOutput += "\t2." + str(index + 1) + " " + item + " - " + str(self.fileActionsClassObject.allowedList[index]) +  "\n"
            
            fullBlock = """
        +-------------------------------------------------+
        This the list of the functions that this tool can
        do. Enter one of the numbers to execute that action,
        or enter 'b' to go back to the main menu.

        1. Check the download folder and run any new files
        that have appeared.

        2. Activate an internal malicious script (Only enter 2.1, 2.2, ...).

%s


        b --> Go back to Main Menu.

        +-------------------------------------------------+
        """
            
            print fullBlock % (anOutput)
            returnString = raw_input("Enter your command -->")
            if returnString != None and returnString != "" and returnString != " ":
                if returnString == "1":
					#return here
                    logging.info("setDownloadFolderList is called.")
                    self.fileActionsClassObject.setDownloadFolderList()
                    logging.info("saveAllContentToFiles is called.")
                    self.fileActionsClassObject.saveAllContentToFiles()
                    logging.info("checkAndRunDownloadFolder is called.")
                    self.checkAndRunDownloadFolder()

                elif returnString[0] == "2":
                    if len(returnString) >= 3:
                        subNumber = returnString[2:]
                        if subNumber.isdigit():
                            anInt = int(subNumber)
                            print "Finding file #" + str(anInt) + " in list..."
                            for index,item in enumerate(self.fileActionsClassObject.DownloadFolderList):
                                if index == anInt-1:
                                    print "Running file " + item
                                    logging.info("runSentFile is called, with item: " + item)
                                    self.fileActionsClassObject.runSentFile(item)

                    else:
                        print "Error, enter script as 2.# (Where # is the number of the script.)"
                # elif returnString == "3":
                    # aLink =  raw_input("Please enter the link for the webpage to access: ")
                elif returnString == "b" or returnString == "B":
                    break
                else:
                    print "Error. Command was not recognized, try again."
            else:
                print "Error. Command was not recognized, try again."

    def checkAndRunDownloadFolder(self):
        """Runs new files in folder."""
        logging.info("checkAndRunNewFiles is called.")
        self.fileActionsClassObject.checkAndRunNewFiles()

    def createWorkerThread(self, queue, size, aTaskName, aLock, anUrl):
        """Create thread with custom task."""
        print "This is the task sent: " + aTaskName

        if aTaskName == self.checkFolderTask:
            logging.info("Check folder worker instance made.")
            worker = checkFolderWorker(queue, aLock)
            worker.start()
            return worker
        elif aTaskName == self.downloadMechanizeTask:
            logging.info("Stop antivirus worker instance made.")
            worker = downloadLinkWorker(queue, aLock, anUrl)
            worker.start()
            return worker
        elif aTaskName == self.clickLinkTask:
            logging.info("Run random script instance made.")
            worker = clickLinkWorker(queue, aLock, anUrl)
            worker.start()
            return worker
        elif aTaskName == self.startScriptTask:
            logging.info("Run random script instance made.")
            worker = runScriptWorker(queue, aLock, anUrl)
            worker.start()
            return worker
        else:
            print "ERROR. RETURNED NONE."
            return None


    def algorithmLoop(self):
        """
        Start infinite loop that calls the main functions of the tool
        using timers.
        """
        aLock = [threading.Lock()]
        queue = Queue.Queue()
        worker_threads = []
        
        aWebsite = ""
        aWebsite = raw_input("Enter the full address of the website to download files from: ")
        if aWebsite == None or aWebsite == "":
            logging.info("Website is invalid.")
            print "Error. Website is invalid."
            return

        logging.info("createWorkerThread called with task: " + self.clickLinkTask)
        aWorker = self.createWorkerThread(queue, 1, self.clickLinkTask, aLock, aWebsite)
        if aWorker:
            print "Running thread to check folder..."
            worker_threads.append(aWorker)
            logging.info("Worker thread appended.")
            queue.put(self.keybrdMouseClassObject)
        else:
            pass
        time.sleep(3)
        logging.info("createWorkerThread called with task: " + self.checkFolderTask)
        aWorker = self.createWorkerThread(queue, 1, self.checkFolderTask, aLock, "")
        if aWorker:
            print "Running thread to check folder..."
            worker_threads.append(aWorker)
            logging.info("Worker thread appended.")
            queue.put(self.fileActionsClassObject)
        else:
            pass
        time.sleep(3)
        logging.info("createWorkerThread called with task: " + self.startScriptTask)
        aWorker = self.createWorkerThread(queue, 1, self.startScriptTask, aLock, "")
        if aWorker:
            print "Running thread to start script..."
            worker_threads.append(aWorker)
            logging.info("Worker thread appended.")
            queue.put(self.fileActionsClassObject)
        else:
            pass
        time.sleep(3)
        # Change the task names for the appropiate ones.
        logging.info("createWorkerThread called with task: " + self.downloadMechanizeTask)
        aWorker = self.createWorkerThread(queue, 1, self.downloadMechanizeTask, aLock, aWebsite)
        if aWorker:
            print "Running thread to start script..."
            worker_threads.append(aWorker)
            logging.info("Worker thread appended.")
            queue.put(self.keybrdMouseClassObject)
        else:
            pass
        time.sleep(3)
        logging.info("createWorkerThread called with task: " + self.checkFolderTask)
        aWorker = self.createWorkerThread(queue, 1, self.checkFolderTask, aLock, "")
        if aWorker:
            print "Running thread to check folder..."
            worker_threads.append(aWorker)
            logging.info("Worker thread appended.")
            queue.put(self.fileActionsClassObject)
        else:
            pass
        time.sleep(3)
        logging.info("createWorkerThread called with task: " + self.startScriptTask)

        print "Getting home folder path..."
        rootFolder = os.path.expanduser('~')
        #print "This is the machine OS from inside class: " + self.mOS
        if self.mOS == "Linux":
            rootFolder += "/TempFiles/"
        elif self.mOS == "Windows":
            rootFolder += "\\TempFiles\\"
        
        aWorker = self.createWorkerThread(queue, 1, self.startScriptTask, aLock, rootFolder )
        if aWorker:
            print "Running thread to start script..."
            worker_threads.append(aWorker)
            logging.info("Worker thread appended.")
            queue.put(self.fileActionsClassObject)
        else:
            pass
        time.sleep(3)


        for worker in worker_threads:
            #print "Waiting for threads to finish..."
            worker.join()
            time.sleep(1)



def main():
    """Start application."""
    
    cmdArguments = []
    mOS = getOSMachine()
    initializeLogging(mOS)
    logging.info("MenuActionClass instace being created.")
    mainMenuObject = MenuActionClass(mOS)
    
    #Get arguments from command line, except file name.
    cmdArguments = sys.argv[1:]
    
    if cmdArguments:
        if cmdArguments.pop() == "m":
            #print "Main menu will open now..."
            logging.info("m character received as argument. Opening main menu.")
            mainMenuObject.mainMenuLoop()
        else:
            logging.info("Argument was not expected, algorithmLoop called.")
            print "Autonomous action starting now..."
            mainMenuObject.algorithmLoop()
    else:
        print "Autonomous actioin starting now..."
        mainMenuObject.algorithmLoop()
    
    


if __name__ == "__main__":
    main()
