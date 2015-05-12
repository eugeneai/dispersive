source('scaling.R')

funcX <- function(b, X) {
    x0=b[1]
    A=b[2]
    sigma=b[3]
    exp(-((X-x0)^2/(2*sigma^2)))*sqrt(2*pi)*A
    }

funcXX <- function(b, X) {
    x0=b[1]
    A=b[2]
    sigma=b[3]
	x0_2=b[4]
	A_2=b[5]
	sigma_2=sigma[6]
    exp(-((X-x0)^2/(2*sigma^2)))*sqrt(2*pi)*A+exp(-((X-x0_2)^2/(2*sigma_2^2)))*sqrt(2*pi)*A_2
    }

funcX1 <- function(b,x0,X) {
    sigma=b[1]
    A=b[2]
	exp(-((X-x0)^2/(2*sigma^2)))*sqrt(2*pi)*A
    }

funcX2 <- function(b,sigma,X) {
    x0=b[1]
    A=b[2]
	exp(-((X-x0)^2/(2*sigma^2)))*sqrt(2*pi)*A
    }

funcX3 <- function(b,A,X) {
    sigma=b[1]
    x0=b[2]
	exp(-((X-x0)^2/(2*sigma^2)))*sqrt(2*pi)*A
    }

dif_spec1 <- function(b) {
    #X=0:(length(CHANNELS)-1)
	#CX0=which.max(CHANNELS)

	sum((CHANNELS-funcX1(b,CX0,X))^2)
}

dif_spec2 <- function(b) {
    #X=0:(length(CHANNELS)-1)
	#CX0=which.max(CHANNELS)
	#CA=CHANNELS[CX0]
	#CA_2=CA/2
	#t=subset(CHANNELS, CHANNELS > CA_2)
	#t1=which(t[1]==CHANNELS)
	#t2=(CX0-t1)*2
	#t3=t2/2.355
	#CSigma=t3
	sum((CHANNELS-funcX2(b,CSigma,X))^2)
}

dif_spec3 <- function(b) {
    #X=0:(length(CHANNELS)-1)
	#CX0=which.max(CHANNELS)
	#CA=CHANNELS[CX0]
	sum((CHANNELS-funcX3(b,CA,X))^2)
}

dif_spec <- function(b) {
    sum((CHANNELS-funcX(b,X))^2)
}

dif_specXX <- function(b) {
    sum((CHANNELS-funcXX(b,X))^2)
}

#opt_spec <- function(x,y) {


opt_spec <- function(x) {
#X=0:(length(CHANNELS)-1)
#CX0=which.max(CHANNELS)
#CA=CHANNELS[CX0]
#CA_2=CA/2
#t=subset(CHANNELS, CHANNELS > CA_2)
#t1=which(t[1]==CHANNELS)
#t2=(CX0-t1)*2
#t3=t2/2.355
#CSigma=t3
#print(CSigma)
#CSigma=8.196423
pike1=optim(c(CSigma,CA), dif_spec1, gr=NULL,
   method = c("Nelder-Mead"),
   lower = -Inf, upper = Inf,
   control = list(maxit=500), hessian = F)

#print(pike1$par[1])
CSigma<<-pike1$par[1]
CA<<-pike1$par[2]


pike2=optim(c(CX0,CA), dif_spec2, gr=NULL,
   method = c("Nelder-Mead"),
   lower = -Inf, upper = Inf,
   control = list(maxit=500), hessian = F)

#print(pike2$par)
CX0<<-pike2$par[1]
CA<<-pike2$par[2]

pike3=optim(c(CSigma,CX0), dif_spec3, gr=NULL,
   method = c("Nelder-Mead"),
   lower = -Inf, upper = Inf,
   control = list(maxit=500), hessian = F)

#print(pike3$par[1])
CSigma<<-pike3$par[1]
CX0<<-pike3$par[2]

zero_pike=optim(c(CX0,CA,CSigma), dif_spec, gr=NULL,
   method = c("Nelder-Mead"),
   lower = -Inf, upper = Inf,
   control = list(maxit=500), hessian = F)
#print(zero_pike$par[3])
CX0<<-zero_pike$par[1]
CA<<-zero_pike$par[2]
CSigma<<-zero_pike$par[3]

ZY_3d=funcX(zero_pike$par, X)

#AX=0:(length(ALL_CHANNELS)-1)
	#ZY=funcX(pike3$par[1],pike2$par[2],pike3$par[2], X)
d=c(CX0,CA,CSigma)
ZY_2d=funcX(d,X)

#AZY=funcX(zero_pike$par, AX)
#plot(ALL_CHANNELS, type='l', col='blue')
lines(X+x+left,CHANNELS, type='l', col='blue')
#lines(ALL_CHANNELS-AZY, col='green')

lines(X+x+left, ZY_2d, col='green')
lines(X+x+left, ZY_3d, col='red')
#CA<<-NA
#CSigma<<-NA
#CX0<<-NA
#Csigma=zero_pike$par[3]
#print(zero_pike$par[1])
}




ALL_CHANNELS=standard
png(file = "spectre.png")
plot(ALL_CHANNELS, type='l')
dev.off()
left=0
right=1500
l=3
plot(ALL_CHANNELS, type='l')
while (l>0) {

spec=ALL_CHANNELS[left:right]
#png(file = "1_half.png")
#plot(spec, type='l')

k=3
if (l==1) {k=1}
while (k>0) {
#print(Csigma)
X0_pike=which.max(spec)
A_pike=spec[X0_pike]
A_2_pike=A_pike/2
r=subset(spec, spec > A_2_pike)
i=1
r1=which(r[i]==spec)
while ((X0_pike-r1)>50) {
	i=i+1
	r1=which(r[i]==spec)
}
r2=(X0_pike-r1)*2
r3=r2/2.355

#print(A_pike)
x1=(X0_pike-r3*3.5)
y1=(X0_pike+r3*3.5)
CHANNELS=spec[x1:y1]

X=0:(length(CHANNELS)-1)
CX0=which.max(CHANNELS)
CA=CHANNELS[CX0]
CA_2=CA/2
t=subset(CHANNELS, CHANNELS > CA_2)
t1=which(t[1]==CHANNELS)
t2=(CX0-t1)*2
t3=t2/2.355
CSigma=t3


#print(spec[x1:y1])
#opt_spec(x1,y1)
opt_spec(x1)
spec[x1:y1]=0
k=k-1

#Csigma=(Csigma+1)

}
#dev.off()
#lines(spec, type='l', col='yellow')
left=left+1500
right=right+1500

l=l-1
}
