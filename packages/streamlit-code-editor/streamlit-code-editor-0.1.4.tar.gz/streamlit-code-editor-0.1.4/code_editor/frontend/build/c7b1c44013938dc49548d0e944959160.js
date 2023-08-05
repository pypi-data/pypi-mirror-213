ace.define("ace/snippets/python.snippets",["require","exports","module"],(function(t,n,e){e.exports='snippet #!\n\t#!/usr/bin/env python\nsnippet imp\n\timport ${1:module}\nsnippet from\n\tfrom ${1:package} import ${2:module}\n# Module Docstring\nsnippet docs\n\t\'\'\'\n\tFile: ${1:FILENAME:file_name}\n\tAuthor: ${2:author}\n\tDescription: ${3}\n\t\'\'\'\nsnippet wh\n\twhile ${1:condition}:\n\t\t${2:# TODO: write code...}\n# dowh - does the same as do...while in other languages\nsnippet dowh\n\twhile True:\n\t\t${1:# TODO: write code...}\n\t\tif ${2:condition}:\n\t\t\tbreak\nsnippet with\n\twith ${1:expr} as ${2:var}:\n\t\t${3:# TODO: write code...}\n# New Class\nsnippet cl\n\tclass ${1:ClassName}(${2:object}):\n\t\t"""${3:docstring for $1}"""\n\t\tdef __init__(self, ${4:arg}):\n\t\t\t${5:super($1, self).__init__()}\n\t\t\tself.$4 = $4\n\t\t\t${6}\n# New Function\nsnippet def\n\tdef ${1:fname}(${2:`indent(\'.\') ? \'self\' : \'\'`}):\n\t\t"""${3:docstring for $1}"""\n\t\t${4:# TODO: write code...}\nsnippet deff\n\tdef ${1:fname}(${2:`indent(\'.\') ? \'self\' : \'\'`}):\n\t\t${3:# TODO: write code...}\n# New Method\nsnippet defs\n\tdef ${1:mname}(self, ${2:arg}):\n\t\t${3:# TODO: write code...}\n# New Property\nsnippet property\n\tdef ${1:foo}():\n\t\tdoc = "${2:The $1 property.}"\n\t\tdef fget(self):\n\t\t\t${3:return self._$1}\n\t\tdef fset(self, value):\n\t\t\t${4:self._$1 = value}\n# Ifs\nsnippet if\n\tif ${1:condition}:\n\t\t${2:# TODO: write code...}\nsnippet el\n\telse:\n\t\t${1:# TODO: write code...}\nsnippet ei\n\telif ${1:condition}:\n\t\t${2:# TODO: write code...}\n# For\nsnippet for\n\tfor ${1:item} in ${2:items}:\n\t\t${3:# TODO: write code...}\n# Encodes\nsnippet cutf8\n\t# -*- coding: utf-8 -*-\nsnippet clatin1\n\t# -*- coding: latin-1 -*-\nsnippet cascii\n\t# -*- coding: ascii -*-\n# Lambda\nsnippet ld\n\t${1:var} = lambda ${2:vars} : ${3:action}\nsnippet .\n\tself.\nsnippet try Try/Except\n\ttry:\n\t\t${1:# TODO: write code...}\n\texcept ${2:Exception}, ${3:e}:\n\t\t${4:raise $3}\nsnippet try Try/Except/Else\n\ttry:\n\t\t${1:# TODO: write code...}\n\texcept ${2:Exception}, ${3:e}:\n\t\t${4:raise $3}\n\telse:\n\t\t${5:# TODO: write code...}\nsnippet try Try/Except/Finally\n\ttry:\n\t\t${1:# TODO: write code...}\n\texcept ${2:Exception}, ${3:e}:\n\t\t${4:raise $3}\n\tfinally:\n\t\t${5:# TODO: write code...}\nsnippet try Try/Except/Else/Finally\n\ttry:\n\t\t${1:# TODO: write code...}\n\texcept ${2:Exception}, ${3:e}:\n\t\t${4:raise $3}\n\telse:\n\t\t${5:# TODO: write code...}\n\tfinally:\n\t\t${6:# TODO: write code...}\n# if __name__ == \'__main__\':\nsnippet ifmain\n\tif __name__ == \'__main__\':\n\t\t${1:main()}\n# __magic__\nsnippet _\n\t__${1:init}__${2}\n# python debugger (pdb)\nsnippet pdb\n\timport pdb; pdb.set_trace()\n# ipython debugger (ipdb)\nsnippet ipdb\n\timport ipdb; ipdb.set_trace()\n# ipython debugger (pdbbb)\nsnippet pdbbb\n\timport pdbpp; pdbpp.set_trace()\nsnippet pprint\n\timport pprint; pprint.pprint(${1})${2}\nsnippet "\n\t"""\n\t${1:doc}\n\t"""\n# test function/method\nsnippet test\n\tdef test_${1:description}(${2:self}):\n\t\t${3:# TODO: write code...}\n# test case\nsnippet testcase\n\tclass ${1:ExampleCase}(unittest.TestCase):\n\t\t\n\t\tdef test_${2:description}(self):\n\t\t\t${3:# TODO: write code...}\nsnippet fut\n\tfrom __future__ import ${1}\n#getopt\nsnippet getopt\n\ttry:\n\t\t# Short option syntax: "hv:"\n\t\t# Long option syntax: "help" or "verbose="\n\t\topts, args = getopt.getopt(sys.argv[1:], "${1:short_options}", [${2:long_options}])\n\t\n\texcept getopt.GetoptError, err:\n\t\t# Print debug info\n\t\tprint str(err)\n\t\t${3:error_action}\n\n\tfor option, argument in opts:\n\t\tif option in ("-h", "--help"):\n\t\t\t${4}\n\t\telif option in ("-v", "--verbose"):\n\t\t\tverbose = argument\n'})),ace.define("ace/snippets/python",["require","exports","module","ace/snippets/python.snippets"],(function(t,n,e){"use strict";n.snippetText=t("./python.snippets"),n.scope="python"})),ace.require(["ace/snippets/python"],(function(t){"object"==typeof module&&"object"==typeof exports&&module&&(module.exports=t)}));