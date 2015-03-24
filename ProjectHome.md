![http://abaqus-helper.googlecode.com/svn/trunk/AbqHelper.png](http://abaqus-helper.googlecode.com/svn/trunk/AbqHelper.png)

Abaqus-Helper project contains several scripts I write while using Abaqus.

AbqStat, fullname is AbqStatus, provided an alternative for Abaqus buildin job monitor, which made Abaqus Kernel died when some not so large problem is solved. It is simply read Abaqus sta file, and follow it while calculation. This can be simply done by 'tail -f', if you are an unix like user.

[txtgen](txtgen.md) is a little script for python script generate. This script can be replaced if you want to use find/replace function all the time. If you use the module, I suggest you do two things:
  1. make a user defined filetype, like _.rt_
  1. make a shortcut to new a template of the filetype.

[dBzWriter](dBzWriter.md) is a module that reads scalar data and write the data into odb files. The script can be easily adopted to import vector or tensor data into odb files.

If you interested in this project, you may also interested in http://code.google.com/p/viblab, which contains some modules about vibration signal processing.