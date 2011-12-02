# -*- coding:utf-8 -*-
'''
Created on 2011-11-17

@author: WLQ
'''

def txtgen(tem, words):
    'Replace Templates.'
    items = tem.split('$')
    for field in range(int(len(items) / 2)):
        name = items[field * 2 + 1]
        if name != '':
            items[field * 2 + 1] = words[name]
    line = ''
    for i in items:
        line = line + unicode(i)
    return line

def outputtoconsole(text):
    print text

def outputtofile(text,file):
    fid=open(file,'w+')
    fid.write(text)
    fid.close()

def outputtoclip(text):
    import win32clipboard, win32con
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, unicode(text))
    win32clipboard.CloseClipboard()
    
def txtgendemo():
    'print a demo file'
    return """from txtgen import txtgen,outputtoconsole,outputtoclip,outputtofile
template='''Data$index$=$index$
'''
content=''
for index in range(100):
    words={'index':index}
    content=content+txtgen(template,words)

outputtoconsole(content)
"""

