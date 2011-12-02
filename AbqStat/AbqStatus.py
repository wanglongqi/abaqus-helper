# -*- coding:utf-8 -*-
'''
Created on 2011-9-30

@author: WLQ
'''
import sys,os
from PyQt4 import QtCore as QC
from PyQt4 import QtGui as QG
def tail( f, window=32):
    BUFSIZE = 4096
    f.seek(0, 2)
    bytes = f.tell()
    size = window
    block = -1
    data = []
    while size > 0 and bytes > 0:
        if (bytes - BUFSIZE > 0):
            f.seek(block*BUFSIZE, 2)
            data.append(f.read(BUFSIZE))
        else:
            f.seek(0,0)
            data.append(f.read(bytes))
        linesFound = data[-1].count('\n')
        size -= linesFound
        bytes -= BUFSIZE
        block -= 1
    return '\n'.join(''.join(data).splitlines()[-window:])

class Form(QG.QDialog):  
    def __init__(self,parent=None):
        super(Form, self).__init__(parent)
        self.file=None
        self.setWindowIcon(QG.QIcon('stat.png'))
        self.fl=QG.QTextEdit()
        pl=self.fl.palette()
        pl.setColor(pl.Base,QG.QColor(0,0,0))
        self.fl.setPalette(pl)
        self.fl.setCurrentFont(QG.QFont("Courier New",16,QG.QFont.Bold))
        self.fl.setTextColor(QG.QColor(255,255,0))
        self.fl.setText(u'''
        
        
        
        
        ____________________________________________________________
                                                                       
                                                                       
            本程序可以用来查看Abaqus、ANSYS或者一般文本文件的写入情况。
                                                                       
            本程序的目的在于给出一个可以替代Abaqus Monitor的程序，     
            那个程序实在太容易把Abaqus内核弄得不响应了。               
                                                                       
            Open an ABQ Status file to see the Status.                 
                                                                       
                                                  WLQ                 
                                               2011/9/30               
                                                                       
                      ________________________________                 
                     |                                |                
                     |Best wishes for all good people!|                
                     |________________________________|                
                                                                       
       ____________________________________________________________
            
            
        
    ''')
        self.f=QG.QPushButton('Click here to Open the status file.', self)
        grid=QG.QGridLayout()
        grid.addWidget(self.fl,1,0)
        grid.addWidget(self.f,0,0)
        self.setLayout(grid)
        self.setWindowTitle('ABQStatus')
        self.setGeometry(100,100,1024,800)
        self.connect(self.f,QC.SIGNAL('clicked()'),self.showDialog)
        self.timer = QC.QBasicTimer()
        
    def timerEvent(self, e):
        self.fl.setText(tail(self.file))
            
    def showDialog(self):
        self.timer.stop()
        if self.file ==None:
            filename = QG.QFileDialog.getOpenFileName(self, 'Open file',
                    'D:','Abaqus(*.sta);;ANSYS(*.mntr,*.log);;ALL Files(*.*)')
        else:
            dir=os.path.dirname(str(self.file.name))
            filename = QG.QFileDialog.getOpenFileName(self, 'Open file',
                    dir,'Abaqus(*.sta);;ANSYS(*.mntr,*.log);;ALL Files(*.*)')
        self.setWindowTitle('ABQStatus '+filename[:str(filename).rfind('.')])
        self.file=open(filename)
        self.fl.setText(tail(self.file))
        self.timer.start(100,self)
        
app = QG.QApplication(sys.argv)
form = Form()
form.show()
app.exec_()