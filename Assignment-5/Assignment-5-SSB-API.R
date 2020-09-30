library(PxWebApiData)
library(data.table)
library(tidyverse)
library(janitor)
library(dplyr)

?ApiData

county <- ApiData("http://data.ssb.no/api/v0/dataset/95274.json?lang=no",
                  getDataByGET = TRUE)

whole_country <- ApiData("http://data.ssb.no/api/v0/dataset/95276.json?lang=no",
                         getDataByGET = TRUE)

# two similar lists, different labels and coding
head(county[[1]])
head(county[[2]])

head(whole_country[[1]])

# Use first list, rowbind both data
dframe <- bind_rows(county[[1]], whole_country[[1]])


# new names, could have used dplyr::rename()
names(dframe)
names(dframe) <- c("region", "date", "variable", "value")
str(dframe)

# Split date
dframe <- dframe %>% separate(date, 
                              into = c("year", "month"), 
                              sep = "M")
head(dframe)

# Make a new proper date variable
library(lubridate)
dframe <- dframe %>%  mutate(date = ymd(paste(year, month, 1)))
str(dframe)

# And how many levels has the variable?
dframe %>% select(variable) %>% unique()

# car::recode()
dframe <- dframe %>%  mutate(variable1 = car::recode(dframe$variable,
                                                     ' "Utleigde rom"="rentedrooms";
                                                      "Pris per rom (kr)"="roomprice";
                                                      "Kapasitetsutnytting av rom (prosent)"="roomcap";
                                                      "Kapasitetsutnytting av senger (prosent)"="bedcap";
                                                      "Losjiomsetning (1 000 kr)"="revenue";
                                                      "Losjiomsetning per tilgjengeleg rom (kr)"="revperroom";
                                                      "Losjiomsetning, hittil i Ã¥r (1 000 kr)"="revsofar";
                                                      "Losjiomsetning per tilgjengeleg rom, hittil i Ã¥r (kr)"="revroomsofar";
                                                      "Pris per rom hittil i Ã¥r (kr)"="roompricesofar";
                                                      "Kapasitetsutnytting av rom hittil i Ã¥r (prosent)"="roomcapsofar";
                                                      "Kapasitetsutnytting av senger, hittil i Ã¥r (prosent)"="bedcapsofar" '))

dframe %>% select(variable1) %>% unique()
with(dframe, table(variable, variable1))

# dplyr::recode()
dframe <- dframe %>% mutate(variable2 = dplyr::recode(variable,
                                                      "Utleigde rom"="rentedrooms",
                                                      "Pris per rom (kr)"="roomprice",
                                                      "Kapasitetsutnytting av rom (prosent)"="roomcap",
                                                      "Kapasitetsutnytting av senger (prosent)"="bedcap",
                                                      "Losjiomsetning (1 000 kr)"="revenue",
                                                      "Losjiomsetning per tilgjengeleg rom (kr)"="revperroom",
                                                      "Losjiomsetning, hittil i Ã¥r (1 000 kr)"="revsofar",
                                                      "Losjiomsetning per tilgjengeleg rom, hittil i Ã¥r (kr)"="revroomsofar",
                                                      "Pris per rom hittil i Ã¥r (kr)"="roompricesofar",
                                                      "Kapasitetsutnytting av rom hittil i Ã¥r (prosent)"="roomcapsofar",
                                                      "Kapasitetsutnytting av senger, hittil i Ã¥r (prosent)"="bedcapsofar"))

dframe %>% select(variable2) %>% unique()
with(dframe, table(variable, variable2))

# or mutate & ifelse, a bit cumbersome, but flexible
dframe <- 
  dframe %>%
  mutate(variable3 =
           ifelse(variable == "Utleigde rom", "rentedrooms",
                  ifelse(variable == "Pris per rom (kr)", "roomprice",
                         ifelse(variable == "Kapasitetsutnytting av rom (prosent)", "roomcap",
                                ifelse(variable == "Kapasitetsutnytting av senger (prosent)", "bedcap",
                                       ifelse(variable == "Losjiomsetning (1 000 kr)", "revenue",
                                              ifelse(variable == "Losjiomsetning per tilgjengeleg rom (kr)", "revperroom",
                                                     ifelse(variable == "Losjiomsetning, hittil i Ã¥r (1 000 kr)", "revsofar",
                                                            ifelse(variable == "Losjiomsetning per tilgjengeleg rom, hittil i Ã¥r (kr)", "revroomsofar",
                                                                   ifelse(variable == "Pris per rom hittil i Ã¥r (kr)", "roompricesofar",
                                                                          ifelse(variable == "Kapasitetsutnytting av rom hittil i Ã¥r (prosent)", "roomcapsofar", "bedcapsofar")))))))))))


dframe %>% select(variable3) %>% unique()
with(dframe, table(variable, variable3))


# recode region
dframe <- dframe %>% mutate(region = 
                              ifelse(region == "Hele landet",
                                     "Whole country", region))

mosaic::tally(~region, data = dframe)

#janitor::make_clean_names(~region, data = dframe)

# we now have the data in long format ready for data wrangling

dframe <- dframe %>% mutate(region =
                              ifelse(region == "Heile landet", "Whole country",
                                     ifelse(region == "Troms og Finnmark - Romsa ja Finnmárku", "Troms and Finnmark",
                                            ifelse(region == "Trøndelag - Trööndelage", "Trøndelag",
                                                   ifelse(region == "Vestfold og Telemark", "Vestfold and Telemark",
                                                          ifelse(region == "Møre og Romsdal", "Møre and Romsdal", region))))))

mosaic::tally(~region, data = dframe)

# Extract all rows having roomcap vairabless
roomcaps <- filter(dframe, variable1 == 'roomcap')

#plotting graph of roomcap over time grouped by region
roomcaps %>% ggplot(aes(x=month, y=value, group=region))  + geom_line(aes(color=region)) + ggtitle("Room capacity in different regions in Norway in 2020") + labs(x="Month", y = "Number of rooms") + labs(colour = "Region")
