import sqlite3 as sql
from collections import namedtuple
import os, os.path
import csv

DEBUG=False

fields="Z, Line_Name, Comment, line_keV, tube_KV, Filter, Ref_Sample, Ref_Line, Calib, Collimator, Crystal, Detector, Peak_2th, Bkg_2th, LLD, ULD"

Line=namedtuple('Line', fields)

class Lines(object):
    def __init__(self, csv=None, dbname=None):
        if csv == None and db==None:
            raise ValueError, 'one of csv or db should be supplied'

        if csv != None:
            dbname=self.convert_csv(csv)

        self.dbname=dbname

        self.connect()

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
        for row in map(Line._make, reader):
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
            if (Z, ln) in lset:
                continue
            lset.add((Z, ln_))
            if debug:
                print row
            c2.execute("INSERT INTO lines (Z, Name, keV) VALUES (?,?,?);",
                row)
            if Z in eset:
                continue
            eset.add(Z)
            c2.execute("INSERT INTO elements (Z, Name) VALUES (?,?);",
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

if __name__=='__main__':
    lines=Lines('/home/eugeneai/Development/codes/dispersive/SPECPLUS/DATA/lines.csv')
    #for l in lines.fetch_all(' 1 order by Z'):
    #    print l
