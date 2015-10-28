# occupation_growth.py
from __future__ import division
import re
import string
import csv
from StringIO import StringIO
import os

# file='/filepath/usa_00005.csv'
# with open (file,'rU') as csvfile:
# 	reader=csv.reader(csvfile)
# 	data=[row for row in reader]
### feed data to format_acs_forinteractive

# execfile('/Users/aclemens/Desktop/occupation_growth.py')
# newempdata=format_acs_forinteractive(empdata)

def format_acs_forinteractive(data):
	# Format of rows in data is:
	# year[0],datanum[1],serial[2],hhwt[3],statefip[4],countyfips[5],gq[6],pernum[7],perwt[8],occ2010[9],uhrswork[10],inctot[11],incwage[12]
	# Little rearranging because I changed datasets and it screwed up all my indices
	data=[[row[0],row[1],row[2],row[3],0,0,row[4],row[5],row[6],row[9],row[10],row[11],row[12],row[7]] for row in data]

	data_employ=[row for row in data[1:] if int(row[13])==1]
	data_wages=[row for row in data[1:] if int(row[10])>=4 and int(row[11])>=35]
	print len(data_employ),len(data_wages)

	professions=list(set([row[0] for row in occ_codes]))
	finalrows=[]

	# construct a line for each profession that is:
	# [profession, 2006 wage, 2006 employment, 2006 hours worked, 2007 wage, 2007 employment, 2007 hours worked, ... ]
	for profession in professions:
		print 'profession',profession

		# assemble list of all rows in data that match profession
		temp_prof_w=[row for row in data_wages if row[9]==profession]
		temp_prof_e=[row for row in data_employ if row[9]==profession]
		
		# start a new row that begins with the profession id
		new_row=[profession]
		
		# loop through years and find appropriate profession/year combo
		years=range(2006,2014,1)
		for year in years:
			year=str(year)
			year_rows_w=[row for row in temp_prof_w if row[0]==year]
			year_rows_e=[row for row in temp_prof_e if row[0]==year]
			# these are: numerator of average wages (weighted total wages), total employment to be used as denominator,
			# numerator for usual hours worked (no longer used)
			# All three are constructed in the loop below.
			wagenum, employcount_w, employcount_e, hrsnum = 0, 0, 0, 0

			for row in year_rows_w:
				wagenum=wagenum+int(row[12])*int(row[8])
				employcount_w=employcount_w+int(row[8])
				hrsnum=hrsnum+int(row[10])*int(row[8])

			for row in year_rows_e:
				employcount_e=employcount_e+int(row[8])

			try:
				new_row.append(wagenum/employcount_w)
			except:
				print 'no employees'
				new_row.append(0)

			new_row.append(employcount_e)

			try:
				new_row.append(hrsnum/employcount_w)
			except:
				print 'no employees'
				new_row.append(0)

		finalrows.append(new_row)

	return finalrows


