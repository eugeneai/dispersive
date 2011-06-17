# some definitions
ZC=96
FWHM=0.138
sig_lim = 10
SC = 20/(4096-ZC)
l5_9=5.92/SC
Nchan=4096

cols=colors()
chan.nos = c(0:(Nchan-1))

X=0:(Nchan-1)

Z = X * 0
O = Z + 1

gauss = function(x, x0=l5_9, A=1.0, sc=SC, zc=ZC, fwhm=FWHM) {
    sigma = fwhm / 2.35482
    A*exp(-((x-(x0+zc))*sc)**2/(2*sigma**2))
};

mask = function(chan, level=0.001) {
    l = chan>level
    idx = X[l]+1
    r = Z
    r[idx]=1.0
    r
}

GT=gauss(X, l5_9, 2000000, sc=SC)

scale_X = function(X, sc=SC, zc=ZC) {
    (X-zc) * sc
}
