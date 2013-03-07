x=seq(-20,20, by=0.01)

func <- function(x0,A,sigma) {
     exp(-((x-x0)^2/(2*sigma^2)))*sqrt(2*pi)*A
     }

funcX <- function(b, X) {
     x0=b[1]
     A=b[2]
     sigma=b[3]
     exp(-((X-x0)^2/(2*sigma^2)))*sqrt(2*pi)*A
     }

func2 <- function(x0,A,sigma,x0_2,A_2,sigma_2) {
	w=(exp(-((x-x0)^2/(2*sigma^2)))*sqrt(2*pi)*A)
	v=(exp(-((x-x0_2)^2/(2*sigma_2^2)))*sqrt(2*pi)*A_2)
	w+v
	}

y=func(0,10,5)

z=func2(6,1,5,-6,1.25,4)

#w=func(6,1,5)
#v=func(-6,1.25,4)
#plot(z)
#lines(w,col='red')
#lines(v,col='blue')

dif <- function(b) {
	x0=b[1]
	A=b[2]
	sigma=b[3]
	sum((y-func(x0,A,sigma))^2)
}

rc=optim(c(-0.05,9.95,4.95), dif, gr = NULL,
	method = c("Nelder-Mead"),
 	lower = -Inf, upper = Inf,
	control = list(maxit=5000), hessian = F)

f_x0=rc$par[1]
f_A=rc$par[2]
f_sigma=rc$par[3]
png(file = "func.png")
plot(x, func(f_x0,f_A,f_sigma))
lines(x, y, col='red')
dev.off()

dif2 <- function(b) {
	x0=b[1]
	A=b[2]
	sigma=b[3]
	x0_2=b[4]
	A_2=b[5]
	sigma_2=b[6]
	sum((z-func2(x0,A,sigma,x0_2,A_2,sigma_2))^2)
}

source('scaling.R')

dif_spec <- function(b) {
        X=0:(length(CHANNELS)-1)
	sum((CHANNELS-funcX(b, X))^2)
}



if (0) {
   rc2=optim(c(5.95,0.95,4.95,-5.95,1.2,3.95), dif2, gr = NULL,
   method = c("Nelder-Mead"),
   lower = -Inf, upper = Inf,
   control = list(maxit=5000), hessian = F)

   f2_x0=rc2$par[1]
   f2_A=rc2$par[2]
   f2_sigma=rc2$par[3]
   f2_x0_2=rc2$par[4]
   f2_A_2=rc2$par[5]
   f2_sigma_2=rc2$par[6]
   png(file = "func2.png")
   plot(x,func2(f2_x0,f2_A,f2_sigma,f2_x0_2,f2_A_2,f2_sigma_2))
   lines(x, z, col='red')
   dev.off()
}


# Дальнейший текст переделать в функцию.
ALL_CHANNELS=standard
CHANNELS=ALL_CHANNELS[1:150]
CX0=which.max(CHANNELS)
CA=CHANNELS[CX0]
zero_pike=optim(c(CX0,CA,1.), dif_spec, gr=NULL,
   method = c("Nelder-Mead"),
   lower = -Inf, upper = Inf,
   control = list(maxit=5000), hessian = F)

print(zero_pike)

X=0:(length(CHANNELS)-1)
AX=0:(length(ALL_CHANNELS)-1)
ZY=funcX(zero_pike$par, X)
AZY=funcX(zero_pike$par, AX)
plot(ALL_CHANNELS, type='l', col='blue')
lines(ALL_CHANNELS-AZY, col='green')
lines(ZY, col='red')
