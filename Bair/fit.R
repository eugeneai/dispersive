funcX <- function(b, X) {
     x0=b[1]
     A=b[2]
     sigma=b[3]
     s2=2*sigma^2
     A*exp(-((X-x0)^2/s2))
     }

#source('C:/scaling.R')
source('./scaling.R')
DEBUG_PIKES=TRUE


dif_spec <- function(b) {
    X=0:(length(CHANNELS)-1)
	sum((CHANNELS-funcX(b, X))^2)
}


opt_spec <- function(x,y, sigma=1.) {

# Дальнейший текст переделать в функцию.

#CHANNELS=ALL_CHANNELS[1:150]
#CHANNELS=spec[x:y]
CX0=which.max(CHANNELS)
CA=CHANNELS[CX0]
print (c(CX0, CA))

pike=optim(c(CX0,CA,sigma), dif_spec, gr=NULL,
   method = c("Nelder-Mead"),
   lower = -Inf, upper = Inf,
   control = list(maxit=5000), hessian = F)

#print(pike)

X=0:(length(CHANNELS)-1)
#AX=0:(length(ALL_CHANNELS)-1)
ZY=funcX(pike$par, X)
#AZY=funcX(pike$par, AX)
#plot(ALL_CHANNELS, type='l', col='blue')
lines(X+x,CHANNELS, type='l', col='blue')
#lines(ALL_CHANNELS-AZY, col='green')
lines(X+x, ZY, col='red')

if (DEBUG_PIKES) {
   png(paste('pike-', CX0, '.png', sep=''))
   plot(CHANNELS, type='l')
   lines(ZY, col='red')
   dev.off()
}

pike
}

ALL_CHANNELS=standard
spec=ALL_CHANNELS[1:3000]
plot(spec, type='l')

Csigma=2.
first = TRUE
k=3
while (k>0) {
      X0_pike=which.max(spec)
      print (X0_pike)
      A_pike=spec[X0_pike]
      print(A_pike)
      s2=round(Csigma*3.)
      #x1=(X0_pike-50)
      #y1=(X0_pike+50)
      x1=(X0_pike-s2)
      y1=(X0_pike+s2)
      CHANNELS=spec[x1:y1]
      X=0:(length(CHANNELS)-1)
      #print(spec[x1:y1])
      pike=opt_spec(x1,y1, Csigma)
      if (first) {
         Csigma=pike$par[3]
         if (Csigma<1.) {
            Csigma = 2.
         }
      }
      print (pike$par)
      sg=pike$par[3]
      if (sg<1. || sg>100.) {
         sg=3.
      }
      s4=round(sg*3.5)
      x1=(X0_pike-s4)
      y1=(X0_pike+s4)
      CHANNELS=spec[x1:y1]
      X=0:(length(CHANNELS)-1)
      spec[x1:y1]=spec[x1:y1]-funcX(pike$par, X)
      k=k-1
}

lines(spec, type='l', col='yellow')
