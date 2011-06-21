#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
try:  
	import pygtk  
	pygtk.require("2.0")  
except:  
	pass  
try:  
	import gtk  
	import gtk.glade  
except:  
	print("GTK Not Availible")
	sys.exit(1)
try:
        import pylab
        from matplotlib import mlab
        import matplotlib.pyplot as plt
except:
        print("Matplotlib Not Aviable")
try:
        import rpy2
        import rpy2.robjects as robjects
except:
        print("rpy2 Not Aviable")
        sys.exit(1)
from numpy import*
#класс для обработки событий графического окна
class GUI(object):
   wTree = None
   def __init__(self):
       self.wTree = gtk.glade.XML("m.glade")
       #список событий
       dic = {
	"on_copy_clicked" : self.on_copy_clicked,
	"on_draw_clicked" : self.on_draw_clicked,
	"on_find_clicked" : self.on_find_clicked,
	"on_load_data_clicked" : self.on_load_data_clicked,
	"on_load_parametrs_clicked" : self.on_load_parametrs_clicked,
	"on_save_parametrs_clicked" : self.on_save_parametrs_clicked,
       }
       self.window = self.wTree.get_widget("win_main")
       self.window.connect("delete_event",self.gtk_main_quit)
       self.wTree.signal_autoconnect( dic )
       
       self.r=robjects.r
#подключение модуля R
       self.r['source']('MNK.R')
#извлечение необходимых функций
       self.lorentz=self.r['lorentz']
       self.fminsearch=self.r['fminsearch']
       self.sumsq=self.r['sumsq']
       self.conversion=self.r['conversion']
#псевдонимы обьектов
       self.error1=self.wTree.get_widget("error1")
       self.input1_A=self.wTree.get_widget("input1_A")
       self.input1_gamma=self.wTree.get_widget("input1_gamma")
       self.input1_x0=self.wTree.get_widget("input1_x0")
       self.input2_A=self.wTree.get_widget("input2_A")
       self.input2_gamma=self.wTree.get_widget("input2_gamma")
       self.input2_x0=self.wTree.get_widget("input2_x0")
       self.output1_A=self.wTree.get_widget("output1_A")
       self.output1_gamma=self.wTree.get_widget("output1_gamma")
       self.output1_x0=self.wTree.get_widget("output1_x0")
       self.output2_A=self.wTree.get_widget("output2_A")
       self.output2_gamma=self.wTree.get_widget("output2_gamma")
       self.output2_x0=self.wTree.get_widget("output2_x0")
       self.error2=self.wTree.get_widget("error2")    
         

       gtk.main()

   #получить точку пика    
   def get_peak(self,spectr):
       index=spectr.argmax(None)
       return(robjects.FloatVector([self.E[index],max(spectr)]))
      

   def gtk_main_quit(self, widget, data = None):
       gtk.main_quit()
