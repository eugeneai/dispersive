#!/home/chertenok/dev/python-2.4/bin/python2.4
# encoding:utf8
# Regression analysis of X-RAY

import numpy 
#from appliance import *
import scipy.optimize as so
from compiler.ast import *
from compiler.pycodegen import ModuleCodeGenerator
from math import *
import rpy2
import rpy2.robjects as robjects

class ExperimentError(Exception):
	pass
class ExperimentDataError(ExperimentError):
	pass

import compiler, compiler.visitor

class NameVisitor(compiler.visitor.ASTVisitor):
    def __init__(self):
        compiler.visitor.ASTVisitor.__init__(self)
        self.constants={}
        self.other={}
        self.expr=None
    def visitName(self, node):
        name=node.name
        if name.startswith("c"):
            self.constants[name]=1
        else:
            self.other[name]=1
    def visitCallFunc(self, node):
        for n in node.getChildren()[1:]:
            if n is not None:
                self.visit(n)
    def visitExpression(self, node):
	#if self.expr is not None:
	self.expr=node.node
        self.visit(node.node)

def compile_model_as_module(func_name, model):
    """
    Compiles model, which is string expression, expressing mathematical 
    equation of the fitting model.
    The expression contain various varibales, including those to fit.
    All variables, starting with "c" (lower case only) supposed to be the fitting
    constants.
    
    returns tuple: (<function according to requirenments of leastSquaresFit>, 
        list of variables with fitted variables excluded, 
        list of fitting variables)
        
    Name of function will be the |func_name|.
    
    Examples of the equations:
        c0+c1*Th+c2*Hg**2.
    """
    ast=compiler.parse(model, mode="eval")
    v=NameVisitor()
    
    compiler.walk(ast, v)
    consts=list(v.constants.keys())
    vars=list(v.other.keys())
    func=Function(None, func_name,
        [tuple(consts)]+vars+["_Y_target"], [], 0, "User model %s" % model, 
        Stmt([Return(Sub((v.expr, Name("_Y_target"),)))]))
    func.filename="<user models>"
    stmt=Stmt([From('math', [('*', None)], 0), func])
    mod=Module("user_models", stmt)
    mod.filename="<user models>"
    gen=compiler.pycodegen.ModuleCodeGenerator(mod)
    code=gen.getCode()
       
    return (code, consts, vars)
    
def compile_model(func_name, model):
    (code, consts, vars) = compile_model_as_module(func_name, model)
    d={}
    exec(code, d)
    return (d[func_name], consts, vars)
    
#print compiler.parse("""def fun((a,b,c), ((d,e), ff)):
#    return a
#""")
# Data: ((x1,x2), y, value), 0<=value<=1 - significance


class ExperimentData:
    def __init__(self,
                    intensities,     
                    # list of tuples of dictionaries of dictionaries - 
                    # not done!! #    [(<identifier of sample>, {"<element>":{"line-name":<intensity>,...}...}), ...]. It is "sorted" in the measurement sequence
                    ss, # dictionary of dictionaries - {<identifier of sample>:{"<element>":<concentrations>,...}}. These concentrations are supposed to be known.
                    reper=None # name of a sample, which supposed to be a reper
                    ):
        self.intensities=intensities
        self.ss=ss      # I.e., standard samples.
        self.reper=reper
        self.normalized=0
    def normalize(self):
        """
        Nnormalize intensities to the reper data.
        The normalization made in place
        """
        ireper=[]
        for (iname, idata) in self.intensities:
            if iname==self.reper:
                ireper.append((iname, idata))
        self.rintensities=ireper        # Just store the intermediate result
        l=len(ireper)
        if l==0:
            return      # No normalization
        elif l==1:
            return      # No normalization
        sum={}
        for el in ireper[0][1].keys():
            sum[el]=0.0
        for (iname, idata) in ireper:
            for (el, val) in idata.items():
                sum[el]+=val
        avg={}
        for (key, val) in sum.items():
            avg[key]=val/l
        self.avgreper=avg
        self.intensities=self.normalize_ints(self.intensities)
        self.normalized=1
        
    def normalize_ints(self, intensities):
        answer=[]
        avg=self.avgreper
        for (iname, idata) in intensities:
            nid={}
            for (el, val) in idata.items():
                norm=avg[el]
                if norm>0:
                    nid[el]=val / norm
                else:
                    nid[el]=val
            answer.append((iname, nid))
        return answer
        
    def select(self, ss=1):
        """
        Selects and returns intensities, belonging to
        Standard Samples, if |ss==1|, 
        and probes otherwise.
        In both cases for reper, if any, middle value returned.
        """
        answer=[]
        for (iname, idata) in self.intensities:
            s=self.ss.get(iname, None)
            if (s is not None and ss) or (s is None and not ss):
                if iname==self.reper and self.normalized:
                    idata=self.avgreper
                answer.append((iname, idata))
        return answer

