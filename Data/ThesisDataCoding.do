/// //     /////      // ////  //  //      //////
///   /	 /      /     //       //  //      //
///   /  /      /     // //    //  //      ////
///   /  /      /     //       //  //      //
/// //    /////       //       //  //////  //////

///--------------------------------------------------
/// Pedro çvila - Spring 2012 QMSS 5999 Thesis
/// Dataset Coding
///--------------------------------------------------

//Interpolate missing values
//by country: ipolate fgt0ppp2 year, gen(ifgt0)
//by country: ipolate fgt1ppp2 year, gen(ifgt1ppp2)
//by country: ipolate educhildout year, gen(ieduchildout)
//by country: ipolate educompleteprimary year, gen(ieducompleteprimary)
//by country: ipolate genpop year, gen(igenpop)
//by country: ipolate genpopgrowth year, gen(igenpopgrowth)
//by country: ipolate genpopdensity year, gen(igenpopdensity)
//by country: ipolate govedugdp year, gen(igovedugdp)
//by country: ipolate govgini year, gen(igovgini)
//by country: ipolate govconsumexp year, gen(igovconsumexp)
//by country: ipolate govgdpppp year, gen(igovgdpppp)
//by country: ipolate govgdppppcapita year, gen(igovgdppppcapita)
//by country: ipolate labforce year, gen(ilabforce)
//by country: ipolate labprimaryedu year, gen(ilabprimaryedu)
//by country: ipolate medmortinfant year, gen(imedmortinfant)
//by country: ipolate meddptimmuinfant year, gen(imeddptimmuinfant)
//by country: ipolate medmeaimmuinfant year, gen(imedmeaimmuinfant)
//by country: ipolate medcalpday year, gen(imedcalpday)
//by country: ipolate medundernourishment year, gen(imedundernourishment)
//by country: ipolate medlowweightnewborn year, gen(imedlowweightnewborn)
//by country: ipolate medprenatalcare year, gen(imedprenatalcare)
//by country: ipolate medlifeexpbirth year, gen(imedlifeexpbirth)
//by country: ipolate meddrpk year, gen(imeddrpk)
//by country: ipolate medskilledbirth year, gen(imedskilledbirth)
//by country: ipolate medh2o year, gen(imedh2o)


//Create Time Series data
encode country, gen(countryid)
tsset countryid year

