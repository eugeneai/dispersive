source('scaling.R')

funcX <- function(b, X) {
    x0=b[1]
    A=b[2]
    sigma=b[3]
    exp(-((X-x0)^2/(2*sigma^2)))*sqrt(2*pi)*A
    }

funcX1 <- function(b,X,g,h) {
    if (g==1) {
	sigma=b[1]
    A=b[2]
	x0=h
	}
	if (g==2) {
	x0=b[1]
    A=b[2]
	sigma=h
	}
	if (g==3) {
	sigma=b[1]
    x0=b[2]
	A=h
	}

	exp(-((X-x0)^2/(2*sigma^2)))*sqrt(2*pi)*A
    }


dif_spec <- function(b) {
    sum((CHANNELS-funcX(b,X))^2)
}


dif_spec1 <- function(b) {
    if (g==1) {
	res=sum((CHANNELS-funcX1(b,X,1,CX0))^2)}
	if (g==2) {
	res=sum((CHANNELS-funcX1(b,X,2,CSigma))^2)}
	if (g==3) {
	res=sum((CHANNELS-funcX1(b,X,3,CA))^2)}
	res
}






#opt_spec <- function(x,y) {


opt_spec <- function(x) {

g<<-1
pike1=optim(c(CSigma,CA), dif_spec1, gr=NULL,
   method = c("Nelder-Mead"),
   lower = -Inf, upper = Inf,
   control = list(maxit=500), hessian = F)
CSigma<<-pike1$par[1]
CA<<-pike1$par[2]

g<<-2
pike2=optim(c(CX0,CA), dif_spec1, gr=NULL,
   method = c("Nelder-Mead"),
   lower = -Inf, upper = Inf,
   control = list(maxit=500), hessian = F)
CX0<<-pike2$par[1]
CA<<-pike2$par[2]

g<<-3
pike3=optim(c(CSigma,CX0), dif_spec1, gr=NULL,
   method = c("Nelder-Mead"),
   lower = -Inf, upper = Inf,
   control = list(maxit=500), hessian = F)
CSigma<<-pike3$par[1]
CX0<<-pike3$par[2]

zero_pike=optim(c(CX0,CA,CSigma), dif_spec, gr=NULL,
   method = c("Nelder-Mead"),
   lower = -Inf, upper = Inf,
   control = list(maxit=500), hessian = F)
CX0<<-zero_pike$par[1]
CA<<-zero_pike$par[2]
CSigma<<-zero_pike$par[3]

ZY_3d=funcX(zero_pike$par, X)
d=c(CX0+x,CA,CSigma)

#print(CX0+x)
ZY_2d=funcX(d,X)
lines(X+x,CHANNELS, type='l', col='blue')
lines(X+x, ZY_2d, col='green')
lines(X+x, ZY_3d, col='red')
d
}

ALL_CHANNELS=standard

spec=ALL_CHANNELS
hhh_=max(spec)*0.7
g=NA
plot(ALL_CHANNELS, type='l')


k=7

pikes=data.frame(X0=c(), A=c(), sigma=c())

while (k>0) {
X0_pike=which.max(spec)
A_pike=spec[X0_pike]
A_2_pike=A_pike/2
r=subset(spec, spec > A_2_pike)
i=1
r1=which(r[i]==spec)
while ((X0_pike-r1)>25) {
i=i+1
r1=which(r[i]==spec)
}
r2=(X0_pike-r1)*2
r3=r2/2.355
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
rc=opt_spec(x1)
pikes=data.frame(X0=c(pikes$X0,rc[1]), A=c(pikes$A,rc[2]), sigma=c(pikes$sigma,rc[3]))
spec[x1:y1]=0
k=k-1
}

pikes=pikes[with(pikes, order(X0)),]

print (pikes)

X0_Mo=(max(pikes$X0))
X0_0=(min(pikes$X0))

ChX=c(X0_0, X0_Mo)
ChN=c(0,42)
CheV=line_select(ChN)

ChM0=lm(ChX ~ CheV) # ChX ~ CheV + I(CheV**2) + I(CheV**3)

print (ChM0)

Ev_to_Ch_0 = function(eV) {
   cf=ChM0$coefficients
   eV*cf[2]+cf[1]
}

lll_=length(rel_lines$N)
h_=rep(hhh_, lll_)
h_2=hhh_*(0.5+rnorm(lll_, 0.05, s=0.1))

#ChN=c(0,17,23,74,79,33,42)
ChN=c(0,74)
#ChX=head(pikes$X0, length(ChN))
ChX=head(pikes$X0[c(1,4)], length(ChN))
CheV=line_select(ChN)

ChM=lm(ChX ~ CheV)

print ("Resulting scaling parameters")
print (ChM)

Ev_to_Ch = function(eV) {
   cf=ChM$coefficients
   eV*cf[2]+cf[1]
   # predict
}

lines(Ev_to_Ch(rel_lines$eV), h_, col='dark blue', type='h')
text(Ev_to_Ch(rel_lines$eV), h_2, col='dark red', lab=rel_lines$N)
