# sretools
A collection of SRE command line tools

## SSH tool
sretools-ssh        ssh command tool with expect integration.  run remote command, ship and run package on remote server, etc.

## expect
sretools-expect    command line expect tool.   help SRE to "expect' interactive applications in a very easy way.

## structure data 
[sretools-dsq](/examples/sretools-dsq.md) jq/jello like query tools with interactive mode. \
sretools-json2html   format JSON from file or pipe to HTML tables. \
sretools-json2yaml   format JSON from file or pipe \
sretools-yaml2json   format YAML from file or pipe \
sretools-yaml2html   format YAML from file or pipe 

## concole
[sretools-table-format](/examples/sretools-table-format.md)  console table formatting tool.  pipe, CSV, etc. support UNICODE.

## database client
[sretools-dbx](/examples/sretools-dbx.md)        generic JDBC calls. dump query in good table format.  open JDBC access to bash level.


## misc
<ul>
<li>sretools-nonascii    scan FS, files for non-ascii characters.  will help resovle issues caused by "invisiable" characters.</li>
</ul>


## Classes
<ul>
<li>LE   expect class for develp sretools-ltexpect alike tools.</li>
<li>SimpleTable    console formatting table supporting wide chacaters.</li>
<li>JsonConverter  convert JSON str or dict/list object to HTML or YAML.</li>
</ul>
