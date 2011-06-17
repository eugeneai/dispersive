X=0:4095
X0=97.7
fw0=16
XFe=1376.33
fwFe=20.697
AFe=17625.62
x0Fe=6.4
x0=0.

SC=(XFe-X0)/(x0Fe-x0)
Z=X0

gauss = function(x0, A, fwhm) {
        sigma = (fwhm * SC / 2.35482)
        A * exp(-((X-(x0 * SC + Z))**2/(2*sigma**2)))
};

G1 = gauss(6.7, 1024, 0.18)

png('aa.png')

plot(X, G1, type='l', col='red')

dev.off()


