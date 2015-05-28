#setwd('C:/new3')
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

opt_spec <- function(x) {

  g<<-1
  pike1=optim(c(CSigma,CA), dif_spec1, gr=NULL,
    method = c("Nelder-Mead"),
    lower = -Inf, upper = Inf,
    control = list(maxit=500), hessian = F
    )
  CSigma<<-pike1$par[1]
  CA<<-pike1$par[2]

  g<<-2
  pike2=optim(c(CX0,CA), dif_spec1, gr=NULL,
    method = c("Nelder-Mead"),
    lower = -Inf, upper = Inf,
    control = list(maxit=500), hessian = F
  )
  CX0<<-pike2$par[1]
  CA<<-pike2$par[2]

  g<<-3
  pike3=optim(c(CSigma,CX0), dif_spec1, gr=NULL,
    method = c("Nelder-Mead"),
    lower = -Inf, upper = Inf,
    control = list(maxit=500), hessian = F
  )
  CSigma<<-pike3$par[1]
  CX0<<-pike3$par[2]

  zero_pike=optim(c(CX0,CA,CSigma), dif_spec, gr=NULL,
    method = c("Nelder-Mead"),
    lower = -Inf, upper = Inf,
    control = list(maxit=500), hessian = F
  )
  CX0<<-zero_pike$par[1]
  CA<<-zero_pike$par[2]
  CSigma<<-zero_pike$par[3]

  ZY_3d=funcX(zero_pike$par, X)
  d=c(CX0+x,CA,CSigma)

  #print(CX0+x)
  ZY_2d=funcX(d,X)
  lines(X+x,CHANNELS, type='l', col='blue')
  #lines(X+x, ZY_2d, col='green')
  lines(X+x, ZY_3d, col='red')
  d
}

ALL_CHANNELS=standard

g=NA
CX0=NA
CA=NA
CSigma=NA
pikes=data.frame(X0=c(), A=c(), sigma=c())
k=TRUE
spec=ALL_CHANNELS
#X=0:(length(spec)-1)
png(file = "approx_all.png",
  width     = 3.25,
  height    = 3.25,
  units     = "in",
  res       = 1200,
  pointsize = 4)
plot(spec,type='l')
X0_pike=which.max(spec)
A_prev=spec[X0_pike]


aaa <- function(spec) {
  while (k==TRUE) {
    X0_pike=which.max(spec)
    A_pike=spec[X0_pike]
    #print(A_pike/A_prev)
    if ((A_pike/A_prev)>0.5)
    {
      A_2_pike=A_pike/2
      r=subset(spec, spec > A_2_pike)
      i=1
      r1=which(r[i]==spec)
      while ((X0_pike-r1)>65) {
        i=i+1
        r1=which(r[i]==spec)
      }
      r2=(X0_pike-r1)*2
      r3=r2/2.355
      #r3=20.68787
      x1=(X0_pike-r3*3.5)
      y1=(X0_pike+r3*3.5)

      CHANNELS<<-spec[x1:y1]
      X<<-0:(length(CHANNELS)-1)
      CX0<<-which.max(CHANNELS)

      CA<<-CHANNELS[CX0]
      A_prev<<-CA
      CA_2=CA/2
      t=subset(CHANNELS, CHANNELS > CA_2)
      t1=which(t[1]==CHANNELS)
      t2=(CX0-t1)*2
      t3=t2/2.355
      CSigma<<-t3
      #rc=opt_spec(x1+3000)
      rc=opt_spec(x1)
      pikes<<-data.frame(X0=c(pikes$X0,rc[1]), A=c(pikes$A,rc[2]), sigma=c(pikes$sigma,rc[3]))
      #print(rc)
      spec[x1:y1]=0

      #X=0:(length(spec)-1)
      #spec=spec-funcX(c(rc[1],rc[2],abs(rc[3])),X)
    }
    else {k=FALSE}
  }

}



aaa(spec)
pikes=pikes[with(pikes, order(X0)),]
print (pikes)

X0_Mo=(max(pikes$X0))
X0_0=(min(pikes$X0))
ChX=c(X0_0, X0_Mo)
ChN=c(0,42)
CheV=line_select(ChN)
ChM0=lm(ChX ~ CheV)
print (ChM0)

Ev_to_Ch_0 = function(eV) {
  cf=ChM0$coefficients
  eV*cf[2]+cf[1]
}

