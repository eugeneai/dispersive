funcX <- function(b, X) {
     x0=b[1]
     A=b[2]
     sigma=b[3]
     exp(-((X-x0)^2/(2*sigma^2)))*sqrt(2*pi)*A
     }

source('C:/scaling.R')

dif_spec <- function(b) {
    X=0:(length(CHANNELS)-1)
	sum((CHANNELS-funcX(b, X))^2)
}


opt_spec <- function(x,y) {

# Дальнейший текст переделать в функцию.

#CHANNELS=ALL_CHANNELS[1:150]
#CHANNELS=spec[x:y]
CX0=which.max(CHANNELS)
CA=CHANNELS[CX0]


zero_pike=optim(c(CX0,CA,Csigma), dif_spec, gr=NULL,
   method = c("Nelder-Mead"),
   lower = -Inf, upper = Inf,
   control = list(maxit=5000), hessian = F)

#print(zero_pike)

X=0:(length(CHANNELS)-1)
#AX=0:(length(ALL_CHANNELS)-1)
ZY=funcX(zero_pike$par, X)
#AZY=funcX(zero_pike$par, AX)
#plot(ALL_CHANNELS, type='l', col='blue')
lines(X+x,CHANNELS, type='l', col='blue')
#lines(ALL_CHANNELS-AZY, col='green')
lines(X+x, ZY, col='red')

}

ALL_CHANNELS=standard
spec=ALL_CHANNELS[1:3000]
plot(spec, type='l')
Csigma=1
k=3
while (k>0) {
X0_pike=which.max(spec)
A_pike=spec[X0_pike]
#print(A_pike)
x1=(X0_pike-50)
y1=(X0_pike+50)
CHANNELS=spec[x1:y1]
spec[x1:y1]=0
#print(spec[x1:y1])
opt_spec(x1,y1)
k=k-1
Csigma=(Csigma+1)
}

lines(spec, type='l', col='yellow')