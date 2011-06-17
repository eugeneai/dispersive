X=0:4095
X=0:2000
X0=97.7
fw0=16
XFe=1376.33
fwFe=20.697
AFe=17625.62
x0Fe=6.4
x0=0.

SC=(XFe-X0)/(x0Fe-x0)
Z=X0

FWHM=0.48
first=T

gauss = function(x0, A, fwhm) {
        sigma = (fwhm * SC / 2.35482)
        A * exp(-((X-(x0 * SC + Z))**2/(2*sigma**2)))
};

plt_seq = function(x0, A, c, col='black', fwhm=FWHM, p=F) {
	l = length(x0)
	s=0
	for (i in 1:l) {
		k=gauss(x0[i], A*c[i], fwhm)
		s=s+k
		if (p) {
			if (first) {
				plot(k, col=col, type='l')
				first=F
			} else {
				lines(k, col=col)
			}
		}
	}
	#lines(s, col=col)
	s
}

#G1 = gauss(6.7, 1024, 0.18)

png('aa.png')
first=T

s1=plt_seq(c(6.7, 3.2, 1.1), 1, c(1,0.5, 0.1), col='blue')
s2=plt_seq(c(2.2, 5, 6.5), 0.7, c(1,0.7, 0.3), col='red')

s=s1+s2
plot(s, type='l')
first=F

s1=plt_seq(c(6.7, 3.2, 1.1), 1, c(1,0.5, 0.1), col='blue', p=T)
s2=plt_seq(c(2.2, 5, 6.5), 0.7, c(1,0.7, 0.3), col='red', p=T)

#plot(X, G1, type='l', col='red')
lines(s)

dev.off()


