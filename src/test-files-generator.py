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

"""
Usage: test-files-generator --source [PATH] --tests [PATH] --json [PATH/index_folders.json] --testnamespace [namespace prefix] (--todounit yes) (--classattributes yes)

Arguments:
    --source              The path to the PHP project's source folder.
    --tests               The path to the PHP project's tests folder.
    --json                PHP-CodeGraph index_folders.json file. Check out http://github.com/bogdananton/PHP-CodeGraph
    --testnamespace       (optional) Namespace prefix for test files. Default: "tests". Can be "tests\phpunit".
    --todounit            (optional) Set this flag to "yes" to enable scanning for @todounit markers in docblocks and appending them as test methods. Default: disabled.
    --classattributes     (optional) Set this flag to "yes" to generate basic tests that check that the class attributes exist. Default: disabled.

"""

import sys
import optparse
from Generator import Generator

# boot-up
parser = optparse.OptionParser(version = "1.0.0rc2", usage = __doc__.strip())
parser.add_option('--source')
parser.add_option('--tests')
parser.add_option('--json')
parser.add_option('--testnamespace')
parser.add_option('--todounit')
parser.add_option('--classattributes')

options, args = parser.parse_args()

if not options.source or not options.tests or not options.json:
    sys.stdout.write(__doc__)
    sys.exit()

worker = Generator()
worker.setConfig('source', options.source)
worker.setConfig('tests', options.tests)
worker.setConfig('json', options.json)

if (options.testnamespace):
    worker.setConfig('testnamespace', options.testnamespace)

if (options.todounit) and (options.todounit == 'yes'):
        worker.setConfig('todounit', True)

if (options.classattributes) and (options.classattributes == 'yes'):
    worker.setConfig('classattributes', True)

worker.run()
