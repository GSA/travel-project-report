
library(stargazer)

seg <- read.csv("data/by_segment.csv",header=TRUE,sep=",")
seg<- seg[ which(seg$paid_fare_including_taxes_and_fees > 0), ]


seg<- seg[ which(seg$YCA_total != 1), ]
seg<- seg[ which(seg$DashCA_total != 1), ]
seg<- seg[ which(seg$count_total == 2), ]

seg$CAdif= (seg$XCA_FARE - seg$fare)/ seg$nsmiles
seg$dif = (seg$paid_fare_including_taxes_and_fees  - seg$fare)/ seg$nsmiles
seg$yc_diff = (seg$YCA_FARE -seg$XCA_FARE)/ seg$nsmiles



mylogit <- glm(seg$DashCA_x ~ seg$daily_demand + seg$ticketing_adv_booking_group + seg$dif+ seg$CAdif , family = "binomial")
summary(mylogit)
mylogit <- glm(seg$DashCA_x ~ seg$daily_demand + seg$yc_diff+ seg$ticketing_adv_booking_group +  seg$CAdif + seg$no_CA_award, family = "binomial")
summary(mylogit)
stargazer(mylogit,type='html')

reg <- lm(seg$paid_fare_including_taxes_and_fees ~ seg$fare_type +seg$ticketing_adv_booking_group +seg$trip_departure_day_of_week + seg$city_pair_code + seg$airline_carrier)
summary(reg)
reg2 <- lm(seg$paid_fare_including_taxes_and_fees ~ seg$fare_type +seg$segment_refund_indicator + seg$ticket_exchange_indicator+seg$ticketing_adv_booking_group )
summary(reg2)

a <- glm(seg$paid_fare_including_taxes_and_fees ~seg$trip_departure_day_of_week+ seg$fare_type +seg$segment_refund_indicator + seg$ticket_exchange_indicator+seg$ticketing_adv_booking_group + seg$fare_type*seg$ticketing_adv_booking_group)
summary(a)




df <- read.csv("data/by_quarter.csv",header=TRUE,sep=",")
df<- df[ which(df$no_of_segments >10), ]
df$costPerMile = df$fare / df$nsmiles
df$dashPerMile = df$XCA_FARE / df$nsmiles
df$YCAPerMile = df$YCA_FARE / df$nsmiles


df$di  <- df$dashPerMile /df$YCAPerMile 
df$di2  <- df$dashPerMile / df$costPerMile

df$dif = df$XCA_FARE  / df$fare
df$dif2 = df$YCA_FARE  / df$fare
df$diff3 = (df$YCA_FARE - df$XCA_FARE )/df$nsmiles

reg <- lm(df$DashCA ~  df$di + df$dif + df$dashPerMile +df$YCAPerMile +df$large_ms+ df$passengers  + df$X21.Days + df$AIRLINE_ABBREV+ df$no_CA_award)

summary(reg)

