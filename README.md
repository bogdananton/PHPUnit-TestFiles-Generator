PHPUnit file / folder structure generator. Works with [the CodeGraph app](https://github.com/bogdananton/PHP-CodeGraph)'s JSON output.

**Usage**

Generate the PHP-CodeGraph JSON file. Use the following command to generate the folders and files:
```
phpcg --source /projects/PHPUnit-TestFiles-Generator/demo/source/ --log /projects/PHPUnit-TestFiles-Generator/demo/
```

Use the following command to scan for @todounit tags and generate/append the test methods (if not already generated):
```
test-files-generator --source /projects/PHPUnit-TestFiles-Generator/demo/source/ --tests /projects/PHPUnit-TestFiles-Generator/demo/tests/ --json /projects/PHPUnit-TestFiles-Generator/demo/index_folders.json --todounit yes --classattributes yes
```

**Features**

* Generates folder and file structure using the source code's folders / classes / methods.
* Creates blank test methods using the plain text used in methods' @todounit docblock tags if the --todounit option is set and has the value "yes"
* Creates basic tests for each class attribute, if the --classattributes option is set and has the value "yes"

**Conventions**

* Each method will have its own file, named [method_name]Test.php and containing a single class with the name [method_name]
* All methods found in a class will be grouped in a folder having the same name as the class.
* The class' path will be mirrored for test files

If the class is `[PROJECT_PATH]/source/lib/Stock/Inventory.php` then the files will be added in the `[PROJECT_PATH]/tests/lib/Stock/Inventory/`. The source and tests paths can be overridden using the arguments when launching the application.-