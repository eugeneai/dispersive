source('global.R')

STEP=FWHM/4.0/sc

find_pike = function (start_x0, spectrum, step=STEP, channels=10*FWHM/sc, eps=1.0, plot=FALSE) {
    x0 = start_x0
    term_x = x0 + channels
    p_a = -1e38
    s = step
    f = list()
    repeat {
        if (x0>term_x) {
           f$found=FALSE
           break;
        }
        g = gauss(X,x0=x0, zc=0, A=1, sc=sc)
        #mm = mask(g, level=0.01)
        f = lm(spectrum ~ g, weights=O)
        a = f$coefficients[2]
        b = f$coefficients[1]
        if (b>0 && a>0){ 
           if (a<p_a)
              s = -s/2.0
        }
        x0 = x0 + s
        print (c(a, p_a, x0, s, b))
        #print (mm)
        if (abs(a-p_a)<eps) {
            f$found=TRUE
            break;
        }
        p_a = a
    }
    if (f$found) {
        
    }
    f$x0 = x0
    f$A = a
    f$b = b
    if (plot && f$found) {
        g = gauss(X, f$x0, A=f$A, zc=0., sc=SC)+f$b
        plot(X, g, type='l')
        lines(X, spectrum, type='l', col='red')
    }
    f
}
