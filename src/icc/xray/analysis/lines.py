import sqlite3 as sql
from collections import namedtuple
import os, os.path
import csv

DEBUG=True

fields="Z, Line_Name, Comment, line_keV, tube_KV, Filter, Ref_Sample, Ref_Line, Calib, Collimator, Crystal, Detector, Peak_2th, Bkg_2th, LLD, ULD"

CSVLine=namedtuple('CSVLine', fields)
Line=namedtuple('Line', 'Z, element, name, keV')
Element=namedtuple('Element', 'Z, Name')

def _float(x):
    print x
    try:
        x=float(x)
    except e:
        print e
    return x

class Lines(object):
    def __init__(self, csv=None, dbname=None):
        if csv == None and dbname==None:
            raise ValueError, 'one of csv or db should be supplied'

        if csv != None:
            dbname=self.convert_csv(csv)

        self.dbname=dbname

        self.connect()
        self.db.create_function("float", 1, _float)

    def convert_csv(self,filename, debug = DEBUG):
        def _f(x):
            if x=='':
                return None
            if x.find(';')!=-1:
                return None
            try:
                return float(x.replace(',','.').replace('*',''))
            except ValueError, e:
                print "Error:", e
                return x
        reader=csv.reader(open(filename), delimiter=';')
        db_name=os.path.splitext(filename)[0]+'.sqlite3'
        conn=self.connect(dbname=db_name)
        conn.create_function("float", 1, _f)
        reader.next() # skip first row of fiels names
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS tmp ;')
        cur.execute('DROP TABLE IF EXISTS lines ;')
        cur.execute('DROP TABLE IF EXISTS elements ;')
        self.create_db(conn)
        for row in map(CSVLine._make, reader):
            #params=['?'] * len(row)
            #params=', '.join(params)
            params='?, ?, ?, float(?), ?, ?, ?, ?, ?, float(?), ?, ?, float(?), float(?), ?, ?'
            cmd="""
                INSERT INTO tmp (%s)
                VALUES
                (%s);
            """ % (fields, params)
            cur.execute(cmd, row)
        #print cmd
        conn.commit()
        cur = conn.cursor()
        cur.execute('''SELECT DISTINCT Z, line_keV, Line_Name from tmp;''')
        c2=conn.cursor()
        lset=set()
        eset=set()
        for row in cur:
            Z, keV, ln = row
            ln_=ln.split()[1].split('-')[0]
            row=(Z, keV, ln_)
            if (Z, ln_) in lset:
                continue
            lset.add((Z, ln_))
            if debug:
                print row
            c2.execute("INSERT INTO lines (Z, keV, Name) VALUES (?, ?, ?);",
                row)
            if Z in eset:
                continue
            eset.add(Z)
            c2.execute("INSERT INTO elements (Z, Name) VALUES (?, ?);",
                (Z, ln.split()[0]))

        conn.commit()

        return db_name

    def connect(self, dbname=None):
        if dbname != None:
            return sql.connect(dbname)

        if type(self.dbname) in [type(''), type(u'')]:
            self.db = sql.connect(self.dbname)

        return self.db

    def create_db(self, db=None):
        if db == None:
            db = self.db
        c=db.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS tmp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Z INTEGER,
                Line_Name TEXT NULL,
                Comment TEXT NULL,
                line_keV REAL,
                tube_KV REAL,
                Filter TEXT NULL,
                Ref_Sample TEXT NULL,
                Ref_Line TEXT NULL,
                Calib TEXT NULL,
                Collimator REAL,
                Crystal TEXT NULL,
                Detector TEXT NULL,
                Peak_2th REAL NULL,
                Bkg_2th TEXT NULL,
                LLD REAL NULL,
                ULD REAL NULL
        );
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Z INTEGER,
                Name TEXT,
                keV REAL
        );
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS elements (
                Z INTEGER PRIMARY KEY,
                Name TEXT
        );
        ''')

    def fetch_all(self, sql, params=tuple()):
        cur=self.db.cursor()
        sql='''SELECT DISTINCT %s from lines ''' % fields+" where "+sql+';'
        rows=cur.execute(sql,params)
        for row in map(Line._make, rows):
                yield row

    def select(self, Z=None, element=None, line=None, kev=None, where=None, order_by=None):
        if line:
            line=line.upper()
        c=["1"]
        if Z != None:
            c.append("e.Z=%i" % Z)
        if element != None:
            c.append("e.Name='%s'" % element)
        if line != None:
            c.append("l.Name='%s'" % line);
        if kev != None:
            c.append("l.kev=%f" % kev);
        stmt="""
        SELECT e.Z, e.Name as element, l.Name as line, l.keV as kev
        FROM elements e INNER JOIN lines l ON e.Z=l.Z
        WHERE
        %s
        """ % ' and '.join(c)
        if where:
            stmt+=" and "+where
        if order_by:
            stmt+=" ORDER BY "+order_by

        stmt+=" ;"
        cur = self.db.cursor()
        if DEBUG:
            print "STMT:", stmt
        cur.execute(stmt)
        for row in cur:
            yield Line._make(row)


if __name__=='__main__':
    import os
    import pylab as pl
    import pprint as pp
    import numpy as np

    #lines=Lines(csv='/home/eugeneai/Development/codes/dispersive/SPECPLUS/DATA/lines.csv')
    if os.name!="nt":
        lines=Lines(dbname='/home/eugeneai/Development/codes/dispersive/SPECPLUS/DATA/lines.sqlite3')
    else:
        lines=Lines(dbname='C:\\dispersive\\SPECPLUS\\DATA\\lines.sqlite3')
        
    L1={'A':0.8, "B":0.8/6.}
    L2={'K':(0,0,0), "L":(1,0,0)}

    ls=list(lines.select(order_by="keV", where="not l.name like 'M%' and keV<20. and (e.name='Mo' or e.name='W' or e.name='Cl' or e.name='Zr' or e.name='V' or e.name='Si' or e.name='As') "))
    pp.pprint(ls)
    print len(ls)
    x=np.array([0, ls[-1].keV*1.03])
    y=np.array([1, 1.])
    pl.plot(x,y)
    y=np.array([0, 0.])
    pl.plot(x,y)

    pl.axvline(0.0, color=(0,1,0))
    pl.axvline(0.0086, color=(0,1,0))
    for l in ls:
        ln=l.name[0]
        ln2=l.name[1]
        pl.axvline(l.keV, color=L2.get(ln, 1.), ymax=L1.get(ln2, (0,1,0)))

    pl.show()
