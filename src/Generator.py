# The MIT License (MIT)
#
# Copyright (c) 2014 Bogdan Anton
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json
import re

class Generator():

    dataJSON = {}
    testsNeeded = []

    config = {
        'source': 'source/',
        'tests': 'tests/',
        'json': 'index_folders.json',
        'testsnamespace': 'tests',
        'todounit': False,
        'classattributes': False,
        'force_overwrite': False
    }
    # force_overwrite should only be set to true to overwrite the test files

    def getConfig(self, key):
        return self.config[key]

    def setConfig(self, key, value):
        self.config[key] = value
        return True

    def run(self):
        self.loadJSON()
        self.prepareMethods()
        self.makePaths()
        self.makeMethodFiles()

        if (self.getConfig("todounit")):
            self.makeTodounitTests()

        if (self.getConfig("classattributes")):
            self.makeClassAttributesTests()

        # print(self.testsNeeded)
        print("\nDone.\n")
        pass

    def loadJSON(self):
        json_data = open(self.getConfig('json'))
        self.dataJSON = json.load(json_data)
        json_data.close()
        pass

    def prepareMethods(self):
        for entry in self.dataJSON:
            file_path   = str(entry['file'].replace(self.getConfig('source'), ''))
            file_path = file_path.replace('\\\\', '\\').replace('\\', '/').split('/')

            class_name  = str(entry['class'])
            if (class_name == ""):
                filename = file_path[-1].split('.')
                del filename[-1]
                class_name = re.sub('[^0-9a-zA-Z_]+', '', '_'.join(filename))

            del file_path[-1]

            is_method = False
            static = False
            access = 'public'

            if (entry['item'] == 'class_method'):
                is_method = True
                method_name = str(entry['name'])
                static = bool(str(entry['isStatic']))
                access = str(entry['access']).replace('_', '')

            else:
                method_name = False

            # append todounit plaintext comments (if needed and found)
            todounit = []
            if (self.getConfig('todounit')):
                todounit_found = re.findall(r"\@todounit (.*)", entry['docblock'])
                if (todounit_found):
                    for todounit_entry in todounit_found:
                        todounit_entry = str(todounit_entry).replace('@todounit ', '').strip()
                        todounit.append(todounit_entry)
                        pass

            file_path.append(class_name)
            self.testsNeeded.append({'structure': file_path, 'class': class_name, 'method': method_name, 'access': access, 'static': static, 'is_method': is_method, 'todounit': todounit})

            pass
        pass

    def makePaths(self):
        separator = os.path.sep
        paths = []

        for entry in self.testsNeeded:
            paths.append(self.getFullpath(entry['structure'], separator))
            pass

        paths = list(set(paths))

        for entry in paths:
            self.makePath(entry)
            pass

    def makePath(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            pass

    def getFullpath(self, splits, separator):
        return self.getConfig('tests') + separator + separator.join(splits)

    def makeMethodFiles(self):
        for entry in self.testsNeeded:
            if (entry['method']):
                self.makeMethodFile(entry)
            pass

    def makeMethodFile(self, entry):
        separator = os.path.sep
        namespacePrefix = self.getConfig('testsnamespace')
        
        path = self.getFullpath(entry['structure'], separator) + separator + entry['method'] + 'Test.php'
        fileNamespace = namespacePrefix + "\\" + "\\".join(entry['structure'])
        
        # will check if the file exists and will not destroy it if it exists, as long as the force_overwrite flag is set to False
        if (self.getConfig('force_overwrite') or (not os.path.isfile(path))):
            classDocblock = ""

            if (entry['is_method']):
                methodType = '->'
                if (entry['static']):
                    methodType = '::'
                classDocblock = """\n/**\n * Covers the """ + entry['access'] + """ method """ + entry['class'] + methodType + entry['method'] + """()\n */"""

            fileContents = """<?php
namespace """ +  fileNamespace + """;
""" + classDocblock + """
class """ + entry['method'] + """ extends \PHPUnit_Framework_TestCase
{
	public function testIncomplete()
	{
		$this->markTestIncomplete(" ... ");
	}
}
"""
            with open(path, 'w') as file:
                file.write(fileContents)
        pass


    def makeTodounitTests(self):
        for entry in self.testsNeeded:
            if (entry['method'] and entry['todounit']):
                self.makeMethodFile(entry) # will not override existing files
                
                for todounit_entry in entry['todounit']:
                    todounit_entry = re.sub('[^0-9a-zA-Z_ ]+', '', todounit_entry)

                    testTitle = todounit_entry.title().replace(' ', '')
                    testContent = """\n   /**
	 * """ + todounit_entry + """
	 */
	public function test""" + testTitle + """()
	{
		$this->markTestIncomplete(" ... ");
	}
"""
                    separator = os.path.sep
                    path = self.getFullpath(entry['structure'], separator) + separator + entry['method'] + 'Test.php'
                    
                    if (self.insertPrependMethod(path, testContent, 'test'+testTitle)):
                        print("Added test '" + todounit_entry + "' (test" + testTitle + ") in " + entry['method'] + 'Test.php')

                    pass
                pass
        pass
    
    def insertPrependMethod(self, filepath, content, testname):
        isMultilineComment = False
        previousChar = ""
        previousWord = ""
        listenForClassOpen = False
        wasInserted = False
        file_content = ""

        file = open(filepath, 'r')
        for line in file:

            if (line.find(testname + '()') > 0):
                return False

            for char in line:
                file_content += char

                if ((char == '*') and (previousChar == '/')):
                    isMultilineComment = True
                    previousWord = ""

                if (not isMultilineComment):
                    if ((previousWord == 'class') and (char == " ")):
                        listenForClassOpen = True

                    if ((char == " ") or (char == ";")):
                        previousWord = ""

                    if ((not wasInserted) and (listenForClassOpen) and (char == "{")):
                        wasInserted = True
                        file_content += content

                    if ((char != " ") and (char != "\t") and (char != "\n") and (char.isalpha())):
                        previousWord += char

                if ((char == '/') and (previousChar == '*')):
                    isMultilineComment = False
                    previousWord = ""

                previousChar = char

        if (wasInserted):
            with open(filepath, 'w') as file:
                file.write(file_content)
            return True

        return False
        pass

    def makeClassAttributesTests(self):
        for entry in self.dataJSON:
            if (entry['item'] == 'class_attribute'):

                file_path   = str(entry['file'].replace(self.getConfig('source'), ''))
                file_path = file_path.replace('\\\\', '\\').replace('\\', '/').split('/')

                class_name  = str(entry['class'])
                if (class_name == ""):
                    filename = file_path[-1].split('.')
                    del filename[-1]
                    class_name = re.sub('[^0-9a-zA-Z_]+', '', '_'.join(filename))

                del file_path[-1]
                file_path.append(class_name)
                entry['structure'] = file_path
                entry['method'] = '___attributes___'
                entry['is_method'] = False

                self.makeMethodFile(entry) # will not override existing files

                testTitleExtended = ""
                if (entry['static']):
                    testTitleExtended = "static "

                testTitleExtended += entry['access'] + " "
                attributeName = entry['name'].replace('$', '')

                testTitleExtended += "attribute " + attributeName + " is defined"
                testTitle = testTitleExtended.title().replace(' ', '')

                if (entry['static']):
                    assertText = """$this->assertClassHasStaticAttribute('""" + entry['name'].replace('$', '') + """', '\\""" + entry['namespace'] + """');"""
                else:
                    assertText = """$this->assertClassHasAttribute('""" + entry['name'].replace('$', '') + """', '\\""" + entry['namespace'] + """');"""

                testContent = """\n   /**
     * """ + testTitleExtended + """
     */
    public function test""" + testTitle + """()
    {
        """ + assertText + """
    }
"""
                separator = os.path.sep
                path = self.getFullpath(entry['structure'], separator) + separator + entry['method'] + 'Test.php'
                
                if (self.insertPrependMethod(path, testContent, 'test'+testTitle)):
                    print("Added attribute test '" + testTitleExtended + "' (test" + testTitle + ") in " + entry['method'] + 'Test.php')
            pass
        pass