def wrangle_data(data):
	# Feed format_acs_forinteractive into here.
	# format of data rows:
	# [profession, 2006 wage, 2006 employment, 2006 hours worked, 2007 wage, 2007 employment, 2007 hours worked, ... ]
	inter_rows=[]

	# First remove professions for which there are no observations in *any* single year
	data=[row for row in data if row[1]!=0 and row[2]!=0 and row[3]!=0 and row[4]!=0 and row[5]!=0 and row[6]!=0 and row[7]!=0 and row[8]!=0 and row[9]!=0 and row[10]!=0 and row[11]!=0 and row[12]!=0 and row[13]!=0 and row[14]!=0 and row[15]!=0 and row[16]!=0 and row[17]!=0 and row[18]!=0 and row[19]!=0 and row[20]!=0 and row[21]!=0 and row[22]!=0 and row[23]!=0]
	print len(data)

	# set up low/mid/high divisions based on 2006 wages. First, build a list of wages where each
	# wage is repeated once for each weighted employed person (a leeeeetle inefficient)
	wages_2006=[]
	for row in data:
		for i in range(0,row[2],1):
			wages_2006.append(row[1])

	print len(wages_2006)
	wages_2006=sorted(wages_2006)

	# This sets up the percentiles - adjust cut1 and cut2 to get something other than the 20th and 90th
	cuts=len(wages_2006)/10
	cut1=wages_2006[int(cuts*2)]
	cut2=wages_2006[int(cuts*8)]

	# and now sort occupations into low/mid/high based on 2006 wage
	low_occs=[row for row in data if row[1]<=cut1]
	mid_occs=[row for row in data if row[1]>cut1 and row[1]<cut2]
	high_occs=[row for row in data if row[1]>=cut2]

	# quick sanity check - number of occupations in each group and the actual cuts
	print len(low_occs),len(mid_occs),len(high_occs)
	print wages_2006[int(round(cuts*2))],wages_2006[int(round(cuts*9))]

	# now create the first three rows of our eventual data structure by looping through the three
	# occupation lists and building average wage and total employment data for each. Output rows
	# for javascript are:
	# [sector, subsector, 2007 wage, wage growth, type flag, starting employment index (0),
	# emp index 2008, emp index 2009, emp index 2010...]
	for type in [['low',low_occs],['mid',mid_occs],['high',high_occs]]:
		totalemp2006, totalemp2007, totalemp2008, totalemp2009, totalemp2010, totalemp2011, totalemp2012, totalemp2013 = 0, 0, 0, 0, 0, 0, 0, 0
		average2007, average2013 = 0, 0		

		temp_row=[type[0],type[0]]

		for row in type[1]:
			average2007=average2007+row[4]*row[5]
			average2013=average2013+row[22]*row[23]

			totalemp2006=totalemp2006+row[2]
			totalemp2007=totalemp2007+row[5]
			totalemp2008=totalemp2008+row[8]
			totalemp2009=totalemp2009+row[11]
			totalemp2010=totalemp2010+row[14]
			totalemp2011=totalemp2011+row[17]
			totalemp2012=totalemp2012+row[20]
			totalemp2013=totalemp2013+row[23]

		average2007=average2007/totalemp2007
		average2013=average2013/totalemp2013

		temp_row.extend([average2007,(average2013-average2007)/average2007,-1,0])
		temp_row.extend([(totalemp2008-totalemp2007)/totalemp2007,(totalemp2009-totalemp2007)/totalemp2007,(totalemp2010-totalemp2007)/totalemp2007,(totalemp2011-totalemp2007)/totalemp2007,(totalemp2012-totalemp2007)/totalemp2007,(totalemp2013-totalemp2007)/totalemp2007])
		inter_rows.append(temp_row)

	# Adjust the last number here to screen out professions with small sample sizes
	data=[row for row in data if row[2]>250000]

	# Next create rows for each specific occupation. This is pretty easy since data is already in a
	# occupation by occupation format.
	for code in occ_codes:
		set=[row for row in data if row[0]==code[0]]
		lowoccs=[row[0] for row in low_occs]
		midoccs=[row[0] for row in mid_occs]
		highoccs=[row[0] for row in high_occs]

		if code[0] in lowoccs:
			flag=-1
		if code[0] in midoccs:
			flag=0
		if code[0] in highoccs:
			flag=1

		try:
			new_row=[code[2],code[1],set[0][4],(set[0][22]-set[0][4])/set[0][4],1,0,(set[0][8]-set[0][5])/set[0][5],(set[0][11]-set[0][5])/set[0][5],(set[0][14]-set[0][5])/set[0][5],(set[0][17]-set[0][5])/set[0][5],(set[0][20]-set[0][5])/set[0][5],(set[0][23]-set[0][5])/set[0][5],flag]
			inter_rows.append(new_row)
		except:
			pass

	# Finally, create the aggregated occupation groupings rows
	top_occs=[row[0] for row in inter_rows]
	
	# I was running into some kind of crazy exception using set() so...
	b=[]
	for occ in top_occs:
		if occ not in b:
			b.append(occ)

	top_occs=b
	for occ in top_occs[3:]:
		occ_row=[row[0] for row in occ_codes if row[2]==occ]
		temp_occ=[row for row in data if row[0] in occ_row]
		temp_row=[occ,'none']

		totalemp2006, totalemp2007, totalemp2008, totalemp2009, totalemp2010, totalemp2011, totalemp2012, totalemp2013 = 0, 0, 0, 0, 0, 0, 0, 0
		average2007, average2013 = 0, 0

		for row in temp_occ:
			average2007=average2007+row[4]*row[5]
			average2013=average2013+row[22]*row[23]

			totalemp2006=totalemp2006+row[2]
			totalemp2007=totalemp2007+row[5]
			totalemp2008=totalemp2008+row[8]
			totalemp2009=totalemp2009+row[11]
			totalemp2010=totalemp2010+row[14]
			totalemp2011=totalemp2011+row[17]
			totalemp2012=totalemp2012+row[20]
			totalemp2013=totalemp2013+row[23]

		average2007=average2007/totalemp2007
		average2013=average2013/totalemp2013

		temp_row.extend([average2007,(average2013-average2007)/average2007,0,0])
		temp_row.extend([(totalemp2008-totalemp2007)/totalemp2007,(totalemp2009-totalemp2007)/totalemp2007,(totalemp2010-totalemp2007)/totalemp2007,(totalemp2011-totalemp2007)/totalemp2007,(totalemp2012-totalemp2007)/totalemp2007,(totalemp2013-totalemp2007)/totalemp2007])
		inter_rows.append(temp_row)

	# Just a little formatting to create a nice small javascript object
	for i,row in enumerate(inter_rows):
		row[0]=row[0].lower().title()
		for j,entry in enumerate(row):
			try:
				inter_rows[i][j]=round(entry,3)
			except:
				pass

	inter_rows[0][0]=inter_rows[0][0].lower()
	inter_rows[1][0]=inter_rows[1][0].lower()
	inter_rows[2][0]=inter_rows[2][0].lower()

	return inter_rows








