# -*- coding: utf-8 -*-



from utils import segment, trip, traveller, route

#call the data class
#data = segment.get()

#data.by_quarter()
#data is specified at segment level of a trip. useful because its the most granular view
#data.by_segment()

#gets data rolled up at quarter level this is usefule becuase consumer level data is at the quarter level
#data.by_quarter()

#gets trip specific view
#trip.get()

#gets a traveller view by year, useful for credit card analysis
#traveller.get()

#saves by route data
route.get()