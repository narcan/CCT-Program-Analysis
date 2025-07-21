# Pedro Ávila - Spring 2012 QMSS 5999 Thesis
# Dataset Analysis for CCT Investigation
#--------------------------------------------------Arrange the environment

#clear
#set more off
#eststo clear

#get variables from data file
ThesisData->read.csv("/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Data/ThesisDataCSV.csv")

#Set the ThesisData data frame as the default dataframe
attach(ThesisData)
#--------------------------------------------------Summary Stats
#Rates of Change in Poverty

summary(govgdpppp[which(country=="Brazil")])

sum rcgovgdpppp rcfgt0 rcfgt1 if country=="Brazil"
sum rcgovgdpppp rcfgt0 rcfgt1 if country=="Mexico"
sum rcgovgdpppp rcfgt0 rcfgt1 if country=="Chile"
sum rcgovgdpppp rcfgt0 rcfgt1 if country=="Jamaica"
sum rcgovgdpppp rcfgt0 rcfgt1 if country=="Nicaragua"
sum rcgovgdpppp rcfgt0 rcfgt1 if eventualcct==1 & region=="Latin America"
sum rcgovgdpppp rcfgt0 rcfgt1 if eventualcct==1 & region=="Caribbean"
sum rcgovgdpppp rcfgt0 rcfgt1 if eventualcct==0 & region=="Latin America"
sum rcgovgdpppp rcfgt0 rcfgt1 if eventualcct==0 & region=="Caribbean"
sum rcgovgdpppp rcfgt0 rcfgt1 if eventualcct==0 & region=="West Africa"
sum rcgovgdpppp rcfgt0 rcfgt1 if eventualcct==0 & region=="Sub-Saharan Africa"
sum rcgovgdpppp rcfgt0 rcfgt1 if eventualcct==0 & region=="North Africa"
sum rcgovgdpppp rcfgt0 rcfgt1 if eventualcct==0 & region=="Southeast Asia"
sum rcgovgdpppp rcfgt0 rcfgt1 if eventualcct==0 & region=="Middle East"
sum rcgovgdpppp rcfgt0 rcfgt1 if eventualcct==0 & region=="Eastern Europe"
sum rcgovgdpppp rcfgt0 rcfgt1 if eventualcct==0 & region=="Balkans"

