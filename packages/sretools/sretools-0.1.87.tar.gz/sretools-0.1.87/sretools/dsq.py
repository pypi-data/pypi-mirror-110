import sys
import argparse
import os
import json
import yaml
import xmltodict
import re
import traceback
import time
import random
import string
from sretools import SimpleTable
from sretools import Input
from sretools import prepare_table
from collections import deque
from collections import defaultdict
from types import FunctionType

__INTERACTIVE=False

def _j(ds) :
    return json.dumps(ds,indent=2,sort_keys=True)
def _x(ds) :
    import xml.dom.minidom as dom
    import dicttoxml
    xmlstr = dicttoxml.dicttoxml(ds).decode()
    xml = dom.parseString(xmlstr)
    return xml.toprettyxml()
def _y(ds) :
    return yaml.dump(ds,default_flow_style=False,explicit_start=True, explicit_end=False)
def _l(ds) :
    if type(ds) in [list,set,tuple] :
        for i in ds :
            print(i)
    if type(ds) is dict :
        l=len(ds)+2
        fmt="{:"+str(l)+"} = {}"
        for i,v in ds.items() :
            print(fmt.format("."+i,v))
def _lf(fn) :
    return open(fn,"r").read()
def _lj(fn) :
    return json.loads(_lf(fn))
def _ly(fn) :
    return yaml.safe_load(_lf(fn))
def _ef(fn) :
    exec(_lf(fn))
def _l2t(xjson,header=None) :
    data,header=prepare_table(xjson,header)
    return SimpleTable(data=data,header=header)
def _t(data=list(),header=None,dataonly=False) :
    return SimpleTable(data=data,header=header,noheader=dataonly)
