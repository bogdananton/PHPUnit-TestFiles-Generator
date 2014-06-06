import os
import re
import io, json
import datetime

##################################################
# configuration paths
##################################################
base_PATH = "D:\\root\\todounit\\example\\"
repository_PATH = base_PATH + "\\classes\\"
reports_PATH = "D:\\root\\todounit\\reporting\\"
tests_destination_PATH = base_PATH + 'tests\\'
##################################################
DO_REMOVE_TODO_UNIT_LINE = False # set to False if you don't want to change the files in the repository_PATH
DO_CREATE_TEST_STRUCTURE = True | DO_REMOVE_TODO_UNIT_LINE # if DO_REMOVE_TODO_UNIT_LINE is set to True (will delete comments, then create structure)
##################################################

allFilesList = []
testsListWaiting = [] # pending, waiting to recover method (pattern "function something")
testsListFinal   = [] # final list

existingTestFiles = [] # scrape of current test files
existingTests = [] # scrape of current tests

def traverseFolders(folder, source_type):
    for root, subFolders, files in os.walk(folder):
        for file in files:
            if(source_type == 'repo'):
                allFilesList.append(os.path.join(root,file))
            else :
                existingTestFiles.append(os.path.join(root,file))

        for subFolder in subFolders:
            traverseFolders(subFolder, source_type)
    pass

def findPhpunitComment(line):
    m = re.search('(?<=@todounit)(.*)', line)
    if not (m is None):
        return (m.group(1)).strip().split('\t')
    else:
        return False

def findMethod(line):
    m = re.search('(?<=function )([a-zA-Z0-9\_]+)', line)
    if not (m is None):
        return (m.group(1)).strip()
    else:
        return False

def findClass(line):
    m = re.search('(?<=class )([a-zA-Z0-9\_]+)', line)
    if not (m is None):
        return (m.group(1)).strip()
    else:
        return False

def assignTestsListWaiting(methodName):
    for pendingTestStrings in testsListWaiting:
        pendingTestStrings[2] = methodName
        testsListFinal.append(pendingTestStrings)
    pass

def createTestScaffold(data):
    relativeBaseFolder = getRelativeBaseFolder(data[0])+'\\'+data[1]
    fullTestFolder_PATH = tests_destination_PATH + relativeBaseFolder

    if(os.path.isdir(fullTestFolder_PATH) == False):
        os.makedirs(fullTestFolder_PATH)

    testFullFilename_PATH = fullTestFolder_PATH + '\\' + data[2]+'.php'
    if(os.path.exists(testFullFilename_PATH) == False):
        createBaseText = """<?php

class """+data[1]+'_'+data[2]+""" extends PHPUnit_Framework_TestCase {

}"""
        with io.open(testFullFilename_PATH, 'w', encoding='utf-8') as f:
            f.write(unicode(createBaseText))

    # count current number of lines
    readFile = open(testFullFilename_PATH)
    lines = readFile.readlines()
    readFile.close()


    # add description and meta data (covers, ...)
    description_docblock = """/**
    * @covers """+data[1]+"""::"""+data[2]

    if(data[4] != ""):
        description_docblock += """
    * """+data[4]


    description_docblock += """
    */"""

    w = open(testFullFilename_PATH,'w')
    # keep all except the last line
    w.writelines([item for item in lines[:-1]])

    # append new test method
    w.write(unicode( """
    """+description_docblock+"""
    public function test"""+data[3]+"""(){
        // implement me
        $this->markTestSkipped('Auto generated method using phpunit docblock');
    }

}"""))
    w.close()
    # print relativeBaseFolder
    pass

def getRelativeBaseFolder(full_PATH):
    old_file_PATH = full_PATH.replace(base_PATH,'')
    k = old_file_PATH.rfind("\\")
    return old_file_PATH[:k]


# scan existing tests
traverseFolders(tests_destination_PATH, 'tests') # fill tests list

existingTestsList = []
newlyFoundTests = []
hashedTests = [] # will be used to check if method is already covered