#Poverty Levels in Brazil (*** TABLE ***)
eststo clear
eststo: quietly reg ifgt0 igovgdpppp igovgini year if country=="Brazil", robust
eststo: quietly reg ifgt1 igovgdpppp igovgini year if country=="Brazil", robust
esttab, ar2 nocons nonumber wide mtitles("Brazil FGT0" "Brazil FGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/SUM-FGT-BRA.csv", replace nonumber wide mtitles("Brazil FGT0" "Brazil FGT1")

#Poverty Levels in Brazil (*** GRAPHS ***)
graph twoway line ifgt0 year if country=="Brazil", scheme(s1color) yla(,nogrid) title(Brazil: Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(2003)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/SUM-FGT0-BRA.png", replace

graph twoway line ifgt1 year if country=="Brazil", scheme(s1color) yla(,nogrid) title(Brazil: Depth of Poverty, size(medium)) legend(size(vsmall)) xline(2003)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/SUM-FGT1-BRA.png", replace

#--------------------GDP predicts poverty in Brazil
#Show that the rate of change in GDP is the best predictor of RCFGT0 in this model
eststo clear
eststo: quietly reg rcfgt0 rcgovgdpppp rcgovgini igovgdpppp igovgini year if country=="Brazil", robust
eststo: quietly reg rcfgt0 rcgovgdpppp year if country=="Brazil", robust
eststo: quietly reg rcfgt0 rcgovgini year if country=="Brazil", robust
eststo: quietly reg rcfgt0 igovgdpppp year if country=="Brazil", robust
eststo: quietly reg rcfgt0 igovgini year if country=="Brazil", robust
esttab, ar2 nocons nonumber mtitles("Full Model" "Rate of Change GDP" "Rate of Change Gini" "GDP" "Gini")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/GDP-RCFGT0-BRA.csv", replace nonumber mtitles("Full Model" "Rate of Change GDP" "Rate of Change Gini" "GDP" "Gini")

#Show that the rate of change in GDP is the best predictor of RCFGT1 in this model
eststo clear
eststo: quietly reg rcfgt1 rcgovgdpppp rcgovgini igovgdpppp igovgini year if country=="Brazil", robust
eststo: quietly reg rcfgt1 rcgovgdpppp year if country=="Brazil", robust
eststo: quietly reg rcfgt1 rcgovgini year if country=="Brazil", robust
eststo: quietly reg rcfgt1 igovgdpppp year if country=="Brazil", robust
eststo: quietly reg rcfgt1 igovgini year if country=="Brazil", robust
esttab, ar2 nocons nonumber mtitles("Full Model" "Rate of Change GDP" "Rate of Change Gini" "GDP" "Gini")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/GDP-RCFGT1-BRA.csv", replace nonumber mtitles("Full Model" "Rate of Change GDP" "Rate of Change Gini" "GDP" "Gini")
#--------------------------------------------------

#--------------------------------------------------Naive Analysis of RCFGT (Table & Graphs)
#--------------------NAI RCFGT0
eststo clear
eststo: quietly reg rcfgt0 year if country=="Brazil"
predict natrrcfgt0bra
eststo: quietly reg rcfgt0 year if eventualcct==1 & region=="Latin America"
predict natrrcfgt0lacct
eststo: quietly reg rcfgt0 year if eventualcct==0 & region=="Latin America"
predict natrrcfgt0lancct

#Label prediction Variables
label variable natrrcfgt0bra "Brazil"
label variable natrrcfgt0lacct "Latin American Countries with CCT Programs"
label variable natrrcfgt0lancct "Latin American Countries without CCT Programs"

# *** TABLE ***
  esttab, ar2 nocons nonumber mtitles("Brazil" "Latin America CCT" "Latin America nCCT")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/NAI-RCFGT0.csv", replace nonumber mtitles("Brazil" "Latin America CCT" "Latin America nCCT")

# *** GRAPH ***
  graph twoway (line natrrcfgt0bra natrrcfgt0lacct natrrcfgt0lancct year), scheme(s1color) yla(,nogrid) title(Trends on Rate of Change in Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(2003)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/NAI-Trends-RCFGT0.png", replace

#--------------------NAI RCFGT1
eststo clear
eststo: reg rcfgt1 year if country=="Brazil"
predict natrrcfgt1bra
eststo: reg rcfgt1 year if eventualcct==1 & region=="Latin America"
predict natrrcfgt1lacct
eststo: reg rcfgt1 year if eventualcct==0 & region=="Latin America"
predict natrrcfgt1lancct

#Label prediction variables
label variable natrrcfgt1bra "Brazil"
label variable natrrcfgt1lacct "Latin American Countries with CCT Programs"
label variable natrrcfgt1lancct "Latin American Countries without CCT Programs"

# *** TABLE ***
  esttab, ar2 nocons nonumber mtitles("Brazil" "Latin America CCT" "Latin America nCCT")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/NAI-RCFGT1.csv", replace nonumber mtitles("Brazil" "Latin America CCT" "Latin America nCCT")

# *** GRAPH ***
  graph twoway (line natrrcfgt1bra year) (line natrrcfgt1lacct year) (line natrrcfgt1lancct year), scheme(s1color) yla(,nogrid) title(Trends on Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(2003)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/NAI-Trends-RCFGT1.png", replace

#/--------------------NAI RCFGT (net of GDP & Gini) in Brazil (*** for Tables ***)
eststo clear
eststo: quietly reg rcfgt0 rcgovgdpppp rcgovgini year if country=="Brazil", robust
predict naftrcfgt0bra
eststo: quietly reg rcfgt1 rcgovgdpppp rcgovgini year if country=="Brazil", robust
predict naftrcfgt1bra

#Label prediction variables
label variable naftrcfgt0bra "Poverty Headcount Ratio"
label variable naftrcfgt1bra "Depth of Poverty"

# *** TABLE ***
  esttab, ar2 nocons nonumber mtitles("Brazil RCFGT0" "Brazil RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/RCFGT-BRA.csv", replace nonumber mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------NAI RCFGT (net of GDP & Gini) in Brazil (*** for Graphs ***)
quietly reg rcfgt0 igovgdpppp igovgini year if country=="Brazil", robust
predict naftpsrcfgt0bra
quietly reg rcfgt1 igovgdpppp igovgini year if country=="Brazil", robust
predict naftpsrcfgt1bra
quietly reg rcgovgdpppp year if country=="Brazil", robust
predict naftrcgdpbra

#Label new prediction variables
label variable naftpsrcfgt0bra "Poverty Headcount Ratio"
label variable naftpsrcfgt1bra "Depth of Poverty"
label variable naftrcgdpbra "GDP Trend"

# *** GRAPHS ***
  graph twoway (line rcfgt0 year) (line naftpsrcfgt0bra year) (line naftrcgdpbra year) if country=="Brazil", scheme(s1color) yla(,nogrid) title(Brazil: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(2003)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/NAI-RCFGT0-BRA.png", replace

graph twoway (line rcfgt1 year) (line naftpsrcfgt1bra year) (line naftrcgdpbra year) if country=="Brazil", scheme(s1color) yla(,nogrid) title(Brazil: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(2003)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/NAI-RCFGT1-BRA.png", replace
#/--------------------------------------------------
  
  #/--------------------------------------------------Full Model Analysis (Brazil)
#Make Splines for CCT Stages
mkspline before 1 phase1 2 phase2 = cctstage

#/--------------------RCFGT MODEL in Brazil (*** for Tables ***)
eststo clear
eststo: quietly reg rcfgt0 rcgovgdpppp rcgovgini before phase1 phase2 if country=="Brazil", robust
predict modftrcfgt0bra
eststo: quietly reg rcfgt1 rcgovgdpppp rcgovgini before phase1 phase2 if country=="Brazil", robust
predict modtfrcfgt1bra
quietly reg rcgovgdpppp year if country=="Brazil", robust
predict modrcgdpbra

#Label prediction variables
label variable modftrcfgt0bra "Poverty Headcount Ratio"
label variable modtfrcfgt1bra "Depth of Poverty"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Brazilian Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-BRA.csv", replace nonumber wide title("Brazilian Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

# *** GRAPHS *** (Erratic)
graph twoway (line rcfgt0 year) (line modftrcfgt0bra year) (line modrcgdpbra year) if country=="Brazil", scheme(s1color) yla(,nogrid) title(Brazil: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(2003)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-BRA-ERR.png", replace

graph twoway (line rcfgt1 year) (line modtfrcfgt1bra year) (line modrcgdpbra year) if country=="Brazil", scheme(s1color) yla(,nogrid) title(Brazil: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(2003)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-BRA-ERR.png", replace

#/--------------------RCFGT MODEL in Brazil (*** for Graphs ***)
quietly reg rcfgt0 igovgdpppp igovgini before phase1 phase2 if country=="Brazil", robust
predict modpsrcfgt0bra
quietly reg rcfgt1 igovgdpppp igovgini before phase1 phase2 if country=="Brazil", robust
predict modpsrcfgt1bra
quietly reg rcgovgdpppp year if country=="Brazil", robust
predict modpsrcgdpbra

#Label new prediction variables
label variable modpsrcfgt0bra "Poverty Headcount Ratio"
label variable modpsrcfgt1bra "Depth of Poverty"
label variable modpsrcgdpbra "GDP Trend"

# *** GRAPHS ***
  graph twoway (line modpsrcfgt0bra year) (line modpsrcgdpbra year) if country=="Brazil", scheme(s1color) yla(,nogrid) title(Brazil: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(2003)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-BRA.png", replace

graph twoway (line modpsrcfgt1bra year) (line modpsrcgdpbra year) if country=="Brazil", scheme(s1color) yla(,nogrid) title(Brazil: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(2003)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-BRA.png", replace
#/--------------------------------------------------
  
  #/--------------------------------------------------Full Model Analysis (Mexico)
#/--------------------RCFGT MODEL in Mexico (*** for Tables ***)
eststo clear
eststo: quietly reg rcfgt0 rcgovgdpppp rcgovgini before phase1 phase2 if country=="Mexico", robust
predict modftrcfgt0mex
eststo: quietly reg rcfgt1 rcgovgdpppp rcgovgini before phase1 phase2 if country=="Mexico", robust
predict modtfrcfgt1mex
quietly reg rcgovgdpppp year if country=="Mexico", robust
predict modrcgdpmex

#Label prediction variables
label variable modftrcfgt0mex "Poverty Headcount Ratio"
label variable modtfrcfgt1mex "Depth of Poverty"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Mexican Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-MEX.csv", replace nonumber wide title("Mexican Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT MODEL in Mexico (*** for Graphs ***)
quietly reg rcfgt0 igovgdpppp igovgini before phase1 phase2 if country=="Mexico", robust
predict modpsrcfgt0mex
quietly reg rcfgt1 igovgdpppp igovgini before phase1 phase2 if country=="Mexico", robust
predict modpsrcfgt1mex
quietly reg rcgovgdpppp year if country=="Mexico", robust
predict modpsrcgdpmex

#Label new prediction variables
label variable modpsrcfgt0mex "Poverty Headcount Ratio"
label variable modpsrcfgt1mex "Depth of Poverty"
label variable modpsrcgdpmex "GDP Trend"

# *** GRAPHS ***
  graph twoway (line modpsrcfgt0mex year) (line modpsrcgdpmex year) if country=="Mexico", scheme(s1color) yla(,nogrid) title(Mexico: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(1997)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-MEX.png", replace

graph twoway (line modpsrcfgt1mex year) (line modpsrcgdpmex year) if country=="Mexico", scheme(s1color) yla(,nogrid) title(Mexico: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(1997)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-MEX.png", replace
#/--------------------------------------------------
  
  #/--------------------------------------------------Full Model Analysis (Chile)
#/--------------------RCFGT MODEL in Chile (*** for Tables ***)
eststo clear
eststo: quietly reg rcfgt0 rcgovgdpppp rcgovgini before phase1 phase2 if country=="Chile", robust
predict modftrcfgt0chl
eststo: quietly reg rcfgt1 rcgovgdpppp rcgovgini before phase1 phase2 if country=="Chile", robust
predict modtfrcfgt1chl
quietly reg rcgovgdpppp year if country=="Chile", robust
predict modrcgdpchl

#Label prediction variables
label variable modftrcfgt0chl "Poverty Headcount Ratio"
label variable modtfrcfgt1chl "Depth of Poverty"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Chilean Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-CHL.csv", replace nonumber wide title("Chilean Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT MODEL in Chile (*** for Graphs ***)
quietly reg rcfgt0 igovgdpppp igovgini before phase1 phase2 if country=="Chile", robust
predict modpsrcfgt0chl
quietly reg rcfgt1 igovgdpppp igovgini before phase1 phase2 if country=="Chile", robust
predict modpsrcfgt1chl
quietly reg rcgovgdpppp year if country=="Chile", robust
predict modpsrcgdpchl

#Label new prediction variables
label variable modpsrcfgt0chl "Poverty Headcount Ratio"
label variable modpsrcfgt1chl "Depth of Poverty"
label variable modpsrcgdpchl "GDP Trend"

# *** GRAPHS ***
  graph twoway (line modpsrcfgt0chl year) (line modpsrcgdpchl year) if country=="Chile", scheme(s1color) yla(,nogrid) title(Chile: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(2002)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-CHL.png", replace

graph twoway (line modpsrcfgt1chl year) (line modpsrcgdpchl year) if country=="Chile", scheme(s1color) yla(,nogrid) title(Chile: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(2002)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-CHL.png", replace
#/--------------------------------------------------
  
  #/--------------------------------------------------Full Model Analysis (Jamaica)
#/--------------------RCFGT MODEL in Jamaica (*** for Tables ***)
eststo clear
eststo: quietly reg rcfgt0 rcgovgdpppp rcgovgini before phase1 phase2 if country=="Jamaica", robust
predict modftrcfgt0jam
eststo: quietly reg rcfgt1 rcgovgdpppp rcgovgini before phase1 phase2 if country=="Jamaica", robust
predict modtfrcfgt1jam
quietly reg rcgovgdpppp year if country=="Jamaica", robust
predict modrcgdpjam

#Label prediction variables
label variable modftrcfgt0jam "Poverty Headcount Ratio"
label variable modtfrcfgt1jam "Depth of Poverty"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Jamaican Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-JAM.csv", replace nonumber wide title("Jamaican Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT MODEL in Jamaica (*** for Graphs ***)
quietly reg rcfgt0 igovgdpppp igovgini before phase1 phase2 if country=="Jamaica", robust
predict modpsrcfgt0jam
quietly reg rcfgt1 igovgdpppp igovgini before phase1 phase2 if country=="Jamaica", robust
predict modpsrcfgt1jam
quietly reg rcgovgdpppp year if country=="Jamaica", robust
predict modpsrcgdpjam

#Label new prediction variables
label variable modpsrcfgt0jam "Poverty Headcount Ratio"
label variable modpsrcfgt1jam "Depth of Poverty"
label variable modpsrcgdpjam "GDP Trend"

# *** GRAPHS ***
  graph twoway (line modpsrcfgt0jam year) (line modpsrcgdpjam year) if country=="Jamaica", scheme(s1color) yla(,nogrid) title(Jamaica: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(2001)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-JAM.png", replace

graph twoway (line modpsrcfgt1jam year) (line modpsrcgdpjam year) if country=="Jamaica", scheme(s1color) yla(,nogrid) title(Jamaica: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(2001)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-JAM.png", replace
#/--------------------------------------------------
  
  #/--------------------------------------------------Full Model Analysis (Nicaragua)
#/--------------------RCFGT MODEL in Nicaragua (*** for Tables ***)
eststo clear
eststo: quietly reg rcfgt0 rcgovgdpppp rcgovgini before phase1 phase2 if country=="Nicaragua", robust
predict modftrcfgt0nic
eststo: quietly reg rcfgt1 rcgovgdpppp rcgovgini before phase1 phase2 if country=="Nicaragua", robust
predict modtfrcfgt1nic
quietly reg rcgovgdpppp year if country=="Nicaragua", robust
predict modrcgdpnic

#Label prediction variables
label variable modftrcfgt0nic "Poverty Headcount Ratio"
label variable modtfrcfgt1nic "Depth of Poverty"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Nicaraguan Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-NIC.csv", replace nonumber wide title("Nicaraguan Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT MODEL in Nicaragua (*** for Graphs ***)
quietly reg rcfgt0 igovgdpppp igovgini before phase1 phase2 if country=="Nicaragua", robust
predict modpsrcfgt0nic
quietly reg rcfgt1 igovgdpppp igovgini before phase1 phase2 if country=="Nicaragua", robust
predict modpsrcfgt1nic
quietly reg rcgovgdpppp year if country=="Nicaragua", robust
predict modpsrcgdpnic

#Label new prediction variables
label variable modpsrcfgt0nic "Poverty Headcount Ratio"
label variable modpsrcfgt1nic "Depth of Poverty"
label variable modpsrcgdpnic "GDP Trend"

# *** GRAPHS ***
  graph twoway (line modpsrcfgt0nic year) (line modpsrcgdpnic year) if country=="Nicaragua", scheme(s1color) yla(,nogrid) title(Nicaragua: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(2000)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-NIC.png", replace

graph twoway (line modpsrcfgt1nic year) (line modpsrcgdpnic year) if country=="Nicaragua", scheme(s1color) yla(,nogrid) title(Nicaragua: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(2000)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-NIC.png", replace
#/--------------------------------------------------
  
  #/--------------------------------------------------Full Model Analysis (CCT Countries)
preserve
collapse (median) rcfgt0 rcfgt1 igovgdpppp igovgini rcgovgdpppp cctstage countryyear if eventualcct==1, by(region yearfromcct)
gen rcfgt0cct=rcfgt0
separate rcfgt0, by(region)
separate rcfgt1, by(region)
separate rcgovgdpppp, by(region)

# Label environment variables
label variable rcfgt01 "Poverty Headcount Ratio in the Caribbean"
label variable rcfgt11 "Depth of Poverty in the Caribbean"
label variable rcgovgdpppp1 "GDP in the Caribbean"
label variable rcfgt02 "Poverty Headcount Ratio in Latin America"
label variable rcfgt12 "Depth of Poverty in Latin America"
label variable rcgovgdpppp2 "GDP in the Latin America"

# Spline CCT STAGES
mkspline before 1 phase1 2 phase2 = cctstage

#/--------------------RCFGT in Caribbean CCT Countries
eststo clear
eststo: quietly reg rcfgt01 igovgdpppp igovgini before phase1 phase2 if region=="Caribbean", robust
predict modpsrcfgt0crbcct
eststo: quietly reg rcfgt11 igovgdpppp igovgini before phase1 phase2 if region=="Caribbean", robust
predict modpsrcfgt1crbcct
quietly reg rcgovgdpppp1 before phase1 phase2 if region=="Caribbean", robust
predict modpsrcgdpcrbcct

#Label prediction variables
label variable modpsrcfgt0crbcct "Poverty Headcount Ratio (Caribbean CCT countries)"
label variable modpsrcfgt1crbcct "Depth of Poverty (Caribbean CCT countries)"
label variable modpsrcgdpcrbcct "GDP Trend (Caribbean CCT Countries)"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Caribbean's Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-CRBCCT.csv", replace nonumber wide title("Caribbean's Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT in Latin American CCT Countries
eststo clear
eststo: quietly reg rcfgt02 igovgdpppp igovgini before phase1 phase2 if region=="Latin America", robust
predict modpsrcfgt0latcct
eststo: quietly reg rcfgt12 igovgdpppp igovgini before phase1 phase2 if region=="Latin America", robust
predict modpsrcfgt1latcct
quietly reg rcgovgdpppp2 before phase1 phase2 if region=="Latin America", robust
predict modpsrcgdplatcct

#Label prediction variables
label variable modpsrcfgt0latcct "Poverty Headcount Ratio (Latin American CCT countries)"
label variable modpsrcfgt1latcct "Depth of Poverty (Latin American CCT countries)"
label variable modpsrcgdplatcct "GDP Trend (Latin American CCT Countries)"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Latin America's Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-LATCCT.csv", replace nonumber wide title("Latin America's Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

# *** GRAPHS ***
  #Caribbean
graph twoway (line modpsrcfgt0crbcct yearfromcct) (line modpsrcgdpcrbcct yearfromcct) if region=="Caribbean", scheme(s1color) yla(,nogrid) title(CCT Countries in the Caribbean: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-CRBCCT.png", replace
graph twoway (line modpsrcfgt1crbcct yearfromcct) (line modpsrcgdpcrbcct yearfromcct) if region=="Caribbean", scheme(s1color) yla(,nogrid) title(CCT Countries in the Caribbean: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-CRBCCT.png", replace
#Latin America
graph twoway (line modpsrcfgt0latcct yearfromcct) (line modpsrcgdplatcct yearfromcct) if region=="Latin America", scheme(s1color) yla(,nogrid) title(CCT Countries in Latin America: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-LATCCT.png", replace
graph twoway (line modpsrcfgt1latcct yearfromcct) (line modpsrcgdplatcct yearfromcct) if region=="Latin America", scheme(s1color) yla(,nogrid) title(CCT Countries in Latin America: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-LATCCT.png", replace

drop rcfgt0cct if yearfromcct<0
sort countryyear
encode countryyear, gen(countryyearid)
save "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Data/CCT.dta", replace

restore
#/--------------------------------------------------
  
  #/--------------------------------------------------Full Model Analysis (non-CCT Countries)
preserve
collapse (median) rcfgt0 rcfgt1 igovgdpppp igovgini rcgovgdpppp countryyear if eventualcct==0, by(region year)
gen rcfgt0ncct=rcfgt0
separate rcfgt0, by(region)
separate rcfgt1, by(region)
separate rcgovgdpppp, by(region)

# Label environment variables
label variable rcfgt01 "Poverty Headcount Ratio in the Balkans"
label variable rcfgt11 "Poverty Headcount Ratio in the Balkans"
label variable rcgovgdpppp1 "GDP in the Balkans"
label variable rcfgt02 "Poverty Headcount Ratio in the Caribbean"
label variable rcfgt12 "Poverty Headcount Ratio in the Caribbean"
label variable rcgovgdpppp2 "GDP in the Caribbean"
label variable rcfgt03 "Poverty Headcount Ratio in the Eastern Europe"
label variable rcfgt13 "Poverty Headcount Ratio in the Eastern Europe"
label variable rcgovgdpppp3 "GDP in the Eastern Europe"
label variable rcfgt04 "Poverty Headcount Ratio in the Latin America"
label variable rcfgt14 "Poverty Headcount Ratio in the Latin America"
label variable rcgovgdpppp4 "GDP in the Latin America"
label variable rcfgt05 "Poverty Headcount Ratio in the Middle East"
label variable rcfgt15 "Poverty Headcount Ratio in the Middle East"
label variable rcgovgdpppp5 "GDP in the Middle East"
label variable rcfgt06 "Poverty Headcount Ratio in the North Africa"
label variable rcfgt16 "Poverty Headcount Ratio in the North Africa"
label variable rcgovgdpppp6 "GDP in the North Africa"
label variable rcfgt07 "Poverty Headcount Ratio in the Southeast Asia"
label variable rcfgt17 "Poverty Headcount Ratio in the Southeast Asia"
label variable rcgovgdpppp7 "GDP in the Southeast Asia"
label variable rcfgt08 "Poverty Headcount Ratio in the Sub-Saharan Africa"
label variable rcfgt18 "Poverty Headcount Ratio in the Sub-Saharan Africa"
label variable rcgovgdpppp8 "GDP in the Sub-Saharan Africa"
label variable rcfgt09 "Poverty Headcount Ratio in the West Africa"
label variable rcfgt19 "Poverty Headcount Ratio in the West Africa"
label variable rcgovgdpppp9 "GDP in the West Africa"

#/--------------------RCFGT in Balkan non-CCT Countries
eststo clear
eststo: quietly reg rcfgt01 igovgdpppp igovgini year if region=="Balkans", robust
predict modpsrcfgt0blkncct
eststo: quietly reg rcfgt11 igovgdpppp igovgini year if region=="Balkans", robust
predict modpsrcfgt1blkncct
quietly reg rcgovgdpppp1 year if region=="Balkans", robust
predict modpsrcgdpblkncct

#Label prediction variables
label variable modpsrcfgt0blkncct "Poverty Headcount Ratio (Balkan non-CCT countries)"
label variable modpsrcfgt1blkncct "Depth of Poverty (Balkan non-CCT countries)"
label variable modpsrcgdpblkncct "GDP Trend (Balkan non-CCT Countries)"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Balkan non-CCT Countries' Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-BLKnCCT.csv", replace nonumber wide title("Balkan non-CCT Countries' Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT in Caribbean non-CCT Countries
eststo clear
eststo: quietly reg rcfgt02 igovgdpppp igovgini year if region=="Caribbean", robust
predict modpsrcfgt0crbncct
eststo: quietly reg rcfgt12 igovgdpppp igovgini year if region=="Caribbean", robust
predict modpsrcfgt1crbncct
quietly reg rcgovgdpppp2 year if region=="Caribbean", robust
predict modpsrcgdpcrbncct

#Label prediction variables
label variable modpsrcfgt0crbncct "Poverty Headcount Ratio (Caribbean non-CCT countries)"
label variable modpsrcfgt1crbncct "Depth of Poverty (Caribbean non-CCT countries)"
label variable modpsrcgdpcrbncct "GDP Trend (Caribbean non-CCT Countries)"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Caribbean non-CCT Countries' Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-CRBnCCT.csv", replace nonumber wide title("Caribbean non-CCT Countries' Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT in Eastern Europe non-CCT Countries
eststo clear
eststo: quietly reg rcfgt03 igovgdpppp igovgini year if region=="Eastern Europe", robust
predict modpsrcfgt0eeuncct
eststo: quietly reg rcfgt13 igovgdpppp igovgini year if region=="Eastern Europe", robust
predict modpsrcfgt1eeuncct
quietly reg rcgovgdpppp3 year if region=="Eastern Europe", robust
predict modpsrcgdpeeuncct

#Label prediction variables
label variable modpsrcfgt0eeuncct "Poverty Headcount Ratio (Eastern European non-CCT countries)"
label variable modpsrcfgt1eeuncct "Depth of Poverty (Eastern European non-CCT countries)"
label variable modpsrcgdpeeuncct "GDP Trend (Eastern European non-CCT Countries)"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Eastern Europe non-CCT Countries' Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-EEUnCCT.csv", replace nonumber wide title("Eastern Europe non-CCT Countries' Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT in Latin American non-CCT Countries
eststo clear
eststo: quietly reg rcfgt04 igovgdpppp igovgini year if region=="Latin America", robust
predict modpsrcfgt0latncct
eststo: quietly reg rcfgt14 igovgdpppp igovgini year if region=="Latin America", robust
predict modpsrcfgt1latncct
quietly reg rcgovgdpppp4 year if region=="Latin America", robust
predict modpsrcgdplatncct

#Label prediction variables
label variable modpsrcfgt0latncct "Poverty Headcount Ratio (Latin American non-CCT countries)"
label variable modpsrcfgt1latncct "Depth of Poverty (Latin American non-CCT countries)"
label variable modpsrcgdplatncct "GDP Trend (Latin American non-CCT Countries)"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Latin American non-CCT Countries' Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-LATnCCT.csv", replace nonumber wide title("Latin American non-CCT Countries' Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT in Middle Eastern non-CCT Countries
eststo clear
eststo: quietly reg rcfgt05 igovgdpppp igovgini year if region=="Middle East", robust
predict modpsrcfgt0meancct
eststo: quietly reg rcfgt15 igovgdpppp igovgini year if region=="Middle East", robust
predict modpsrcfgt1meancct
quietly reg rcgovgdpppp5 year if region=="Middle East", robust
predict modpsrcgdpmeancct

#Label prediction variables
label variable modpsrcfgt0meancct "Poverty Headcount Ratio (Middle Eastern non-CCT countries)"
label variable modpsrcfgt1meancct "Depth of Poverty (Middle Eastern non-CCT countries)"
label variable modpsrcgdpmeancct "GDP Trend (Middle Eastern non-CCT Countries)"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Middle Eastern non-CCT Countries' Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-MEAnCCT.csv", replace nonumber wide title("Middle Eastern non-CCT Countries' Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT in North African non-CCT Countries
eststo clear
eststo: quietly reg rcfgt06 igovgdpppp igovgini year if region=="North Africa", robust
predict modpsrcfgt0nafncct
eststo: quietly reg rcfgt16 igovgdpppp igovgini year if region=="North Africa", robust
predict modpsrcfgt1nafncct
quietly reg rcgovgdpppp6 year if region=="North Africa", robust
predict modpsrcgdpnafncct

#Label prediction variables
label variable modpsrcfgt0nafncct "Poverty Headcount Ratio (North African non-CCT countries)"
label variable modpsrcfgt1nafncct "Depth of Poverty (North African non-CCT countries)"
label variable modpsrcgdpnafncct "GDP Trend (North African non-CCT Countries)"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("North African non-CCT Countries' Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-NAFnCCT.csv", replace nonumber wide title("North African non-CCT Countries' Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT in Southeast Asia non-CCT Countries
eststo clear
eststo: quietly reg rcfgt07 igovgdpppp igovgini year if region=="Southeast Asia", robust
predict modpsrcfgt0seancct
eststo: quietly reg rcfgt17 igovgdpppp igovgini year if region=="Southeast Asia", robust
predict modpsrcfgt1seancct
quietly reg rcgovgdpppp7 year if region=="Southeast Asia", robust
predict modpsrcgdpseancct

#Label prediction variables
label variable modpsrcfgt0seancct "Poverty Headcount Ratio (Southeast Asian non-CCT countries)"
label variable modpsrcfgt1seancct "Depth of Poverty (Southeast Asian non-CCT countries)"
label variable modpsrcgdpseancct "GDP Trend (Southeast Asian non-CCT Countries)"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Southeast Asian non-CCT Countries' Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-SEAnCCT.csv", replace nonumber wide title("Southeast Asian non-CCT Countries' Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT in Sub-Saharan Africa non-CCT Countries
eststo clear
eststo: quietly reg rcfgt08 igovgdpppp igovgini year if region=="Sub-Saharan Africa", robust
predict modpsrcfgt0ssancct
eststo: quietly reg rcfgt18 igovgdpppp igovgini year if region=="Sub-Saharan Africa", robust
predict modpsrcfgt1ssancct
quietly reg rcgovgdpppp8 year if region=="Sub-Saharan Africa", robust
predict modpsrcgdpssancct

#Label prediction variables
label variable modpsrcfgt0ssancct "Poverty Headcount Ratio (Sub-Saharan Africa non-CCT countries)"
label variable modpsrcfgt1ssancct "Depth of Poverty (Sub-Saharan Africa non-CCT countries)"
label variable modpsrcgdpssancct "GDP Trend (Sub-Saharan Africa non-CCT Countries)"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("Sub-Saharan Africa non-CCT Countries' Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-SSAnCCT.csv", replace nonumber wide title("Sub-Saharan Africa non-CCT Countries' Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/--------------------RCFGT in West African non-CCT Countries
eststo clear
eststo: quietly reg rcfgt09 igovgdpppp igovgini year if region=="West Africa", robust
predict modpsrcfgt0wafncct
eststo: quietly reg rcfgt19 igovgdpppp igovgini year if region=="West Africa", robust
predict modpsrcfgt1wafncct
quietly reg rcgovgdpppp9 year if region=="West Africa", robust
predict modpsrcgdpwafncct

#Label prediction variables
label variable modpsrcfgt0wafncct "Poverty Headcount Ratio (West African non-CCT countries)"
label variable modpsrcfgt1wafncct "Depth of Poverty (West African non-CCT countries)"
label variable modpsrcgdpwafncct "GDP Trend (West African non-CCT Countries)"

# *** TABLE ***
  esttab, ar2 nocons wide nonumber title("West African non-CCT Countries' Rate of Change in Poverty") mtitles("RCFGT0" "RCFGT1")
esttab using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Tables/MOD-RCFGT-WAFnCCT.csv", replace nonumber wide title("West African non-CCT Countries' Rate of Change in Poverty") mtitles("Rate of Change FGT0" "Rate of Change FGT1")

#/-------------------- *** GRAPHS ***
  #Balkans
graph twoway (line modpsrcfgt0blkncct year) (line modpsrcgdpblkncct year) if region=="Balkans", scheme(s1color) yla(,nogrid) title(non-CCT Countries in the Balkans: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-BLKnCCT.png", replace
graph twoway (line modpsrcfgt1blkncct year) (line modpsrcgdpblkncct year) if region=="Balkans", scheme(s1color) yla(,nogrid) title(non-CCT Countries in the Balkans: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-BLKnCCT.png", replace
#Caribbean
graph twoway (line modpsrcfgt0crbncct year) (line modpsrcgdpcrbncct year) if region=="Caribbean", scheme(s1color) yla(,nogrid) title(non-CCT Countries in the Caribbean: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-CRBnCCT.png", replace
graph twoway (line modpsrcfgt1crbncct year) (line modpsrcgdpcrbncct year) if region=="Caribbean", scheme(s1color) yla(,nogrid) title(non-CCT Countries in the Caribbean: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-CRBnCCT.png", replace
#Eastern Europe
graph twoway (line modpsrcfgt0eeuncct year) (line modpsrcgdpeeuncct year) if region=="Eastern Europe", scheme(s1color) yla(,nogrid) title(non-CCT Countries in Eastern Europe: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-EEUnCCT.png", replace
graph twoway (line modpsrcfgt1eeuncct year) (line modpsrcgdpeeuncct year) if region=="Eastern Europe", scheme(s1color) yla(,nogrid) title(non-CCT Countries in Eastern Europe: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-EEUnCCT.png", replace
#Latin America
graph twoway (line modpsrcfgt0latncct year) (line modpsrcgdplatncct year) if region=="Latin America", scheme(s1color) yla(,nogrid) title(non-CCT Countries in Latin America: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-LATnCCT.png", replace
graph twoway (line modpsrcfgt1latncct year) (line modpsrcgdplatncct year) if region=="Latin America", scheme(s1color) yla(,nogrid) title(non-CCT Countries in Latin America: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-LATnCCT.png", replace
#Middle East
graph twoway (line modpsrcfgt0meancct year) (line modpsrcgdpmeancct year) if region=="Middle East", scheme(s1color) yla(,nogrid) title(non-CCT Countries in the Middle East: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-MEAnCCT.png", replace
graph twoway (line modpsrcfgt1meancct year) (line modpsrcgdpmeancct year) if region=="Middle East", scheme(s1color) yla(,nogrid) title(non-CCT Countries in the Middle East: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-MEAnCCT.png", replace
#North Africa
graph twoway (line modpsrcfgt0nafncct year) (line modpsrcgdpnafncct year) if region=="North Africa", scheme(s1color) yla(,nogrid) title(non-CCT Countries in North Africa: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-NAFnCCT.png", replace
graph twoway (line modpsrcfgt1nafncct year) (line modpsrcgdpnafncct year) if region=="North Africa", scheme(s1color) yla(,nogrid) title(non-CCT Countries in North Africa: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-NAFnCCT.png", replace
#Southeast Asia
graph twoway (line modpsrcfgt0seancct year) (line modpsrcgdpseancct year) if region=="Southeast Asia", scheme(s1color) yla(,nogrid) title(non-CCT Countries in Southeast Asia: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-SEAnCCT.png", replace
graph twoway (line modpsrcfgt1seancct year) (line modpsrcgdpseancct year) if region=="Southeast Asia", scheme(s1color) yla(,nogrid) title(non-CCT Countries in Southeast Asia: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-SEAnCCT.png", replace
#Sub-Saharan Africa
graph twoway (line modpsrcfgt0ssancct year) (line modpsrcgdpssancct year) if region=="Sub-Saharan Africa", scheme(s1color) yla(,nogrid) title(non-CCT Countries in Sub-Saharan Africa: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-SSAnCCT.png", replace
graph twoway (line modpsrcfgt1ssancct year) (line modpsrcgdpssancct year) if region=="Sub-Saharan Africa", scheme(s1color) yla(,nogrid) title(non-CCT Countries in Sub-Saharan Africa: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-SSAnCCT.png", replace
#West Africa
graph twoway (line modpsrcfgt0wafncct year) (line modpsrcgdpwafncct year) if region=="West Africa", scheme(s1color) yla(,nogrid) title(non-CCT Countries in West Africa: Rate of Change in the Poverty Headcount Ratio, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT0-WAFnCCT.png", replace
graph twoway (line modpsrcfgt1wafncct year) (line modpsrcgdpwafncct year) if region=="West Africa", scheme(s1color) yla(,nogrid) title(non-CCT Countries in West Africa: Rate of Change in the Depth of Poverty, size(medium)) legend(size(vsmall)) xline(0)
graph export "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Graphs/MOD-RCFGT1-WAFnCCT.png", replace

#/--------------------------------------------------t-test
#Merge the datasets to include the collapsed rates of change from CCT and non-CCT countries
merge 1:1 countryyearid using "/Users/iPete/Dropbox/Columbia University/2012 - Spring/5999 - Master Thesis/Data/CCT.dta"
ttest rcfgt0cct rcfgt0ncct

restore

exit

/** Notes
* ****************************************************
  * 
  * ****************************************************
  */
  