def _flat(ds,last="."):
    res = ""
    if type(ds) is dict :
        for k,v in ds.items() :
            if type(v) in [dict,list] :
                res += _flat(v,last+"."+k) 
            else :
                res += last+"."+k+" = "+str(v) + "\n"
    if type(ds) is list :
        for i,v in enumerate(ds) :
            if type(v) in [dict,list] :
                res += _flat(v,last+"["+str(i)+"]") 
            else :
                res += last+"["+str(i)+"] = " + str(v) + "\n"
    return res

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="code", nargs='?', default="_", help="code to compile. may be a file.")
    parser.add_argument("-f", "--infile", dest="infile", help="input file")
    parser.add_argument("-t", "--srctype", dest="srctype", default="JSON", help="JSON,YAML or XML")
    parser.add_argument("-i", "--indent", dest="indent", default=4, help="how many spaces for indent. default 4.")
    parser.add_argument("-m", "--modules", dest="modules", help="import modules.")
    parser.add_argument("-K", "--keys", dest="keys_included", help="only keep these keys.")
    parser.add_argument("-E", "--nokeys", dest="keys_excluded", help="these keys should be excluded.")
    parser.add_argument("-F", "--functionize", dest="func", action="store_true", default=False, help="wrap code into an internal function",)
    parser.add_argument("-s", "--rawstr", dest="rawstr", action="store_true", default=False, help="output raw stings for easy grep",)
    parser.add_argument("-e", "--exec", dest="exec", action="store_true", default=False, help="execute code block. all non value display purpose",)
    parser.add_argument("-I", "--interactive", dest="interactive", action="store_true", default=False, help="interactive mode",)
    parser.add_argument("-c", "--compact", dest="compact", action="store_true", default=False, help="dump data structure in compact mode",)
    parser.add_argument("-X", "--debug", dest="debug", action="count", default=False, help="debug mode",)
    _x_args = parser.parse_args()

    if _x_args.debug >=2 :
        print("args = ",_x_args)

    if _x_args.keys_included :
        _xset_keys_included = set([w.lower() for w in _x_args.keys_included.split(",") if w])
    else :
        _xset_keys_included = None
    if _x_args.keys_excluded :
        _xset_keys_excluded = set([w.lower() for w in _x_args.keys_excluded.split(",") if w])
    else :
        _xset_keys_excluded = None

    def cutkeys(ds) :
        if not _xset_keys_included and not _xset_keys_excluded :
            return ds
        if type(ds) is dict :
            ds = {k:v for k, v in ds.items() if (_xset_keys_included and k.lower() in _xset_keys_included ) or (_xset_keys_excluded and k.lower() not in _xset_keys_excluded)}
            for k,v in ds.items() :
                ds[k] = cutkeys(v)
        if type(ds) is list :
            for i,v in enumerate(ds) :
                if type(v) in [dict,list] :
                    ds[i] = cutkeys(v)
        return ds

    def collect_keys(ds, dt) :
        if type(ds) is dict :
            for k, v in ds.items() :
                dt[k.lower()].add(k)
                collect_keys(v,dt)
        elif type(ds) in [list,tuple] :
            for i in ds :
                collect_keys(i,dt)
        else :
            pass

    def show_result(res) :
        if not res :
           return
        if type(res) is str :
            print(res)
        else :
            res = cutkeys(res)
            if _x_args.rawstr :
                print(_flat(res),end="")
            else :
                try :
                    if _x_args.compact :
                        print(json.dumps(res))
                    else :
                        print(json.dumps(res,indent=2))
                except :
                    print(str(res))

    def dotexpand(_x_sin,keydt=None) :
        chgsin = _x_sin
        _x_m = re.search(r"(\w+|\]|\))(\.\w+|\.\\\w+)+",chgsin,re.DOTALL)
        res=""
        while _x_m :
            before = chgsin[:_x_m.start()]
            end = chgsin[_x_m.end():]
            chain = _x_m.group(0)
            newchain = ""
            words = chain.split(".") 
            for i,w in enumerate(words) :
                if w.startswith("\\") or (i==len(words)-1 and end.startswith("(")) :
                    nw = w.lstrip("\\")
                    newchain += "." + nw
                else :
                    nw = w.lower()
                    if nw in keydt and len(keydt[nw]) == 1 :
                        nw = list(keydt[nw])[0]
                        if _x_args.debug and w != nw :
                            print("# keyword replcement : {} -> {}".format(w,nw))
                    if newchain :
                        newchain += "['"+ nw + "']"
                    else :
                        newchain += nw
            res += before + newchain 
            chgsin = end
            _x_m = re.search(r"(\w+|\]|\))(\.\w+|\.\\\w+)+",chgsin,re.DOTALL)
        return res+chgsin

    if _x_args.infile:
        if not os.path.isfile(_x_args.infile):
            print("# {} not exists.".format(_x_args.infile))
        with open(_x_args.infile, "r") as f:
            INPUT = f.read()
    else:
        INPUT = sys.stdin.read()
    INPUT = INPUT.strip()
    if not INPUT :
        INPUT = json.dumps({})
    try :
       if _x_args.srctype.upper() == "JSON" :
            _ = json.loads(INPUT)
       elif _x_args.srctype.upper() == "YAML" :
            _ = yaml.safe_load(INPUT)
       elif _x_args.srctype.upper() == "XML" :
            _ = xmltodict.parse(INPUT)
       else :
        print("# unsupported file type.")
        return -1
    except :
        print("# invalid JSON/YAML/XML.")
        traceback.print_exc()
        return -1

    if _x_args.debug >= 2 :
        print("[dsq]$ data loaded.")
        print(json.dumps(_,indent=2))

    _x_key_dict = defaultdict(set)
    collect_keys(_,dt=_x_key_dict)
    if _x_args.debug >= 2 :
        print("# keys collected :", str(_x_key_dict))
        
    if _x_args.modules :
        for m in _x_args.modules.split(",")  :
            if m :
                m.strip()
                if m.startswith("from ") :
                    exec(m)
                else :
                    exec("import " + m)

    _x_dotkey = True
    if _x_args.interactive :
        __INTERACTIVE=True
        _x_input = Input(ps1="[dsq]$ ")
        _x_history = deque(maxlen=200)
        _x_cmd0=""
        _x_oldsin=""
        _x_block=False
        while True :
            _x_doeval=True
            res=""
            err=""
            #_x_sin = input("[dsq]$ ")
            _x_sin = _x_input.getline()
            if not _x_sin :
                continue
            if _x_sin.startswith("'''")  :
                if _x_block :
                    _x_sin = _x_oldsin 
                    _x_oldsin=""
                    _x_block=False
                    _x_doeval = False
                else :
                    _x_block = True
                    continue
            if _x_block :
                if _x_oldsin :
                    _x_oldsin += "\n" + _x_sin
                else :
                    _x_oldsin += _x_sin
                continue
            lastc =[int(ord(c)) for c in _x_sin][-1]
            if lastc and lastc in [65,66,67,68] : 
                _x_sin = "\\hist"
            if _x_sin in ["quit()","\\q"] :
                break
            if _x_sin in ["dotkey"] :
                _x_dotkey = True
                continue
            if _x_sin in ["nodotkey","no dotkey"] :
                _x_dotkey = False
                continue
            if _x_sin in ["\\hist","\\history"] :
                if not _x_history :
                    print("# no history found.")
                for i,cmd in enumerate(_x_history) :
                    print("# {:3} : {}".format(i,cmd))
                continue
            _x_m1 = re.match(r"\\r (\d+)",_x_sin) 
            _x_m2 = re.match(r"\\(\d+)",_x_sin) 
            if _x_m1 or _x_m2:
                if _x_m1 :
                    ix = int(_x_m1.group(1))
                if _x_m2 :
                    ix = int(_x_m2.group(1))
                if ix < len(_x_history) :
                    _x_sin = _x_history[ix]
                else :
                    continue
            _x_cmd0 = None
            if _x_dotkey and "." in _x_sin :
                _x_cmd0 = _x_sin
                _x_sin = dotexpand(_x_sin,_x_key_dict)
            try :
                if _x_cmd0 :
                    _x_history.append(_x_cmd0)
                elif not _x_sin.startswith("\\") :
                    _x_history.append(_x_sin)
                if _x_sin.startswith("\\") :
                    res = ""
                    err = "# command not recognized."
                else :
                    if re.search(r"^\s*\S+\s*=\s*\S*",_x_sin) :
                        _x_doeval=False
                    if re.match(r"for .*",_x_sin) or re.match(r"while .*",_x_sin) :
                        _x_doeval=False
                    try :
                        if _x_doeval :
                            if _x_args.debug:
                                print("# eval : {}".format(_x_sin))
                            res = eval(_x_sin)
                            show_result(res)
                        else :
                            if _x_args.debug:
                                print("# exec : \n{}".format(_x_sin))
                            res = exec(_x_sin)
                            show_result(res)
                    except :
                        print(traceback.format_exc())
            except :
                err = traceback.format_exc()
                if err :
                    print(err)
                continue
            time.sleep(0.1)
        os.system("reset")
        os.system("clear")
        return 0

    if os.path.isfile(_x_args.code) :
        code = open(_x_args.code,"r").read()
    else :
        code = _x_args.code

    if _x_args.func :
        fname = "".join([random.choice(string.ascii_letters) for _ in range(20)])
        newcode = ""
        if _x_args.modules :
            for m in _x_args.modules.split(",")  :
                if m :
                    m.strip()
                    if m.startswith("from ") :
                        newcode += m + "\n"
                    else :
                        newcode += "import " + m + "\n"
        newcode += "def {}(_) :\n".format(fname)
        code = code.replace("\\n","\n")
        for ln in code.splitlines() :
            ln = ln.rstrip()
            newcode += " "*(int(_x_args.indent)) + ln + "\n"
        code = dotexpand(newcode,_x_key_dict)
        if _x_args.debug :
            print("# code to compile :")
            print(code)
        xcode = compile(code,"<string>","exec")
        cobj = None
        for c in xcode.co_consts :
            if c and type(c) not in [str,int,tuple] :
                cobj = c
                break
        if not cobj :
            print("# no code object found.")
            sys.exit(-1)
    
        xfunc = FunctionType(cobj, globals())
        print(xfunc(_))
        return(0)

    if _x_args.exec :
        code = dotexpand(code,_x_key_dict)
        if _x_args.debug:
            print("# exec : {}".format(code))
        exec(code)
    else :
        code = dotexpand(code,_x_key_dict)
        if _x_args.debug:
            print("# eval : {}".format(code))
        res = eval(code)
        show_result(res)

if __name__ == "__main__" :
    main()
