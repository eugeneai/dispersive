source('global.R')

STEP=FWHM/4.0/sc

find_pike = function (start_x0, spectrum, step=STEP, channels=10*FWHM/sc, eps=1.0, plot=FALSE, fit_fwhm=TRUE) {
    x0 = start_x0
    term_x = x0 + channels
    p_sg = 1e38
    s = step
    f = list()
    phase = 'raw'
    repeat {
        if (x0>term_x) {
           f$found=FALSE
           break;
        }
        g = gauss(X,x0=x0, zc=0, A=1, sc=sc)
        if (phase=='prec') {
           mm = mask(g, level=0.001)
           fm = spectrum ~ g + 0
        } else {
           mm = O
           fm = spectrum ~ g
        }
        f = lm(fm, weights=mm)
        cfs = f$coefficients
        if (length(cfs)==2) { 
           a = cfs[2] 
           b = cfs[1]
        } else {
           a = cfs[1]
           b = 0
        }
        #print (f)
        sm = summary(f)
        sg = sm$sigma
        print (c(a, sg, x0, s, b))
        if ((b>=0 || phase=='prec') && a>0){ 
           if (sg > p_sg)
              s = -s/2.0
        }
        x0 = x0 + s
        #print (mm)
        if (a>0 && abs(sg-p_sg)<eps) {
            if (phase=='prec') {
               f$found=TRUE
               f$mask = mm
               f$sigma = sg
               break;
            }
            phase='prec'
            print ('change phase')
            term_x=x0+step*2
            s=step
            x0=x0-s
            p_sg = 1e38
            next
        }
        p_sg = sg
    }
    if (f$found) {
        
    }
    f$x0 = x0
    f$A = a
    f$b = b
    f$fwhm = FWHM
    p_sg = 1e38
    if (f$found && fit_fwhm) {
       s = FWHM/8.0
       fwhm = FWHM
       print ('Fit fwhm')
       repeat {
           g = gauss(X,x0=x0, zc=0, A=1, sc=sc, fwhm=fwhm)
           fm = spectrum ~ g # + 0
           fw = lm (fm, weights = f$mask)
           cfs = fw$coefficients
           if (length(cfs)==2) { 
              a = cfs[2] 
              b = cfs[1]
           } else {
              a = cfs[1]
              b = 0
           }
           sm = summary(fw)
           sg = sm$sigma
           if (sg > p_sg) {
              s = -s/2.0
           }
           print (c(a, sg, p_sg, fwhm))
           if (abs(sg-p_sg)<eps) {
              f$fwhm = fwhm
              f$A = a
              f$b = b
              f$sigma = sg
              break
           }
           fwhm = fwhm + s
           p_sg = sg
       }
    }
    if (plot && f$found) {
        g = gauss(X, f$x0, A=f$A, zc=0., sc=SC, fwhm=f$fwhm)+f$b
        plot(X, g, type='l')
        lines(X, spectrum, type='l', col='red')
    }
    f
}
