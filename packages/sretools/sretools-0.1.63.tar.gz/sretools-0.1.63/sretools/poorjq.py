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
from collections import deque
from types import FunctionType

def _x(ds) :
    return json.dumps(ds,indent=2,sort_keys=True)

def _y(ds) :
    return yaml.dump(ds,default_flow_style=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--infile", dest="infile", help="input file")
    parser.add_argument("-t", "--srctype", dest="srctype", default="JSON", help="JSON,YAML or XML")
    parser.add_argument("-c", "--code", dest="code", help="code to compile. may be a file.")
    parser.add_argument("-i", "--indent", dest="indent", default=4, help="how many spaces for indent. default 4.")
    parser.add_argument("-m", "--module", dest="module", help="import modules.")
    parser.add_argument("-F", "--functionize", dest="func", action="store_true", default=False, help="indicate code only use but doesn't define function(doc) ",)
    parser.add_argument("-I", "--interactive", dest="interactive", action="store_true", default=False, help="interactive mode",)
    parser.add_argument("-X", "--debug", dest="debug", action="store_true", default=False, help="debug mode",)
    args = parser.parse_args()

    if not (args.code or args.interactive) :
        print("# must specify code by -c in non-interactive mode.")
        sys.exit(-1)

    if args.infile:
        if not os.path.isfile(args.infile):
            print("# {} not exists.".format(args.infile))
        with open(args.infile, "r") as f:
            INPUT = f.read()
    else:
        INPUT = sys.stdin.read()

    try :
       if args.srctype.upper() == "JSON" :
            _ = json.loads(INPUT)
       elif args.srctype.upper() == "YAML" :
            _ = yaml.safe_load(INPUT)
       elif args.srctype.upper() == "XML" :
            _ = xmltodict.parse(INPUT)
       else :
        print("# unsupported file type.")
        return -1
    except :
        print("# invalid JSON/YAML/XML.")
        traceback.print_exc()
        return -1

    print("",flush=True)

    sys.stdin = sys.__stdin__

    history = deque(maxlen=200)
    dotkey = True
    if args.interactive :
        cmd0=""
        print("$[dsq]: data loaded.")
        res=""
        err=""
        while True :
            sin = input("$[dsq]: ")
            if not sin :
                continue
            lastc =[int(ord(c)) for c in sin][-1]
            if lastc and lastc in [65,66,67,68] : 
                sin = "\\hist"
            if re.match(r"\s*no\s*dotkey\s*",sin) :
                dotkey = False
            if re.match(r"\s*dotkey\s*",sin) :
                dotkey = True
            if sin in ["quit()","\\q"] :
                break
            if sin in ["\\hist","\\history"] :
                if not history :
                    print("# no history found.")
                for i,cmd in enumerate(history) :
                    print("# {:3} : {}".format(i,cmd))
                continue
            m = re.match(r"\\r (\d+)",sin) 
            if m:
                ix = int(m.group(1))
                if ix < len(history) :
                    sin = history[ix]
                else :
                    continue
            cmd0 = None
            if dotkey and "." in sin :
                cmd0 = sin
                chgsin = sin
                m = re.search(r"\w+(\.\w+)+",chgsin)
                while m :
                    before = chgsin[:m.start()]
                    end = chgsin[m.end():]
                    chain = m.group(0)
                    newchain = ""
                    for w in chain.split(".") :
                        if newchain :
                            newchain += "['"+ w + "']"
                        else :
                            newchain += w
                    chgsin = before + newchain + end
                    m = re.search(r"\w+(\.\w+)+",chgsin)
                sin = chgsin
            try :
                if cmd0 :
                    history.append(cmd0)
                elif not sin.startswith("\\") :
                    history.append(sin)
                if sin.startswith("\\") :
                    res = ""
                    err = "# command not recognized."
                else :
                    res = eval(sin)
            except :
                err = traceback.format_exc()
            finally :
                if res :
                    print(res)
                if err :
                    print(err)
                err=""
            time.sleep(0.1)
        return 0

    if os.path.isfile(args.code) :
        code = open(args.code,"r").read()
    else :
        code = args.code

    if args.func :
        fname = "".join([random.choice(string.ascii_letters) for _ in range(20)])
        newcode = ""
        if args.module :
            for m in args.module.split(",")  :
                if m :
                    m.strip()
                    if m.startswith("from ") :
                        newcode += m + "\n"
                    else :
                        newcode += "import " + m + "\n"
        newcode += "def {}(_) :\n".format(fname)
        for ln in code.splitlines() :
            newcode += " "*(int(args.indent)) + ln.rstrip()
        code = newcode
    else :
        if not re.search(r"def \w+?\(\w+?)\s*:*",code,re.DOTALL) :
            print("# cannot find function definition.")
            sys.exit(-1)

    if args.debug :
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



if __name__ == "__main__" :
    main()