//Generate Lag variables
gen lfgt0 = L.ifgt0
gen lfgt1 = L.ifgt1
gen leduchildout = L.ieduchildoutgen leducompleteprimary = L.ieducompleteprimary
gen lgenpop = L.igenpopgen lgenpopgrowth = L.igenpopgrowthgen lgenpopdensity = L.igenpopdensitygen lgovedugdp = L.igovedugdp
gen lgovgini = L.igovginigen lgovconsumexp = L.igovconsumexpgen lgovgdpppp = L.igovgdppppgen lgovgdppppcapita = L.igovgdppppcapitagen llabforce = L.ilabforcegen llabprimaryedu = L.ilabprimaryedugen lmedmortinfant = L.imedmortinfant
gen lmeddptimmuinfant = L.meddptimmuinfantgen lmedmeaimmuinfant = L.medmeaimmuinfantgen lmedcalpday = L.imedcalpdaygen lmedundernourishment = L.imedundernourishmentgen lmedlowweightnewborn = L.imedlowweightnewborngen lmedprenatalcare = L.imedprenatalcaregen lmedlifeexpbirth = L.imedlifeexpbirthgen lmeddrpk = L.imeddrpkgen lmedskilledbirth = L.imedskilledbirthgen lmedh2o = L.imedh2o//Generate Rates of Changegen rcfgt0 = (ifgt0 - lfgt0)/lfgt0
gen rcfgt1 = (ifgt1 - lfgt1)/lfgt1
gen rceduchildout = (ieduchildout - leduchildout)/leduchildout
gen rceducompleteprimary = (educompleteprimary - leducompleteprimary)/leducompleteprimary
gen rcgenpop = (igenpop - lgenpop)/lgenpop
gen rcgenpopgrowth = (igenpopgrowth - lgenpopgrowth)/lgenpopgrowth
gen rcgenpopdensity = (igenpopdensity - lgenpopdensity)/lgenpopdensity
gen rcgovedugdp = (igovedugdp - lgovedugdp)/lgovedugdp
gen rcgovgini = (igovgini - lgovgini)/lgovgini
gen rcgovconsumexp = (igovconsumexp - lgovconsumexp)/lgovconsumexp
gen rcgovgdpppp = (igovgdpppp - lgovgdpppp)/lgovgdpppp
gen rcgovgdppppcapita = (igovgdppppcapita - lgovgdppppcapita)/lgovgdppppcapita
gen rclabforce = (ilabforce - llabforce)/llabforce
gen rclabprimaryedu = (ilabprimaryedu - llabprimaryedu)/llabprimaryedu
gen rcmedmortinfant = (imedmortinfant - lmedmortinfant)/lmedmortinfant
gen rcmeddptimmuinfant = (meddptimmuinfant - lmeddptimmuinfant)/lmeddptimmuinfant
gen rcmedmeaimmuinfant = (medmeaimmuinfant - lmedmeaimmuinfant)/lmedmeaimmuinfant
gen rcmedcalpday = (imedcalpday - lmedcalpday)/lmedcalpday
gen rcmedundernourishment = (imedundernourishment - lmedundernourishment)/lmedundernourishment
gen rcmedlowweightnewborn = (imedlowweightnewborn - lmedlowweightnewborn)/lmedlowweightnewborn
gen rcmedprenatalcare = (imedprenatalcare - lmedprenatalcare)/lmedprenatalcare
gen rcmedlifeexpbirth = (imedlifeexpbirth - lmedlifeexpbirth)/lmedlifeexpbirth
gen rcmeddrpk = (imeddrpk - lmeddrpk)/lmeddrpk
gen rcmedskilledbirth = (imedskilledbirth - lmedskilledbirth)/lmedskilledbirth
gen rcmedh2o = (imedh2o - lmedh2o)/lmedh2o

//Label time-series variables
label variable rcfgt0 `"Rate of Change in FGT0"'
label variable rcfgt1 `"Rate of Change in FGT1"'
label variable rceduchildout `"Rate of Change in Children out of primary school"'
label variable rceducompleteprimary `"Rate of Change in Primary Completion"'
label variable rcgenpop `"Rate of Change in total Population"'label variable rcgenpopgrowth `"Rate of Change of Population Growth"'label variable rcgenpopdensity `"Rate of Change in Population density (people per sq. km of land area)"'
label variable rcgovedugdp `"Rate of Change in Public Expenditure on Education"'
label variable rcgovgini `"Rate of Change of Gini Coefficient"'
label variable rcgovconsumexp `"Rate of Change of Consumer Expenditure"'
label variable rcgovgdpppp `"Rate of Change of GDP, PPP (in millions of current international $)"'label variable rcgovgdppppcapita `"Rate of Change of GDP per Capita (PPP)"'label variable rclabforce `"Rate of Change of Labor Force Level"'label variable rclabprimaryedu `"Rate of Change in Labor force with a primary education (% of total)"'
label variable rcmedmortinfant `"Rate of Change of Infant Mortality"'
label variable rcmeddptimmuinfant `"Rate of Change of Infant DPT Immunizations"'label variable rcmedmeaimmuinfant `"Rate of Change of Infant Measles Immunizations"'
label variable rcmedcalpday `"Rate of Change in the Depth of hunger (kilocalories per person per day)"'
label variable rcmedundernourishment `"Rate of Change in the Prevalence of undernourishment (% of population)"'
label variable rcmedlowweightnewborn `"Rate of Change in % of Low-birthweight babies"'
label variable rcmedprenatalcare `"Rate of Change in % of Pregnant women receiving prenatal care"'
label variable rcmedlifeexpbirth `"Rate of Change in total Life expectancy at birth"'
label variable rcmeddrpk `"Rate of Change in Physicians per 1,000 people"'
label variable rcmedskilledbirth `"Rate of Change in % of Births attended by skilled health staff"'
label variable rcmedh2o `"Rate of Change in Improved water source access (% of population)"'