#       sys.exit(0)

   
   def get_x_input(self):
       x0=robjects.FloatVector([eval(self.input1_A.get_text()),
                                eval(self.input1_gamma.get_text()),
                                eval(self.input1_x0.get_text()),
                                eval(self.input2_A.get_text()),
                                eval(self.input2_gamma.get_text()),
                                eval(self.input2_x0.get_text())])
       return x0
    
   def get_const_bool(self):    
        const=robjects.BoolVector([not self.wTree.get_widget("check1_A").get_active(),
                                   not self.wTree.get_widget("check1_gamma").get_active(),
                                   not self.wTree.get_widget("check1_x0").get_active(),
                                   not self.wTree.get_widget("check2_A").get_active(),
                                   not self.wTree.get_widget("check2_gamma").get_active(),
                                   not self.wTree.get_widget("check2_x0").get_active()])
        return const
   #вывод вектора x в соответствующие текстовые поля 
   def set_to_output(self,x,const):
       xstr=robjects.StrVector(["","","","","",""])
       if const[0]:
          xstr[0]=str(x[0])     
       if const[1]:
          xstr[1]=str(x[1])     
       if const[2]:
          xstr[2]=str(x[2])     
       if const[3]:
          xstr[3]=str(x[3])     
       if const[4]:
          xstr[4]=str(x[4])     
       if const[5]:
          xstr[5]=str(x[5])     
       self.output1_A.set_text(xstr[0])
       self.output1_gamma.set_text(xstr[1])
       self.output1_x0.set_text(xstr[2])
       self.output2_A.set_text(xstr[3])
       self.output2_gamma.set_text(xstr[4])
       self.output2_x0.set_text(xstr[5])
       self.error2.set_text(str(self.sumsq(self.E,self.Y,x)[0])) 

   #вывод вектора x         
   def set_to_input(self,x):
       self.error1.set_text(str(self.sumsq(self.E,self.Y,x)[0]))
       self.input1_A.set_text(str(x[0]))
       self.input1_gamma.set_text(str(x[1]))
       self.input1_x0.set_text(str(x[2]))
       self.input2_A.set_text(str(x[3]))
       self.input2_gamma.set_text(str(x[4]))
       self.input2_x0.set_text(str(x[5]))
       l1=array(self.lorentz(self.get_p1(),self.E))
       l2=array(self.lorentz(self.get_p2(),self.E))
       l=l1+l2
       p=self.get_peak(l)
       self.wTree.get_widget("peak_kev").set_text(str(p[0]))
       self.wTree.get_widget("peak_intensity").set_text(str(p[1]))


   def get_p1(self):
        p1=robjects.FloatVector([eval(self.input1_A.get_text()),
                                 eval(self.input1_gamma.get_text()),
                                 eval(self.input1_x0.get_text())])   
        return(p1)  

   def get_p2(self):
        p2=robjects.FloatVector([eval(self.input2_A.get_text()),
                                 eval(self.input2_gamma.get_text()),
                                 eval(self.input2_x0.get_text())])   
        return(p2)    
    
   def on_copy_clicked(self,widget):
       try:    
          self.set_to_input(self.x)
       except:
          pass
   #метод рисования графика    
   def on_draw_clicked(self,widget):
       x= array(self.E)
       y= array(self.Y)
       l1=array(self.lorentz(self.get_p1(),self.E))
       l2=array(self.lorentz(self.get_p2(),self.E))
       l=l1+l2
       plt.plot(x,l1,label='lorentz1')
       plt.plot(x,l2,label='lorentz2')
       plt.plot(x,l,label='approximation')
       plt.plot(x,y,label='spectr')
       plt.xlabel('kev')
       plt.ylabel('inensity')
       plt.legend()
       plt.show()
   #поиск точки минимума
   def on_find_clicked(self,widget):
       #собрать вектор x0 c текстовых полей    
       x0=self.get_x_input()
       #собрать вектор const c checkbutton
       self.const=self.get_const_bool()
       #поиск точки минимума
       self.x=self.fminsearch(self.E,self.Y,x0,self.const)
       #вывод вектора x
       self.x=self.conversion(x0,self.const,self.x)
       #print(self.const)
       self.set_to_output(self.x,self.const)
       
   def on_load_data_clicked(self,widget):
       dialog = gtk.FileChooserDialog("Open..",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
       dialog.set_default_response(gtk.RESPONSE_OK)
       filter = gtk.FileFilter()
       filter.set_name("R files")
       filter.add_pattern("*.csv")
       dialog.add_filter(filter)
       response = dialog.run()
       if response == gtk.RESPONSE_OK:
           self.path_data=dialog.get_filename()
       elif response == gtk.RESPONSE_CANCEL:
           pass
       dialog.destroy()
       #извлечение необходимых данных(из csv файла)       
       d=self.r['read.csv'](self.path_data)
       self.E=d[2]
       self.Y=d[1]
       try:
          self.set_to_input(self.p1+self.p2)
       except:
          pass
       
   def on_load_parametrs_clicked(self,widget):
       dialog = gtk.FileChooserDialog("Open..",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
       dialog.set_default_response(gtk.RESPONSE_OK)
       filter = gtk.FileFilter()
       filter.set_name("R files")
       filter.add_pattern("*.csv")
       dialog.add_filter(filter)
       response = dialog.run()
       if response == gtk.RESPONSE_OK:
           self.path_prm=dialog.get_filename()
       elif response == gtk.RESPONSE_CANCEL:
           pass
       dialog.destroy()
       self.d=self.r['read.csv'](self.path_prm)
       self.p1=self.d[1]
       self.p2=self.d[2]
       try:
          self.set_to_input(self.p1+self.p2)
       except:
          pass     
       
   def on_save_parametrs_clicked(self,widget):
       pass
            
a = GUI()
