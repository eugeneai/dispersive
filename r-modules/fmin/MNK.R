 conversion<-function(values,const,x)
 {
    values[const]=x
    values
 }

#распределение Лоренца
#p - вектор параметров распределения Лоренца
#x -
lorentz<-function(p,x)
{
#p[1]-A
#p[2]-gamma
#p[3]-x0
        dx=x-p[3]
        p[1] / (pi*p[2]*(1+(dx/p[2])**2))
}


#сумма квадратов
sumsq<-function(E,Y,x)
{
		p1=x[1:3]
        p2=x[4:6]		
        sum((Y-lorentz(p1,E)-lorentz(p2,E))**2)	

}

 #E - вектор энергий (ось ox)
 #Y - спектр, полученный с рентгенофлоуресцентного аппарата (ось оу)
 #values - вектор параметоров кривых Лоренца
 #const - вектор определяющий, какие элементы values есть параметры(константы),
 # а какие переменные(TRUE - переменная,FALSE - параметр)
 fminsearch<-function(E,Y,values,const=c(TRUE,TRUE,TRUE,TRUE,TRUE,TRUE))
 {
  f<-function(E,Y,x)
 {
 	sumsq(E,Y,x)
 }
 
 #fminsearch<-function(x0=as.numeric)
 #построение симплекса из n+1 точки, где n=length(x0)
 simplex<-function(x0=as.numeric)
 {
 #длина ребра симплекса
 t=0.5
 #количество переменных
 n=length(x0)
 #создание матрицы
 m=matrix(rep(x0,n+1),c(n,n+1))
       for (i in 1:n)
	        {
	            m[i,i]=m[i,i]+t
	        } 
  m  
 }
 
 conversion<-function(x)
 {
    values[const]=x
    values
 }
 #вычисление значений ф-ции в точках записанных в матрице m
 evalution<-function(E,Y,m)
 {
        result=c()
        for (i in 1:length(m[1,]))
	    {
		  result[i]=f(E,Y,conversion(m[,i]))
		}
	    result
 }
 #поиск индекса точки из матрицы m, соответствующей значению ф-ции y
 find<-function(E,Y,m,y)
 {
 for (i in 1:length(m[1,]))
     {
	    if (f(E,Y,conversion(m[,i]))==y){
	        result=i
		    }
	 }
	 result
 }
 #центр тяжести(среднее арифметическое) точек, кроме x(h) 
 centerfg<-function(m,h)
 {
 n=length(m[1,])
 x=seq(l=(n-1),from=0,by=0)
 for (i in 1:n)
    {
	     if (i != h)
		    {
              x=x+(m[,i])
            }
	}  
	x=x/(n-1)
 }
 #****************************************************
 #основная функция
 #****************************************************
      #преобразование values в соответствии с вектором const
      x0=values[const] 
      #коэффициент отражения 
      alpha=1
      #коэффициент сжатия
      beta=0.5
      #коэффициент растяжения
      gamma=2
      #инициализация симплекса
      m=simplex(x0)
      #1шаг
 
      for (i in 1:1000)
       {
       fval=evalution(E,Y,m)
       fval=sort(fval)
       n=length(x0)
       #запись индексов точек с наибольшим значением функции,следующим по величине и наименьшим значением ф-ции
       h=find(E,Y,m,fval[n+1])
       g=find(E,Y,m,fval[n])
       l=find(E,Y,m,fval[1])
       #2шаг
       #точка центра тяжести точек, кроме x(h)
       x_c=centerfg(m,h)
       #3шаг
       #отражение
       x_r=(1+alpha)*x_c-alpha*m[,h]
       #вичисление ф-ции в точке xr
       f_r=f(E,Y,conversion(x_r))
       #4шаг
       if (f_r<=fval[1])
           {
      	      #растяжение
      	      x_e=(1-gamma)*x_c+gamma*x_r
		  
      	      f_e=f(E,Y,conversion(x_e))
      	      if (f_e<fval[1])  m[,h]=x_e 		
      	      if (f_e>=fval[1])  m[,h]=x_r
        	 }
       if ((fval[1]<f_r)&(f_r<=fval[n]))
           {
	             m[,h]=x_r
           }	
	        a=((fval[n+1]>=f_r)&(f_r>fval[n]))
            if (a | (f_r>fval[n+1]))
	           {
	           if (a==TRUE)
                    {
	                  c=m[,h]
	      	        m[,h]=x_r
	      	        x_r=c
	      	        c=f_r
	          	    f_r=fval[n+1]
	      	        fval[n+1]=c
	            	 }
          		  x_s=beta*m[,h]+(1-beta)*x_c
	      		  f_s=f(E,Y,conversion(x_s))
 	      	      if (f_s<fval[n+1])
	      		       {
              				tempD=fval[n+1]
		              		tempV=m[,h]
		      	        	m[,h] = x_s
		      		        fval[n+1] = f_s
		      		        x_s=tempV
		              		f_s=tempD
		      		   }
		      	  if (f_s>=fval[n+1])
                         {
		      		      for (i in 1:(n+1))
			      		     {
			      			    if (i != l)
			      				  {
			      				    m[,i]=m[,l]+(m[,i]-m[,l])/2
			      				  }
			      			 }
                         }   				   
		       }
       }
       fval=sort(evalution(E,Y,m))
       l=find(E,Y,m,fval[1])
       m[,l]
 }
 