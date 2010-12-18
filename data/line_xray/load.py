#!/usr/bin/env python
# encoding: utf-8
import pprint, csv, os, os.path
import types, rpy2
from xray import *

els=[u"Na",u"Mg",u"Al",u"Si",u"P",u"K",u"Ca",u"Ti",
         u"Mn",u"Fe",u"S",u"Ba",u"Sr",u"Zr",u"Cl"]
defMdl={
    "Si":"c0+c1*Si+c2*Fe", 
    "Fe":"c0+c1*Fe+c2*Si",
    "Na":"c0+c1*Na+c2*Al",
    "Mg":"c0+c1*Mg+c2*Ca",
    "Al":"c0+c1*Al", #"+c2*Si",
    "P":"c0+c1*P", # +c2*Fe
    "K":"c0+c1*K", 
    "Ca":"c0+c1*Ca+c2*Mg", #+C4*Mg 
    "Ti":"c0+c1*Ti", 
    "Mn":"c0+c1*Mn+c2*Fe", 
    "S":"c0+c1*S", 
    "Ba":"c0+c1*Ba+c2*Ti", 
    "Sr":"c0+c1*Sr",  # +C3*Ba
    "Zr":"c0+c1*Zr+c2*Sr", 
    "Cl":"c0+c1*Cl",
}


def load_sss(file):
    file.readline()
    file.readline()
    ss={}
    while 1:
        ans=load_ss(file)
        if ans:
            (name, d)=ans
            name=name.strip().decode('utf8')
            ss[name]=d
        else:
            break
    return ss
    
def load_ss(file):
    first=file.readline()
    if first=="": return
    second=file.readline()
    if second=="": return
    third=file.readline()
    if third=="": return
    if first.strip()=="": return
    if second.strip()=="": return
    if third.strip()=="": return
    first=first.strip().split(" ")
    name=first[1]
    second=second.strip().split(" ")
    n=0
    c={}
    for val in second:
        try:
            c[els[n]]=float(val)
            n+=1
        except ValueError:
            pass
    third=third.strip().split(" ")
    try:
        for val in third:
            try:
                c[els[n]]=float(val)
                n+=1
            except ValueError:
                pass
    except IndexError:
        pass
    return (name.strip(), c)
    
def load_exp(file):
    exps=()
    while 1:
        ans=load_ex(file)
        if ans:
            (name, d)=ans
            global curr_name, cprobes, probes
            cprobes.append((name.strip(), d))
        else:
            break
    probes[curr_name]=cprobes
    return probes

probes={}
cprobes=[]
curr_name="unknown"

def load_ex(file):
    first=file.readline().strip()
    if first=="": return
    first=first.lstrip()
    if first[0]==":":
        global curr_name, cprobes, probes
        probes[unicode(curr_name, 'utf8')]=cprobes
        cprobes=[]
        first=first.split(" ")
        curr_name=" ".join(first[1:])
        first=file.readline().strip()
        if first=="": return
    name=first.strip()
    first=file.readline().strip()
    if first=="": return
    second=file.readline().strip()
    if second=="": return
    first=first.split(" ")
    second=second.split(" ")
    n=0
    c={}
    for val in first:
        try:
            c[els[n]]=float(val)
            n+=1
        except ValueError:
            pass
    try:
        for val in second:
            try:
                c[els[n]]=float(val)
                n+=1
            except ValueError:
                pass
    except IndexError:
        pass
    return (unicode(name, 'utf8'), c)    

    
def print_ints(ints):
    for (iname, idata) in ints:
        print "\t", iname
        print_els(idata)
            
def print_els(data):
    n=0
    for el in els:
        if n==0:
            print "\t",
        val=data.get(el, None)
        if val is not None:
            print "%2s:%07.3f" % (el, val),
            n+=1
            if n==8:
                print "\n",
                n=0
    if n!=0:
        print

def print_parties(self, parties):
    for (name, ints) in parties.iteritems():
        print "Партия:%s" % name
        print_ints(ints)

def _as_utf8(s):
    if type(s)==types.UnicodeType:
        return s.encode('utf8')
    return s

def csv_export_party(party, csvw):
    """Export party probes in a CSV stream"""
    header=["name"]+els
    csvw.writerow(header)
    if type(party)==dict:
        party=party.items()
    for probe, elems in party:
        row=[probe.replace(" ","_")]
        for el in els:
            row.append(elems[el])
        row=map(_as_utf8, row)
        csvw.writerow(row)

def csv_export(parties, prefix):
    """Export data to a number of CSV files.
    :param:parties is a exported data,
    :param:prefix is a file name prefix added to each group
    """

    for group, probes in parties.iteritems():
        file_name=prefix+group.replace(" ","_")+".csv"
        print file_name    
        csvw=csv.writer(open(file_name, 'w'), delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
        csv_export_party(probes, csvw)
        del csvw


def main():
    fss=open("Data_calc/poch.cst")
    ss=load_sss(fss)
    #print "Loaded samples", ss
    fss.close()
    fexp=open("Data_calc/Exp.dat")
    eexp=load_exp(fexp)
    fexp.close()

    #pprint.pprint(ss)
    #csv_export(eexp, 'D_')
    #csv_export({"SRSC":ss}, "")
    
    
    # experiment

    calibr=eexp[u"SRS"]
    e=ExperimentData(calibr, ss)
    mdl=defMdl
    c=Calibration(e, mdl)
    #c.calculate(init_values={"Si":{"c0":0, "c1":0}})
    c.calculate()
    test_ss=c.concentrations(calibr)
    print "Аттестованные содержания"
    names=ss.keys()
    names.sort()
    for name in names:
        els=ss[name]
        print name
        print_els(els)
    print "Калибровка (пересчитанная)"
    print_ints(test_ss)
    for (name, ints) in eexp.iteritems():
        if name!="unknown":
            print "Партия:%s" % name
            print_ints(c.concentrations(ints))

if __name__=="__main__":
    main()
