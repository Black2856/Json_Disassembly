import sys , os
import tkinter, tkinter.filedialog, tkinter.messagebox
import json

def songExtract(noteJson):
    ret = []
    try:
        for i in noteJson['song']['notes']:
            li = []
            if ('lengthInSteps' in i) == True:
                li.append(i['lengthInSteps'])
            else:
                li.append(-1)
            if ('mustHitSection' in i) == True:
                li.append(i['mustHitSection'])
            else:
                li.append(-1)
            if ('bpm' in i) == True:
                li.append(i['bpm'])
            else:
                li.append(-1)
            ret.append(li)
    except:
        tkinter.messagebox.showerror('error','This file isnt correct!')
        sys.exit()
    return ret

def noteExtract(noteJson,trueMHS: bool,falseMHS: bool):
    ret = []
    try:
        for i in noteJson['song']['notes']:
            if i['mustHitSection'] == True:
                for j in i['sectionNotes']:
                    if trueMHS == True:
                        if(0 <= j[1] and j[1] <= 3):
                            ret.append(j)
                    else:
                        if(4 <= j[1] and j[1] <= 7):
                            j[1] = j[1] - 4
                            ret.append(j)
            else:
                for j in i['sectionNotes']:
                    if falseMHS == True:
                        if(0 <= j[1] and j[1] <= 3):
                            ret.append(j)
                    else:
                        if(4 <= j[1] and j[1] <= 7):
                            j[1] = j[1] - 4
                            ret.append(j)
    except:
        tkinter.messagebox.showerror('error','This file isnt correct!')
        sys.exit()
    return ret

def writeInfo(fp,noteList):
    for i in noteList:
        fp.write(str(round(i[0]))+',')
        fp.write(str(round(i[1]))+',')
        fp.write(str(round(i[2]))+':')

# ファイル選択ダイアログの表示
root = tkinter.Tk()
root.withdraw()
fTyp = [("","Json")]
iDir = os.path.abspath(os.path.dirname(__file__))
path = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)

#ファイルのオープン及びnotemapか確認
try:
    fpIn = open(path,'r')
    noteJson = json.load(fpIn)
except json.JSONDecodeError:
    tkinter.messagebox.showerror('error','This file isnt json format!')
    sys.exit()
except:
    sys.exit()

outputName = ['_scratch.txt']
try:
    bpm = noteJson['song']['bpm']
except:
    tkinter.messagebox.showerror('error','This file isnt notes data!')
    sys.exit()

#書き出し
fpOut = open(os.path.splitext(os.path.basename(path))[0]+outputName[0],'w')

fpOut.write('songInfo:\n')
noteList = []
noteList = songExtract(noteJson)
noteList[0][2] = bpm
writeInfo(fpOut,noteList)

fpOut.write('\n\nplayer1(bf):\n')
noteList = []
noteList = noteExtract(noteJson,True,False)
noteList.sort(key=lambda x:x[0])
writeInfo(fpOut,noteList)

fpOut.write('\n\nplayer2(enemy):\n')
noteList = []
noteList = noteExtract(noteJson,False,True)
noteList.sort(key=lambda x:x[0])
writeInfo(fpOut,noteList)

fpOut.write('\n\nboth1:\n')
noteList = []
noteList = noteExtract(noteJson,True,True)
noteList.sort(key=lambda x:x[0])
writeInfo(fpOut,noteList)

#fpOut.write('\n\nboth2:\n')
#noteList = []
#noteList = noteExtract(noteJson,False,False)
#noteList.sort(key=lambda x:x[0])
#writeInfo(fpOut,noteList)

fpOut.write('\n\n[noteDataPattern]noteTick,noteLane,noteLength: ...')
fpOut.write('\n[songDataPattern]lengthInSteps,mustHitSection,bpm: ...')

fpIn.close()