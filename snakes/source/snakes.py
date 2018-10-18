import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mBox
from tkinter import Menu
from tkinter.filedialog import *

def load_data_from_file(fname):
    data={}
    try:
        f = open(fname, 'r')
    except OSError as err:
        mBox.showerror("System error", "OS error:{0}".fromat(err))
    except:
            raise
    try:
        data = json.load(f)
    #except JSONDecodeError as err:
    except:
        mBox.showerror("File format error", "File Format Error")
        print("Unexpected error:", sys.exc_info()[0])

    f.close()
    return data

def store_data_to_file(fname, data):
    f = open(fname, 'w')
    json.dump(data, f)
    f.close()

def build_material_list(fname):
    data = load_file(fname, data)
    return data


def store_material_list(fname, mlist):
    store_data_to_file(fname, mlist)

def material_combo_sanity_check(combo, mlist):
    for x in combo:
        if x in mlist:
            pass
        else:
            return False
    return True

def sum_materials_weight(mCombo, mlist):
    wSum = 0;
    for x in mCombo:
        if x in mlist:
            wSum += mlist[x]['weight']
        else:
            return -1

    return wSum;

def calc_project_total_material_consumption(m2weight, m2):
    return m2weight*m2


def yview(*args):
    print(args)
    lbName.yview(*args)

def sset(*args):
    print(args)
    scrollbar.set(*args)


def _msgBox():
    mBox.showinfo('About', '  This is a simple tool for my old\nfriend!\n\n  Hopefully his business runs well!\n\nSincerely!\n\t\tShown830@outlook.com\n\t\tSep 2018')

def _quit():
    win.quit()
    win.destroy()
    exit()

def _open():
    global filePath
    global mList
    filePath = askopenfilename(filetypes=(("Material file", "*.material"),("Material file", "*.mtl")), title="打开原料文件")
    mList = {}
    lbName.delete(0, tk.END)
    mList = load_data_from_file(filePath)
    for k,v in mList.items():
        lbName.insert(tk.END, k+"        "+str(v['weight']))
    
    lbName.select_set(0)

def _notifySave():
    if changeStatus == False:
        return
    chose=mBox.askokcancel(title="保存", message="文件已改动,是否保存?")
    if chose == True:
        _save()


def _new():
    global filePath
    global mList
    _notifySave()
    filePath = asksaveasfilename(filetypes=(("Material file", "*.material"),("Material file", "*.mtl")), initialfile="default.material", title="新建原料文件")
    mList = {}
    lbName.delete(0, tk.END)

def _save():
    global filePath
    global mList
    store_material_list(filePath, mList)
    changeStatus=False

def _saveAs():
    global mList
    path = asksaveasfilename(filetypes=(("Material file", "*.material"),("Material file", "*.mtl")), title="原料文件另存为")
    store_material_list(path, mList)
    changeStatus=False

def _ladd():
    global win_add
    global categoryEntry
    global weightEntry
    win_add = tk.Tk()
    win_add.title("添加原料")
    #win_add.resizable(200, 200)
    win_add.minsize(400, 70)
    catgoryLb = tk.Label(win_add, text="类别", padx=5, pady=5)
    weightLb = tk.Label(win_add, text="克重", padx=5, pady=5)

    catgoryLb.grid(column=0, row=0, columnspan=2, sticky='W')
    weightLb.grid(column=1, row=0, columnspan=2, sticky='W')

    categoryEntry = tk.Entry(win_add)
    weightEntry = tk.Entry(win_add)
    categoryEntry.config(width=15)
    weightEntry.config(width=15)
    categoryEntry.grid(column=0, row=1, columnspan=1, sticky='W')
    weightEntry.grid(column=1, row=1, columnspan=1, sticky='W')

    bConfirm = ttk.Button(win_add, text="确定", command=_aConfirm)
    bCancel = ttk.Button(win_add, text="取消", command=_aCancel)
    bConfirm.grid(column=2, row=0)
    bCancel.grid(column=2, row=1)
    win_add.mainloop()

def _ldelete():
    global changeStatus
    for x in lbName.curselection():
        item = lbName.get(x)
        print(item)
        print(item[0])
        if item[0] in mList:
            del mlist[item[0]]
            changeStatus=True

        lbName.delete(x)
        lbName.select_set(x)

def _aConfirm():
    global changeStatus

    selected = lbName.curselection()
    if len(selected) == 0:
        loffs = 0
    else:
        loffs= lbName.curselection()[0]

    print(loffs)
    nm = categoryEntry.get()
    if len(nm) == 0:
        mBox.showerror('Error', "'类别'不能为空!!")
        return False
    wt = weightEntry.get()
    if len(wt) == 0:
        mBox.showerror('Error', "'克重'不能为空!!")
        return False
    lbName.insert(loffs, nm+"        "+wt)
    item = {}
    item['weight'] = int(wt)
    item['price'] = 0

    mList[nm]=item
    changeStatus = True
    win_add.quit()
    win_add.destroy()


