# some definitions
zero_c=88
FWHM=0.138
sigma = FWHM / 2.35482
sig_lim = 10
sc = 20/(4096-zero_c)
l5_9=5.92/sc
gauss = function(x, x0, A, sc=sc, zc=zero_c) {
    A*exp(-((x-(x0+zc))*sc)**2/(2*sigma**2))
};

cols=colors()
X = c(0:4095)
