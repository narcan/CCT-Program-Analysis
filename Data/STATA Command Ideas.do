//trend analysis for the means by cctcountry
preserve
collapse fgt0ppp2pcchange, by(cctcountry year)
separate fgt0ppp2pcchange, by(cctcountry)
twoway connected fgt0ppp2pcchange0-fgt0ppp2pcchange1 yearfromcct, scheme(s1color) yla(,nogrid) ytitle("FGT 0") legend(size(vsmall))
restore


//Generate Summary Statistics for Brazil and a few others...
//list year educhildout eduprogresssecondary edulit medmeaimmuinfant medmortinfant govgini if country=="Brazil"
//eststo clear
//eststo: reg educhildout year if country=="Brazil"
//eststo: reg eduprogresssecondary year if country=="Brazil"
//eststo: reg edulit year if country=="Brazil"
//eststo: reg medmeaimmuinfant year if country=="Brazil"
//eststo: reg medmortinfant year if country=="Brazil"
//eststo: reg govgini year if country=="Brazil"
//esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/TA-VarReg-BRA.csv", replace nonumber mtitles("#Children out of School" "%Children Progressing to Secondary Edu" "Literacy Rate" "%Children Immunized against Measles" "Infant Mortality Rate" "GINI Coefficient")
//esttab
// nonumber mtitles("#Children out of School" "%Children Progressing to Secondary Edu" "Literacy Rate" "%Children Immunized against Measles" "Infant Mortality Rate" "GINI Coefficient")

//Generate Summary Statistics for CCTcountry level analysis...
//estpost ttest fgt0ppp2 year, by(cctcountry)
//esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/TA-Ttest.txt", wide nonumber mtitle("CCT Difference")

//Graph fgt0ppp2 by countries with CCTs over years
//preserve//collapse fgt0ppp2, by(country year cctcountry)
//separate fgt0ppp2, by(country)//twoway connected fgt0ppp21-fgt0ppp220 year if cctcountry==1, scheme(s1color) yla(,nogrid) ytitle("FGT 0") legend(size(vsmall))
//graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/FGT0ByCCTCountry01-20.png", replace
//twoway connected fgt0ppp221-fgt0ppp240 year if cctcountry==1, scheme(s1color) yla(,nogrid) ytitle("FGT 0") legend(size(vsmall))
//graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/FGT0ByCCTCountry21-40.png", replace
//twoway connected fgt0ppp241-fgt0ppp260 year if cctcountry==1, scheme(s1color) yla(,nogrid) ytitle("FGT 0") legend(size(vsmall))
//graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/FGT0ByCCTCountry41-60.png", replace
//twoway connected fgt0ppp261-fgt0ppp269 year if cctcountry==1, scheme(s1color) yla(,nogrid) ytitle("FGT 0") legend(size(vsmall))
//graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/FGT0ByCCTCountry61-69.png", replace

//twoway connected fgt0ppp21-fgt0ppp220 year if cctcountry==0, scheme(s1color) yla(,nogrid) ytitle("FGT 0") legend(size(vsmall))
//graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/FGT0ByNonCCTCountry01-20.png", replace
//twoway connected fgt0ppp221-fgt0ppp240 year if cctcountry==0, scheme(s1color) yla(,nogrid) ytitle("FGT 0") legend(size(vsmall))
//graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/FGT0ByNonCCTCountry21-40.png", replace
//twoway connected fgt0ppp241-fgt0ppp260 year if cctcountry==0, scheme(s1color) yla(,nogrid) ytitle("FGT 0") legend(size(vsmall))
//graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/FGT0ByNonCCTCountry41-60.png", replace
//twoway connected fgt0ppp261-fgt0ppp268 year if cctcountry==0, scheme(s1color) yla(,nogrid) ytitle("FGT 0") legend(size(vsmall))
//graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/FGT0ByNonCCTCountry61-69.png", replace

restore

//Make a spline
//mkspline year1 1993 year2 2003 year3 = year
//reg fgt0ppp2 year1 year2 year3
//predict xb//sort year//egen meanfgt0ppp2 = mean(fgt0ppp2), by(year)
//Graph the fitted linear regression line for the means (GraphE-SplineRegression)
//graph twoway (line fgt0ppp2 xb year) (scatter fgt0ppp2 year) if year>=1980 & country=="Brazil", scheme(s1color) yla(,nogrid) xsize(2) ysize(1) ytitle("Confidence in Financial Institutions") xtitle("GSS Year for Respondant")

//Test for Heteroskedasticity - hettest
//Use Robust Standard Errors to relax the assumption that the errors are identically distributed
//Use Clustered Standard Errors to relax the assumption that the errors are independently distributed
//predxcon nconlegis, xvar(year) f(1973) t(2010) i(1) graph class(npartyid) scheme(s1mono) yla(,nogrid) xsize(3.5) ysize(2) m(o i s) color(navy grey maroon) legend(cols(3))
//graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/4016 - Time Series/Labs/Lab01/GraphB.png", replace