lll_=length(rel_lines$N)
hhh_=max(ALL_CHANNELS)*0.7
h_=rep(hhh_, lll_)
h_2=hhh_*(0.5+rnorm(lll_, 0.05, s=0.1))

ChN=c(0,17,23,74,79,33,42)
ChX=head(pikes$X0, length(ChN))
CheV=line_select(ChN)
ChM=lm(ChX ~ CheV)
print ("Resulting scaling parameters - X0")
print (ChM)

Ev_to_Ch = function(eV) {
  cf=ChM$coefficients
  eV*cf[2]+cf[1]
}

lines(Ev_to_Ch_0(rel_lines$eV), h_, col='green', type='h')
lines(Ev_to_Ch(rel_lines$eV), h_, col='dark blue', type='h')
text(Ev_to_Ch(rel_lines$eV), h_2, col='dark red', lab=rel_lines$N)
dev.off()

SigN=c(0,17,23,74)
SigX=head(abs(pikes$sigma), length(SigN))
SigeV=line_select(SigN)
SigM=lm(SigX ~ SigeV + I(sqrt(SigeV)))
print ("Resulting scaling parameters - Sigma")
print (SigM)

Ev_to_Sig = function(eV) {
  cf=SigM$coefficients
  cf[1] + eV*cf[2] + sqrt(eV)*cf[3]
}

lines_=line_select(ChN)
print(lines_)
evSig=Ev_to_Sig(lines_)
evCh0=Ev_to_Ch_0(lines_)
evCh=Ev_to_Ch(lines_)
pikes$N=ChN
pikes$evSig=evSig
pikes$evCh0=evCh0
pikes$evCh=evCh
print(pikes)

copy_pikes=pikes
spec=ALL_CHANNELS[3000:4096]
k=TRUE
g=NA
CX0=NA
CA=NA
CSigma=NA
X1=0:(length(spec)-1)
spec1=spec-funcX(c(pikes$evCh[nrow(pikes)]-3000,pikes$A[nrow(pikes)],pikes$evSig[nrow(pikes)]),X1)
X0_pike=which.max(spec1)
A_prev=spec1[X0_pike]
png(file = "approx_R&C.png",
  width     = 3.25,
  height    = 3.25,
  units     = "in",
  res       = 1200,
  pointsize = 4)
plot(spec,type='l',col='green') # Spectrum
lines(spec1,type='l')           #Wo Mo (42) ?
pikes=data.frame(X0=c(), A=c(), sigma=c())
aaa(spec1)
pikes=pikes[with(pikes, order(X0)),]
print ("Pikes in the 3000:etc localities")
print(pikes)

copy_pikes2=pikes
spec=ALL_CHANNELS[3000:4096]
k=TRUE
g=NA
CX0=NA
CA=NA
CSigma=NA
X1=0:(length(spec)-1)
spec1=spec-funcX(c(pikes$X0[nrow(pikes)],pikes$A[nrow(pikes)],pikes$sigma[nrow(pikes)]),X1)
lines(spec1,type='l',col='yellow')   # Looks like Zr (40)
X0_pike=which.max(spec1)
A_prev=spec1[X0_pike]
pikes=data.frame(X0=c(), A=c(), sigma=c())
aaa(spec1)
pikes=pikes[with(pikes, order(X0)),]
print("Pikes in the Coumpton localitiy:")
print(pikes)
dev.off()

result=funcX(c(pikes$X0[nrow(pikes)],pikes$A[nrow(pikes)],pikes$sigma[nrow(pikes)]),X1)+ # Releigh
   funcX(c(copy_pikes2$X0[nrow(copy_pikes2)],copy_pikes2$A[nrow(copy_pikes2)],copy_pikes2$sigma[nrow(copy_pikes2)]),X1) # Cou
png(file = "result_R&C.png",
  width     = 3.25,
  height    = 3.25,
  units     = "in",
  res       = 1200,
  pointsize = 4)
plot(spec,type='l',col='blue')
lines(result,type='l',col='red')
dev.off()

result=result + funcX(c(copy_pikes2$X0[1],copy_pikes2$A[1],copy_pikes2$sigma[1]),X1)

png(file = "result_R&C&Zr.png",
  width     = 3.25,
  height    = 3.25,
  units     = "in",
  res       = 1200,
  pointsize = 4)
plot(spec,type='l',col='blue')
lines(result,type='l',col='red')
dev.off()