class Calibration:
    def __init__(self, 
                    experimentData, # Instace of the class Experiment
                    elements,       # dictionary - {<element>: <element exp string>}. 
                    ):

        self.ed=experimentData
        self.elements=elements
        self.prepared=0
        self.calibrated=0

    def as_frame(self, element, data, encoding='utf-8', conc=True):
            cols={'probe':[]}
            if conc:
                    cols['conc']=[]
            for probe, elems in data:
                    cols['probe'].append(probe)
                    if conc:
                            if probe in self.ed.ss:
                                    c = self.ed.ss[probe][element]
                                    cols['conc'].append(c)
                            else:
                                    cols['conc'].append(None)
                    for e,v in elems.items():
                            l = cols.setdefault(e, [])
                            l.append(v)

            ncols={}
            for c,v in cols.items():
                    ncols[c.encode('utf8')]=robjects.FloatVector(v)
            df = robjects.DataFrame(ncols)
            return df, list(cols.keys())
    
    def calculate(self, init_values=None, raw_init_values=1, significance=None):
        """
        Calculate the calibration.
        init_values - initial values:
            {<element> : {<constant>:value, ...},...} should correspond 
            the models.
        raw_init_values - raw init values, used if init_values is None
        """
        answer={}
        if not self.prepared:
            self.prepare()
        raw_data=self.ed.select(ss=1) # Select all intensities for standard samples
        res={}
        for (el, v) in self.models.items():
            (_el, _equ, model)=v
	    #print "V is", v
	    #print "Raw:", raw_data
            data=raw_data # self.select_ints(raw_data, vars, el, significance)
            #print "Data:", data

            # create a data frame for R
            df, _keys = self.as_frame(_el, data)

            robjects.globalenv['cal_data']=df
            cmd='lm(%s, data=cal_data)' % model
            #print cmd
            fit = robjects.r(cmd)
            #print fit
            robjects.r['rm']('cal_data')
            res[_el]=fit

        self.calibration=res
        self.calibrated=1
        return res
        
    def concentrations(self, ints, elements=None):
        """
        Calculate lift of the concentrations.
        if |elements|, which is a list of element names, 
            is None then return only concentrations for
            known in the calibration elements
        else
            constructs concentrations for given |elements|
        """
        if elements is None:
            elements=list(self.calibration.keys())
        cal = self.calibration
        answer = {}
        a={}
        for el in elements:
                df, keys = self.as_frame(el, ints, conc=False)
                rc = robjects.r['predict'](cal[el], df)
                a[el]=rc
        # transpose
        row=0
        answer=[]
        for name, _ in ints:
               ed={}
               for el in elements:
                       ed[el]=a[el][row]
               row+=1
               answer.append((name, ed))
        return answer
    
    def prepare(self):
        """
        We should prepare data to make the corellation according to 
        requirenments of the |leastSquaresFit| function,
        ensure that the intensities are normalized with the reper data,
        and make the corellation functions from task given in elemets.
        """
        if not self.ed.normalized:      # try to normalize intensities
            self.ed.normalize()
        # so we have raw, probably normalized data, of the structure (iname, idata_dict).
        self.prepare_functions()
        self.prepared=1
        
    def select_ints(self, ints, elements, element=None, significance=None):
        """
        Selects and prepare data for leastSquaresFit procedure.
        Parameters:
            ints - intensities, which select from,
            elements - elements to be selected (ptojection),
            element - the dependant element (function), 
                its concentration in the so (element is not None),
            significance - value of the data row (None - assign all 1):
                dictionary {<probe or ss name>: <value>}, value is in [0,1]
        """
        answer=[]
        for (iname, idata) in ints:
            els=[]
            for el in elements:
                els.append(idata[el])
            if element is not None:
                fel=self.ed.ss[iname][element]
                if significance is not None:
                    sig=significance.get(el, 1)
                    a=(els, fel, sig)
                else:   # significance is None
                    a=(els, fel)
            else:
                a=(els, 0.)
                # exit for concentration calculation
            answer.append(a)
	if not answer:
	    return answer
	lv=len(answer)
	lh=len(answer[0][0])+1
	llast=lh-1
	newa=[]
	for i in range(lh):
	    newa.append(numpy.zeros(lv,float))
	for i, row in enumerate(answer):
	    vx, y=row
	    for j, x in enumerate(vx):
		newa[j][i]=x
	    newa[llast][i]=y
        return newa
    
    def prepare_functions(self):
        models={}
        for (el, equ) in self.elements.items():
            models[el]=(el, equ, 'conc~'+equ)
        self.models=models
        
    # -------- util -------------
    def draw_picture(self, index):
        import biggles
        p = biggles.FramedPlot()
        p.aspect_ratio = 1
        p.title="Calibration for %i-th channel" % index
        p.xlabel="Concentrations"
        p.ylabel="Intensities"
        p.xrange=0, 1.2
        p.yrange=0, 7000
        
        x=[]
        y=[]
        for cd in range(len(self.concentrations)):
                cs=self.concentrations[cd]
                iss=self.intensities[cd]
                c=cs[index]
                i=iss[index]
                x.append(c)
                y.append(i)
    
        points = biggles.Points( x, y, type="circle" )
        points.label = "Data"
                
        #print x,y
        
        # data for line driwing
        
        xx=[]
        for i in self.intensities:
                xx.append(self.choose(i))
                
        xx_max=[]
        xx_min=[]
        for j in range(len(self.indices)):
                a=[]
                for i in xx:
                        a.append(i[j])
                xx_max.append(max(a))
                xx_min.append(min(a))
        
        xindex=self.indices.index(index)
        print(xx_max, xx_min, xindex)
        yy=[xx_min[xindex], xx_max[xindex]]
        iindex=self.element_indices.index(index)
        calibr=self.calibrations[iindex]
        print(yy)
        
        """
        xx=[
                self.equation(calibr[0], xx_min),
                self.equation(calibr[0], xx_max)
        ]
        """
        xx=[
                self.equation(calibr[0], 
                        self.choose(self.intensities[1])),
                self.equation(calibr[0],
                        self.choose(self.intensities[0]))
        ]
    
        line = biggles.Curve(xx, yy)
        line.label = "Calibrating line"
        
        #legend = biggles.PlotKey( .7, .9, [points, line] )
        
        #p.add( line, points, legend)
        p.add( points, line)
        p.show()

if __name__=='__main__':
    from . import load
    load.main()