//Generate Median & Mean rates of change in the FGT0 & FGT1 levels for World CCT and non-CCT countries
egen medrcfgt0cct = median(rcfgt0) if eventualcct==1, by(country year)
egen medrcfgt1cct = median(rcfgt1) if eventualcct==1, by(country year)
egen medrcfgt0ncct = median(rcfgt0) if eventualcct==0, by(country year)
egen medrcfgt1ncct = median(rcfgt1) if eventualcct==0, by(country year)
egen mrcfgt0cct = mean(rcfgt0) if eventualcct==1, by(country year)
egen mrcfgt1cct = mean(rcfgt1) if eventualcct==1, by(country year)
egen mrcfgt0ncct = mean(rcfgt0) if eventualcct==0, by(country year)
egen mrcfgt1ncct = mean(rcfgt1) if eventualcct==0, by(country year)

//Label Median & Mean rates of change
label variable medrcfgt0cct `"Median FGT0 for CCT Countries"'
label variable medrcfgt1cct `"Median FGT1 for CCT Countries"'
label variable medrcfgt0ncct `"Median FGT0 for non-CCT Countries"'
label variable medrcfgt1ncct `"Median FGT1 for non-CCT Countries"'
label variable mrcfgt0cct `"Mean FGT0 for CCT Countries"'
label variable mrcfgt1cct `"Mean FGT1 for CCT Countries"'
label variable mrcfgt0ncct `"Mean FGT0 for non-CCT Countries"'
label variable mrcfgt1ncct `"Mean FGT1 for non-CCT Countries"'


//Label interpolated variables
label variable country `"Country"'
label variable year `"Year"'
label variable ifgt0 `"Poverty headcount ratio at PPP $2/day"'
label variable ifgt1 `"Depth of Poverty at PPP $2/day"'
label variable ieduchildout `"Children out of school, primary"'
label variable ieducompleteprimary `"Primary completion rate, total (% of relevant age group, Complete)"'
label variable igenpop `"Population, total"'
label variable igenpopgrowth `"Population growth (annual %)"'
label variable igenpopdensity `"Population density (people per sq. km of land area)"'
label variable igovedugdp `"Public spending on education, total (% of GDP)"'
label variable igovgini `"GINI index"'
label variable igovconsumexp `"Household final consumption expenditure, PPP (current international $)"'
label variable igovgdpppp `"GDP, PPP (in millions of current international $)"'
label variable igovgdppppcapita `"GDP per capita, PPP (current international $)"'
label variable ilabforce `"Labor force, total"'
label variable ilabprimaryedu `"Labor force with a primary education (% of total)"'
label variable imedmortinfant `"Mortality rate, infant (per 1,000 live births)"'
label variable imeddptimmuinfant `"Immunization, DPT (% of children ages 12-23 months)"'
label variable imedmeaimmuinfant `"Immunization, measles (% of children ages 12-23 months)"'
label variable imedcalpday `"Depth of hunger (kilocalories per person per day)"'
label variable imedundernourishment `"Prevalence of undernourishment (% of population)"'
label variable imedlowweightnewborn `"Low-birthweight babies (% of births)"'
label variable imedprenatalcare `"Pregnant women receiving prenatal care (%)"'
label variable imedlifeexpbirth `"Life expectancy at birth, total (years)"'
label variable imeddrpk `"Physicians (per 1,000 people)"'
label variable imedskilledbirth `"Births attended by skilled health staff (% of total)"'
label variable imedh2o `"Improved water source (% of population with access)"'
label variable cctparticipants `"CCT Participants Receiving Benefits"'
label variable cctsizelocal `"Value of CCT Benefits Distributed in local currency"'
label variable eventualcct `"Dummy variable for whether the country has deployed a CCT program"'
label variable yearfromcct `"Number of years from the year of the CCT implementation"'
label variable cctyear `"Year in which CCT program was deployed"'
label variable continent `"Continent"'
label variable region `"Grouping Region"'


