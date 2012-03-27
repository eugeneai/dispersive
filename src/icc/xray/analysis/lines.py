import sqlite3 as sql
from collections import namedtuple
import os, os.path
import csv

Line=namedtuple('Line', "Z, Line_Name, Comment, line_keV, tube_KV, Filter, Ref_Sample, Ref_Line, Calib, Collimator, Crystal, Detector, Peak_2th, Bkg_th, LLD, ULD")

class Lines(object):
    def __init__(self, csv=None, db=None):
        if csv == None and db==None:
            raise ValueError, 'one of csv or db should be supplied'

        if csv != None:
            db=self.convert_csv(csv)

        self.connect(db)

    def convert_csv(self,filename):
        reader=csv.reader(open(filename), delimiter=';')
        print reader.next()
        for row in map(Line._make, reader):
            print row



if __name__=='__main__':
    lines=Lines('/home/eugeneai/Development/codes/dispersive/SPECPLUS/DATA/lines.csv')