for test_file_under_test in existingTestFiles:
    latestClassFound = 'no_class' # init
    file = open(test_file_under_test, 'r')
        
    for line in file:
        #find latest class definition
        findClassDefinition = findClass(line)
        if findClassDefinition:
            latestClassFound = findClassDefinition

        foundMethod = findMethod(line)
        if foundMethod:
            existingTestsList.append([test_file_under_test, latestClassFound, foundMethod])

            hashedClassName = latestClassFound
            #if hashedClassName[-4:] == 'Test':
            #    hashedClassName = hashedClassName[0:-4]

            hashedTests.append(test_file_under_test.replace(tests_destination_PATH,'') + ' | ' + hashedClassName+ ' | ' + foundMethod);
        pass
    file.close()

# fill source list
traverseFolders(repository_PATH, 'repo')

for file_under_test in allFilesList:
    # clean existing / previous unmatched docblock from testsListWaiting
    testsListWaiting = [] # clean pending list

    latestClassFound = 'no_class'
    file = open(file_under_test, 'r')

    linesToBeRemoved = []
    cursorLinesToBeRemoved = -1
    for line in file:
        cursorLinesToBeRemoved += 1

        #find latest class definition
        findClassDefinition = findClass(line)
        if findClassDefinition:
            latestClassFound = findClassDefinition

        # find docblock comment
        foundPhpunitDoc = findPhpunitComment(line)
        if foundPhpunitDoc:
            linesToBeRemoved.append(cursorLinesToBeRemoved)

            title = ''
            description = ''
            title = foundPhpunitDoc[0]

            if(len(foundPhpunitDoc) > 1):
                description = foundPhpunitDoc[1].strip()

            # push pending 
            testsListWaiting.append([file_under_test, latestClassFound, '', title, description])

        foundMethod = findMethod(line)
        if foundMethod:
            assignTestsListWaiting(foundMethod)
            testsListWaiting = [] # clean pending list
            pass
        pass
    file.close()

    if len(linesToBeRemoved) > 0 & DO_REMOVE_TODO_UNIT_LINE == True:
        file = open(file_under_test, 'r')
        cursor = -1
        valueOutput = ''

        for line in file:
            cursor += 1

            if(cursor not in linesToBeRemoved):
                valueOutput += line

        file.close()

        f = open(file_under_test,'w')
        f.write(valueOutput)
        f.close()


# save report scanned
data_string = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
# report_file_path_json = reports_PATH + 'source_scan_' + data_string + '.json'
# with io.open(report_file_path_json, 'w', encoding='utf-8') as f:
#    f.write(unicode(json.dumps(testsListFinal, ensure_ascii=False)))

report_file_path_text = reports_PATH + 'source_scan_' + data_string + '.txt'
with io.open(report_file_path_text, 'w', encoding='utf-8') as f:
    for showExtracted in testsListFinal:
        new_string = getRelativeBaseFolder(showExtracted[0])

        prepare_hash = new_string+'\\'+showExtracted[1]+'\\'+showExtracted[2]+'.php' + ' | ' + showExtracted[1]+'_'+showExtracted[2]+' | test' + showExtracted[3]

        statusFound = 'already exists'
        if(prepare_hash not in hashedTests):
            statusFound = 'new'
            if DO_CREATE_TEST_STRUCTURE == True :
                createTestScaffold(showExtracted)
    
            print prepare_hash

        f.write(unicode('File:\t'   + showExtracted[0] + '\n'))
        f.write(unicode('Class:\t'  + showExtracted[1] + '\n'))
        f.write(unicode('Method:\t' + showExtracted[2] + '\n'))
        f.write(unicode('Status Test:\t'   + statusFound + '\n')) # to be completed when scanning existing files
        f.write(unicode('Test:\t'   + showExtracted[3] + '\n'))
        
        if showExtracted[4]!='' :
            f.write(unicode('Description:\t' + showExtracted[4] + '\n'))

        f.write(unicode('\n\n'))
        pass