// Generate and label a few recodes
recode yearfromcct (min/0 .=0 "Before CCT") (1/2=1 "Nacent CCT") (3/4=2 "Intermediate CCT") (5/max=3 "Advanced CCT"), gen(cctstage)
recode yearfromcct (min/0 .=0 "Pre-CCT") (1/max=1 "Post-CCT"), gen(cctstate)
label variable cctstage `"Stage of CCT"'
label variable cctstate `"State of CCT"'


//Label other variables
//label variable genpopruralgrowth `"Rural population growth (annual %)"'
//label variable genpopurbgrowth `"Urban population growth (annual %)"'
//label variable cctyear `"Years from CCT Program Implementation"'
//label variable rcctparticipants `"CCT Participants Receiving Benefits in the month of December"'
//label variable rcctsizelocal `"Value of CCT Benefits Distributed in R$ in the month of December"'
//label variable fgt0ppp125 `"Poverty headcount ratio at $1.25 a day (PPP) (% of population)"'
//label variable fgt1ppp125 `"Poverty gap at $1.25 a day (PPP) (%)"'
//label variable fgt0ppp2 `"Poverty headcount ratio at $2 a day (PPP) (% of population)"'
//label variable fgt1ppp2 `"Poverty gap at $2 a day (PPP) (%)"'
//label variable fgt0rural `"Poverty headcount ratio at rural poverty line (% of rural population)"'
//label variable fgt1rural `"Poverty gap at rural poverty line (%)"'
//label variable fgt0urb `"Poverty headcount ratio at urban poverty line (% of urban population)"'
//label variable fgt1urb `"Poverty gap at urban poverty line (%)"'
//label variable edupersist5th `"Persistence to grade 5, total (% of cohort)"'
//label variable edupersistprimary `"Persistence to last grade of primary, total (% of cohort)"'
//label variable eduprogresssecondary `"Progression to secondary school (%)"'
//label variable edulit `"Literacy rate, adult total (% of people ages 15 and above)"'
//label variable edulityouth `"Literacy rate, youth total (% of people ages 15-24)"'
//label variable eduenrollprimary `"Total enrollment, primary (% net)"'
//label variable eduenrollprimarypcnet `"School enrollment, primary (% net)"'
//label variable eduenrollsecondarypcnet `"School enrollment, secondary (% net)"'
//label variable eduenrollpreprimarypcgross `"School enrollment, preprimary (% gross)"'
//label variable eduenrolltertiarypcgross `"School enrollment, tertiary (% gross)"'
//label variable edudurationprimary `"Primary education, duration (years)"'
//label variable edudurationsecondary `"Secondary education, duration (years)"'
//label variable labparticipation `"Labor participation rate, total (% of total population ages 15+)"'
//label variable labsecondaryedu `"Labor force with secondary education (% of total)"'
//label variable labtertiaryedu `"Labor force with tertiary education (% of total)"'
//label variable labunemp `"Unemployment, total (% of total labor force)"'
//label variable labunemplt `"Long-term unemployment (% of total unemployment)"'
//label variable labunempprimaryedu `"Unemployment with primary education (% of total unemployment)"'
//label variable labunempsecondaryedu `"Unemployment with secondary education (% of total unemployment)"'
//label variable labunemptertiaryedu `"Unemployment with tertiary education (% of total unemployment)"'
//label variable labunempyouth `"Unemployment, youth total (% of total labor force ages 15-24)"'
//label variable medheight4ageu5 `"Malnutrition prevalence, height for age (% of children under 5)"'
//label variable medmortneonatal `"Mortality rate, neonatal (per 1,000 live births)"'
//label variable medmortu5 `"Mortality rate, under-5 (per 1,000)"'
//label variable medtubdetect `"Tuberculosis case detection rate (%, all forms)"'
//label variable medweight4ageu5 `"Malnutrition prevalence, weight for age (% of children under 5)"'
//label variable program `"CCT Program"'
//label variable ttype `"Transfer Type (0-NA, or Unknown Treatment; 1-Non-cash Welfare; 2-Unconditional Cash Transfer; 3-Conditional Cash Transfer"'
//label variable countryyear `"Codification of Country-Year"'
//label variable eduintake1stgross `"Gross intake rate in grade 1, total (% of relevant age group)"'
//label variable edurepeatprimary `"Repeaters, primary, total (% of total enrollment)"'
//label variable edurepeatsecondary `"Repeaters, secondary, total (% of total enrollment)"'
//label variable edustartprimary `"Primary school starting age (years)"'
//label variable edustartsecondary `"Secondary school starting age (years)"'
//label variable eduteacherratioprimary `"Pupil-teacher ratio, primary"'
//label variable eduteacherratiosecondary `"Pupil-teacher ratio, secondary"'
//label variable eduteachersecondary `"Secondary education, teachers"'
//label variable eduteachersprimary `"Primary education, teachers"'
//label variable eduteachtrainprimary `"Trained teachers in primary education (% of total teachers)"'
//label variable geninch10pc `"Income share held by highest 10%"'
//label variable geninch20pc `"Income share held by highest 20%"'
//label variable genincl10pc `"Income share held by lowest 10%"'
//label variable genincl20pc `"Income share held by lowest 20%"'
//label variable genpopadult `"Population ages 15-64 (% of total)"'
//label variable genpoplcity `"Population in largest city"'
//label variable genpoplcitypcurb `"Population in the largest city (% of urban population)"'
//label variable genpopold `"Population ages 65 and above (% of total)"'
//label variable genpoprural `"Rural population"'
//label variable genpopruralpc `"Rural population (% of total population)"'
//label variable genpopurb `"Urban population"'
//label variable genpopurbagglomerate1mil `"Population in urban agglomerations of more than 1 million"'
//label variable genpopurbagglomerate1milpc `"Population in urban agglomerations of more than 1 million (% of total population)"'
//label variable genpopurbpc `"Urban population (% of total)"'
//label variable genpopyouth `"Population ages 0-14 (% of total)"'
//label variable govgnippp `"GNI, PPP (current international $)"'
//label variable govppplcux `"PPP conversion factor, GDP (LCU per international $)"'
//label variable govpppmktx `"PPP conversion factor (GDP) to market exchange rate ratio"'
//label variable govpppprivlcux `"PPP conversion factor, private consumption (LCU per international $)"'
//label variable govstuexpprimary `"Expenditure per student, primary (% of GDP per capita)"'
//label variable govstuexpsecondary `"Expenditure per student, secondary (% of GDP per capita)"'
//label variable govstuexptertiary `"Expenditure per student, tertiary (% of GDP per capita)"'
//label variable medaritreatu5 `"ARI treatment (% of children under 5 taken to a health provider)"'
//label variable medcontraprev `"Contraceptive prevalence (% of women ages 15-49)"'
//label variable meddiatreatu5 `"Diarrhea treatment (% of children under 5 receiving oral rehydration and continued feeding)"'
//label variable medfertility `"Fertility rate, total (births per woman)"'
//label variable medfertilityteen `"Adolescent fertility rate (births per 1,000 women ages 15-19)"'
//label variable medhiv `"Prevalence of HIV, total (% of population ages 15-49)"'
//label variable medhivkid `"Children (0-14) living with HIV"'
//label variable medmalfeveranddrugsu5 `"Children with fever receiving antimalarial drugs (% of children under age 5 with fever)"'
//label variable mednursepk `"Nurses and midwives (per 1,000 people)"'
//label variable medtechpk `"Community health workers (per 1,000 people)"'
//label variable medteenmom `"Teenage mothers (% of women ages 15-19 who have had children or are currently pregnant)"'
//label variable medtetnewborn `"Newborns protected against tetanus (%)"'
//label variable medtub `"Incidence of tuberculosis (per 100,000 people)"'
//label variable medtubtreat `"Tuberculosis treatment success rate (% of registered cases)"'
//label variable ccountry `"Country Code"'
//label variable cyear `"YearCode"'




exit