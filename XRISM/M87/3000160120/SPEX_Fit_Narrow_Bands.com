#Running a CIE fit
data 3000160120 3000160120
plot dev xs
plot type data
plot x log
plot y log
plot rx 1.5:10.0
plot ry 0.001:10.0
ignore 0:1.5 unit kev
ignore 10.0:100 unit kev
obin 1.5:10.0 unit kev
plot
com reds
#com hot
com cie
#com rel 3 1,2
com rel 2 1
dist 0.00421 z
par 1 z val 0.00421
#par 3 norm val 1000
par 2 norm val 1000
par 2 t val 2.21
par 2 vrms val 70
#par 2 nh val 1.28E-8
#par 2 nh stat f
#par 3 it couple 3 t
#par 3 vrms stat t
#par 3 26 stat t
#par 3 14 stat t
#par 3 16 stat t
#par 3 18 stat t
#par 3 20 stat t
#par 3 28 stat t
par 1 z stat t
par 2 it couple 2 t
par 2 vrms stat t
par 2 sig stat t
par 2 26 val 0.7
par 2 26 stat t
par 2 14 val 1.0
par 2 14 stat t
par 2 16 val 1.0
par 2 16 stat t
par 2 18 val 0.8
par 2 18 stat t
par 2 20 val 0.8
par 2 20 stat t
par 2 28 val 0.7
par 2 28 stat t

log out spex_results_1t overwrite

fit
fit
plot
fit
fit
fit
fit

error 2 t

par 2 t stat f
#par 2 norm stat f
#par 1 z stat f
plot dev cps 3000160120_1t_fit_1p5to10_narrowband.ps


ignore 0:6 unit kev
ignore 7:100 unit kev
obin 1.5:10.0 unit kev

par 2 14 stat f
par 2 16 stat f
par 2 18 stat f
par 2 20 stat f
par 2 28 stat f
par 2 vrms val 70
par 2 vrms stat t
fit
plot rx 6:7
plot

log exe spex_errors_Fe

ignore 0:7 unit kev
use 1.8:2.4 unit kev
obin 1.5:11.0 unit kev
par 2 26 stat f
par 2 14 stat t
par 2 vrms val 70
par 2 vrms stat t
fit
plot rx 1.8:2.4
plot

log exe spex_errors_Si


ignore 0:2.4 unit kev
use 2.38:2.8 unit kev
obin 1.5:11.0 unit kev
par 2 14 stat f
par 2 16 stat t
par 2 vrms val 70
par 2 vrms stat t
fit
plot rx 2.38:2.8
plot

log exe spex_errors_S


ignore 0:3.0 unit kev
use 3.0:3.6 unit kev
obin 1.5:11.0 unit kev
par 2 16 stat f
par 2 18 stat t
par 2 vrms val 70
par 2 vrms stat t
fit
plot rx 3.0:3.6
plot

log exe spex_errors_Ar


ignore 0:3.7 unit kev
use 3.7:4.7 unit kev
obin 1.5:11.0 unit kev
par 2 18 stat f
par 2 20 stat t
par 2 vrms val 70
par 2 vrms stat t
fit

plot rx 3.7:4.7
plot

log exe spex_errors_Ca


ignore 0:7.4 unit kev
use 7.4:8.2 unit kev
obin 1.5:11.0 unit kev
par 2 20 stat f
par 2 28 stat t
par 2 vrms val 70
par 2 vrms stat t
fit
plot rx 7.4:8.2
plot

log exe spex_errors_Ni


par 2 28 stat f
use 1.5:11 unit kev
obin 1.5:11.0 unit kev
par 2 vrms val 70
par 2 vrms stat t
fit
plot rx 1.5:11
plot

log close output

log exe spex_errors_1t
