library(tidyverse)

library(stargazer)
setwd("H:/travel-policy-report/travel-project-report")
seg <- read.csv("data/by_segment.csv",header=TRUE,sep=",")
seg<- seg[ which(seg$paid_fare_including_taxes_and_fees > 0), ]


seg<- seg[ which(seg$YCA_y != 1), ]
seg<- seg[ which(seg$DashCA_y != 1), ]
seg<- seg[ which(seg$count_y == 2), ]
seg <- seg[which(seg$awarded == 1),]
seg$dashPerMile= seg$XCA_FARE / seg$nsmiles
seg$YCAPerMile= seg$YCA_FARE / seg$nsmiles
seg$costPerMile= seg$paid_fare_including_taxes_and_fees / seg$nsmiles
seg$yc_diff = (seg$XCA_FARE /seg$YCA_FARE)


#probability of getting a certain fare type
mylogit <- glm(seg$DashCA_x ~ seg$daily_demand + seg$yc_diff+seg$dashPerMile+  seg$YCAPerMile + seg$no_CA_award +seg$ticketing_adv_booking_group + seg$ticket_exchange_indicator + seg$segment_refund_indicator + seg$city_pair_code, family = "binomial")

summary(mylogit)

mylogit <- glm(seg$YCA_x ~ seg$daily_demand + seg$yc_diff+ seg$ticketing_adv_booking_group +seg$costPerMile+  seg$CAdif + seg$no_CA_award, family = "binomial")
summary(mylogit)

mylogit <- glm(seg$DG_x ~ seg$daily_demand + seg$yc_diff+ seg$ticketing_adv_booking_group +seg$costPerMile+  seg$CAdif + seg$no_CA_award, family = "binomial")

summary(mylogit)



seg <- seg %>% filter(
  fare_type %in% c( "YCA","Dash CA" ,"Other","DG")
)


reg2 <- lm(seg$costPerMile ~ seg$yc_diff + seg$fare_type +seg$segment_refund_indicator + seg$ticket_exchange_indicator+ seg$ticketing_adv_booking_group + seg$fare_type*seg$ticketing_adv_booking_group + seg$airline_carrier+ seg$city_pair_code )
summary(reg2)





df <- read.csv("data/by_quarter.csv",header=TRUE,sep=",")
df<- df[ which(df$no_of_segments >10), ]
df<- df[ which(df$DashCA >0), ]
df$costPerMile = df$fare / df$nsmiles
df$dashPerMile = df$XCA_FARE / df$nsmiles
df$YCAPerMile = df$YCA_FARE / df$nsmiles


df$di  <- df$dashPerMile /df$YCAPerMile 
df$di2  <- df$dashPerMile / df$costPerMile

df$dif = df$XCA_FARE  / df$fare
df$dif2 = df$YCA_FARE  / df$fare
df$diff3 = (df$XCA_FARE / df$YCA_FARE )


reg <- lm(df$DashCA ~  df$di+ df$dashPerMile +df$YCAPerMile +df$large_ms+ df$passengers  + df$X21.Days + df$AIRLINE_ABBREV)
reg <- lm(df$DG ~  df$diff3 + df$dashPerMile +df$YCAPerMile +df$large_ms+ df$passengers  + df$X21.Days + df$AIRLINE_ABBREV)