def _aCancel():
    win_add.quit()
    win_add.destroy()

def _calc():
    global mList
    cmd = cmdEntry.get()
    if len(cmd) == 0:
        mBox.showerror("Error", "please enter a reasonable product combo")
    order = orderEntry.get()
    if len(order) == 0:
        mBox.showerror("Error", "please enter a reasonable order value")

    for k,v in mList.items():
        print(k)
        for p,pv in v.items():
            print(p, pv)

    check = material_combo_sanity_check(cmd, mList)
    if check == False:
        mBox.showerror("Error", "Product combo contains unrecognized value")
    wSum = sum_materials_weight(cmd, mList);
    print(cmd)
    print(order)
    print(wSum)
    wSum = wSum*int(order)
    wSum = wSum/1000
    mSumEntry.delete(0, tk.END)
    mSumEntry.insert(0, str(wSum))
    

if __name__ == "__main__":
    import sys
    global mList

    mList = { }

    global filePath
    filePath = "default.material"

#    for k,v in nList.items():
#        print(k)
#        for p,pv in v.items():
#            print(p, pv)



#    wSum = sum_materials_weight('BBAA', mList);

    global changeStatus    
    changeStatus=False


    win = tk.Tk()
    win.title("GUI")
    win.resizable(200, 200)
    btnFrame = tk.Frame(win, padx=20, pady=20)
    btnFrame.grid(column=2, row=1)
    buttonA = ttk.Button(btnFrame, text="添加原料类别", command=_ladd)
    buttonA.grid(column=2, row=0, padx=20, pady=20)
    bDelete = ttk.Button(btnFrame, text="删除原料类别", command=_ldelete)
    bDelete.grid(column=2, row=2, padx=20, pady=20)

    frame = tk.Frame(win, padx=20, pady=20)
    frame.grid(column=1, row=1)
    LabelCategory = ttk.Label(frame, text="类别        克重/平米")
    LabelCategory.grid(column=0, row=0, sticky='W')
    lbName = tk.Listbox(frame, exportselection=1, selectmode=tk.SINGLE, height=15, width=30)
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)

    lbName.grid(column = 0, row=1, sticky='W', columnspan=1, rowspan=1)
    #lbName.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    lbName.config(yscrollcommand=sset)

    scrollbar.config(command=yview)
    scrollbar.grid(column=3, row=1, rowspan=50, sticky='NS')
    #scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    menuBar = Menu(win)

    fileMenu = Menu(menuBar, tearoff=0)
    fileMenu.add_command(label="打开原料文件", command=_open)
    fileMenu.add_command(label="新建原料文件", command=_new)
    fileMenu.add_command(label="保存", command=_save)
    fileMenu.add_command(label="另存为", command=_saveAs)
    fileMenu.add_command(label="退出", command=_quit)
    menuBar.add_cascade(label="命令", menu=fileMenu)

    helpMenu = Menu(menuBar, tearoff=0)
    helpMenu.add_command(label="关于", command=_msgBox)
    menuBar.add_cascade(label="帮助", menu=helpMenu)

    inputFrame = tk.Frame(win, padx=20, pady=20)
    inputFrame.grid(column=1, row=2)
    cmdLb = tk.Label(inputFrame, text="产品组合", padx=5, pady=5)
    orderLb = tk.Label(inputFrame, text="订单总量(平米)", padx=5, pady=5)
    mSumLb = tk.Label(inputFrame, text="原料总量(Kg)", padx=5, pady=5)
    cmdLb.grid(column=0, row=0, sticky='W')
    orderLb.grid(column=0, row=2, sticky='W')
    mSumLb.grid(column=0, row=4, sticky='W')

    cmdEntry = tk.Entry(inputFrame, width=20)
    orderEntry = tk.Entry(inputFrame, width=20)
    mSumEntry = tk.Entry(inputFrame, width=20)
    cmdEntry.grid(column=0, row=1, sticky='W')
    orderEntry.grid(column=0, row=3, sticky='W')
    mSumEntry.grid(column=0, row=5, sticky='W')

    btnCalc = ttk.Button(inputFrame, text="计算", command=_calc)
    btnCalc.grid(column=2, row=3, padx=20, sticky='E')
    win.config(menu=menuBar)
    win.minsize(400, 400)

    win.mainloop()


