## Run this file after spex_fit_1t.com, but in the same session.
log out spex_results_Narrow_bands append
# Calculate errors
error 1 z
#error 2 norm
#error 2 t
error 2 vrms
error 2 28
#error 3 norm
#error 3 gamm
log close output
