# -*- coding:utf-8 -*-
'''
Created on 2011-12-18

读入数据文件，将其显示在现有的ODB里，数据文件格式为：

节点编号 Z振级

配置文件中应有：
odbfile=ODB文件的路径
instance=instance的名称
step=插入数据的计算步
frame=frame的帧数
filename=数据文件文件名

@author: WLQ
'''

#处理输入文件
def ParseZdb(filename):
    label=[]
    zdb=[]
    for line in open(filename):
        tmp=line.split()
        if len(tmp)==2:
            label.append(int(tmp[0]))
            zdb.append((float(tmp[1]),))
    return (label,zdb)
        
from zdbcfg import *
from odbAccess import *
from abaqusConstants import *
#建立场变量
odb=session.openOdb(odbfile,readOnly=False)
myinstance=odb.rootAssembly.instances[instance]
#if frame in odb.steps[step].frames:
if frame <= len(odb.steps[step].frames):
    myframe=odb.steps[step].frames[frame]
else:
    myframe=odb.steps[step].Frame(incrementNumber=1,frameValue=0.0,description='dBz output frame.')

if 'dBz' in myframe.fieldOutputs.keys():
    myfield=myframe.fieldOutputs['dBz']
else:
    myfield=myframe.FieldOutput(name='dBz',description='dBz information.', type=SCALAR)
#写入值
label,zdb=ParseZdb(filename)    
myfield.addData(position=NODAL, instance=myinstance,labels=label,data=zdb)
odb.steps[step].setDefaultField(myfield)
odb.save()
odb.close()

