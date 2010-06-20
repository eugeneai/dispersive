# some definitions
ZC=88
FWHM=0.138
sigma = FWHM / 2.35482
sig_lim = 10
SC = 20/(4096-zero_c)
l5_9=5.92/sc

cols=colors()
X = c(0:4095)
Z = X * 0
O = Z + 1

gauss = function(x, x0=l5_9, A=1.0, sc=SC, zc=ZC) {
    A*exp(-((x-(x0+zc))*sc)**2/(2*sigma**2))
};

mask = function(chan, level=0.01) {
    l = chan>level
    idx = X[l]+1
    r = Z
    r[idx]=1.0
    r
}

GT=gauss(X, l5_9, 2000000, sc=sc)
