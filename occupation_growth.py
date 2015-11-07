# occupation_growth.py
from __future__ import division
import re
import string
import csv
from StringIO import StringIO
import os
import pandas as pd

occ_codes=[['4410','Personal Care And Service','Motion Picture Projectionists'],['340','Management, Business, Science, And Arts','Lodging Managers'],['425','Management, Business, Science, And Arts','Emergency Management Directors'],['726','Business Operations Specialists','Fundraisers'],['735','Business Operations Specialists','Market Research Analysts and Marketing Specialists'],['9110','Transportation And Material Moving','Ambulance Drivers and Attendants'],['1106','Computer And Mathematical','Computer Network Architects'],['1107','Computer And Mathematical','Computer Occupations, All Other'],['3256','Healthcare Practitioners And Technical','Nurse Anesthetists'],['3258','Healthcare Practitioners And Technical','Nurse Practitioners, and Nurse Midwives'],['9415','Transportation And Material Moving','Transportation Attendants, except flight attendants'],['1340','Architecture And Engineering','Biomedical and agricultural engineers'],['3420','Healthcare Practitioners And Technical','Health practitioner support technologists and technicians'],['3648','Healthcare Support','placeholder1'],['3645','Healthcare Support','placeholder2'],['3646','Healthcare Support','placeholder3'],['3647','Healthcare Support','placeholder4'],['3649','Healthcare Support','placeholder5'],['3655','Healthcare Support','placeholder6'],['3840','Protective Service','placeholder7'],['10', 'Management, Business, Science, And Arts', 'Chief executives and legislators/public administration'], ['20', 'Management, Business, Science, And Arts', 'General and Operations Managers'], ['30', 'Management, Business, Science, And Arts', 'Managers in Marketing, Advertising, and Public Relations'], ['100', 'Management, Business, Science, And Arts', 'Administrative Services Managers'], ['110', 'Management, Business, Science, And Arts', 'Computer and Information Systems Managers'], ['120', 'Management, Business, Science, And Arts', 'Financial Managers'], ['130', 'Management, Business, Science, And Arts', 'Human Resources Managers'], ['140', 'Management, Business, Science, And Arts', 'Industrial Production Managers'], ['150', 'Management, Business, Science, And Arts', 'Purchasing Managers'], ['160', 'Management, Business, Science, And Arts', 'Transportation, Storage, and Distribution Managers'], ['205', 'Management, Business, Science, And Arts', 'Farmers, Ranchers, and Other Agricultural Managers'], ['220', 'Management, Business, Science, And Arts', 'Constructions Managers'], ['230', 'Management, Business, Science, And Arts', 'Education Administrators'], ['300', 'Management, Business, Science, And Arts', 'Architectural and Engineering Managers'], ['310', 'Management, Business, Science, And Arts', 'Food Service and Lodging Managers'], ['320', 'Management, Business, Science, And Arts', 'Funeral Directors'], ['330', 'Management, Business, Science, And Arts', 'Gaming Managers'], ['350', 'Management, Business, Science, And Arts', 'Medical and Health Services Managers'], ['360', 'Management, Business, Science, And Arts', 'Natural Science Managers'], ['410', 'Management, Business, Science, And Arts', 'Property, Real Estate, and Community Association Managers'], ['420', 'Management, Business, Science, And Arts', 'Social and Community Service Managers'], ['430', 'Management, Business, Science, And Arts', 'Managers, nec (including Postmasters)'], ['500', 'Business Operations Specialists', 'Agents and Business Managers of Artists, Performers,  and Athletes'], ['510', 'Business Operations Specialists', 'Buyers and Purchasing Agents, Farm Products'], ['520', 'Business Operations Specialists', 'Wholesale and Retail Buyers, Except Farm Products'], ['530', 'Business Operations Specialists', 'Purchasing Agents, Except Wholesale, Retail, and Farm Products'], ['540', 'Business Operations Specialists', 'Claims Adjusters, Appraisers, Examiners, and Investigators'], ['560', 'Business Operations Specialists', 'Compliance Officers, Except Agriculture'], ['600', 'Business Operations Specialists', 'Cost Estimators'], ['620', 'Business Operations Specialists', 'Human Resources, Training, and Labor Relations Specialists'], ['700', 'Business Operations Specialists', 'Logisticians'], ['710', 'Business Operations Specialists', 'Management Analysts'], ['720', 'Business Operations Specialists', 'Meeting and Convention Planners'], ['730', 'Business Operations Specialists', 'Other Business Operations and Management Specialists'], ['800', 'Financial Specialists', 'Accountants and Auditors'], ['810', 'Financial Specialists', 'Appraisers and Assessors of Real Estate'], ['820', 'Financial Specialists', 'Budget Analysts'], ['830', 'Financial Specialists', 'Credit Analysts'], ['840', 'Financial Specialists', 'Financial Analysts'], ['850', 'Financial Specialists', 'Personal Financial Advisors'], ['860', 'Financial Specialists', 'Insurance Underwriters'], ['900', 'Financial Specialists', 'Financial Examiners'], ['910', 'Financial Specialists', 'Credit Counselors and Loan Officers'], ['930', 'Financial Specialists', 'Tax Examiners and Collectors, and Revenue Agents'], ['940', 'Financial Specialists', 'Tax Preparers'], ['950', 'Financial Specialists', 'Financial Specialists, nec'], ['1000', 'Computer And Mathematical', 'Computer Scientists and Systems Analysts/Network systems Analysts/Web Developers'], ['1010', 'Computer And Mathematical', 'Computer Programmers'], ['1020', 'Computer And Mathematical', 'Software Developers, Applications and Systems Software'], ['1050', 'Computer And Mathematical', 'Computer Support Specialists'], ['1060', 'Computer And Mathematical', 'Database Administrators'], ['1100', 'Computer And Mathematical', 'Network and Computer Systems Administrators'], ['1200', 'Computer And Mathematical', 'Actuaries'], ['1220', 'Computer And Mathematical', 'Operations Research Analysts'], ['1230', 'Computer And Mathematical', 'Statisticians'], ['1240', 'Computer And Mathematical', 'Mathematical science occupations, nec'], ['1300', 'Architecture And Engineering', 'Architects, Except Naval'], ['1310', 'Architecture And Engineering', 'Surveyors, Cartographers, and Photogrammetrists'], ['1320', 'Architecture And Engineering', 'Aerospace Engineers'], ['1350', 'Architecture And Engineering', 'Chemical Engineers'], ['1360', 'Architecture And Engineering', 'Civil Engineers'], ['1400', 'Architecture And Engineering', 'Computer Hardware Engineers'], ['1410', 'Architecture And Engineering', 'Electrical and Electronics Engineers'], ['1420', 'Architecture And Engineering', 'Environmental Engineers'], ['1430', 'Architecture And Engineering', 'Industrial Engineers, including Health and Safety'], ['1440', 'Architecture And Engineering', 'Marine Engineers and Naval Architects'], ['1450', 'Architecture And Engineering', 'Materials Engineers'], ['1460', 'Architecture And Engineering', 'Mechanical Engineers'], ['1520', 'Architecture And Engineering', 'Petroleum, mining and geological engineers, including mining safety engineers'], ['1530', 'Architecture And Engineering', 'Engineers, nec'], ['1540', 'Architecture And Engineering', 'Drafters'], ['1550', 'Technicians', 'Engineering Technicians, Except Drafters'], ['1560', 'Technicians', 'Surveying and Mapping Technicians'], ['1600', 'Life, Physical, And Social Science', 'Agricultural and Food Scientists'], ['1610', 'Life, Physical, And Social Science', 'Biological Scientists'], ['1640', 'Life, Physical, And Social Science', 'Conservation Scientists and Foresters'], ['1650', 'Life, Physical, And Social Science', 'Medical Scientists, and Life Scientists, All Other'], ['1700', 'Life, Physical, And Social Science', 'Astronomers and Physicists'], ['1710', 'Life, Physical, And Social Science', 'Atmospheric and Space Scientists'], ['1720', 'Life, Physical, And Social Science', 'Chemists and Materials Scientists'], ['1740', 'Life, Physical, And Social Science', 'Environmental Scientists and Geoscientists'], ['1760', 'Life, Physical, And Social Science', 'Physical Scientists, nec'], ['1800', 'Life, Physical, And Social Science', 'Economists and market researchers'], ['1810', 'Life, Physical, And Social Science', ''], ['1820', 'Life, Physical, And Social Science', 'Psychologists'], ['1830', 'Life, Physical, And Social Science', 'Urban and Regional Planners'], ['1840', 'Life, Physical, And Social Science', 'Social Scientists, nec'], ['1900', 'Life, Physical, And Social Science', 'Agricultural and Food Science Technicians'], ['1910', 'Life, Physical, And Social Science', 'Biological Technicians'], ['1920', 'Life, Physical, And Social Science', 'Chemical Technicians'], ['1930', 'Life, Physical, And Social Science', 'Geological and Petroleum Technicians, and Nuclear Technicians'], ['1960', 'Life, Physical, And Social Science', 'Life, Physical, and Social Science Technicians, nec'], ['1980', 'Life, Physical, And Social Science', 'Professional, Research, or Technical Workers, nec'], ['2000', 'Community And Social Services', 'Counselors'], ['2010', 'Community And Social Services', 'Social Workers'], ['2020', 'Community And Social Services', 'Community and Social Service Specialists, nec'], ['2040', 'Community And Social Services', 'Clergy'], ['2050', 'Community And Social Services', 'Directors, Religious Activities and Education'], ['2060', 'Community And Social Services', 'Religious Workers, nec'], ['2100', 'Legal', 'Lawyers, and judges, magistrates, and other judicial workers'], ['2140', 'Legal', 'Paralegals and Legal Assistants'], ['2150', 'Legal', 'Legal Support Workers, nec'], ['2200', 'Education, Training, And Library', 'Postsecondary Teachers'], ['2300', 'Education, Training, And Library', 'Preschool and Kindergarten Teachers'], ['2310', 'Education, Training, And Library', 'Elementary and Middle School Teachers'], ['2320', 'Education, Training, And Library', 'Secondary School Teachers'], ['2330', 'Education, Training, And Library', 'Special Education Teachers'], ['2340', 'Education, Training, And Library', 'Other Teachers and Instructors'], ['2400', 'Education, Training, And Library', 'Archivists, Curators, and Museum Technicians'], ['2430', 'Education, Training, And Library', 'Librarians'], ['2440', 'Education, Training, And Library', 'Library Technicians'], ['2540', 'Education, Training, And Library', 'Teacher Assistants'], ['2550', 'Education, Training, And Library', 'Education, Training, and Library Workers, nec'], ['2600', 'Arts, Design, Entertainment, Sports, And Media', 'Artists and Related Workers'], ['2630', 'Arts, Design, Entertainment, Sports, And Media', 'Designers'], ['2700', 'Arts, Design, Entertainment, Sports, And Media', 'Actors, Producers, and Directors'], ['2720', 'Arts, Design, Entertainment, Sports, And Media', 'Athletes, Coaches, Umpires, and Related Workers'], ['2740', 'Arts, Design, Entertainment, Sports, And Media', 'Dancers and Choreographers'], ['2750', 'Arts, Design, Entertainment, Sports, And Media', 'Musicians, Singers, and Related Workers'], ['2760', 'Arts, Design, Entertainment, Sports, And Media', 'Entertainers and Performers, Sports and Related Workers, All Other'], ['2800', 'Arts, Design, Entertainment, Sports, And Media', 'Announcers'], ['2810', 'Arts, Design, Entertainment, Sports, And Media', 'Editors, News Analysts, Reporters, and Correspondents'], ['2825', 'Arts, Design, Entertainment, Sports, And Media', 'Public Relations Specialists'], ['2840', 'Arts, Design, Entertainment, Sports, And Media', 'Technical Writers'], ['2850', 'Arts, Design, Entertainment, Sports, And Media', 'Writers and Authors'], ['2860', 'Arts, Design, Entertainment, Sports, And Media', 'Media and Communication Workers, nec'], ['2900', 'Arts, Design, Entertainment, Sports, And Media', 'Broadcast and Sound Engineering Technicians and Radio Operators, and media and communication equipment workers, all other'], ['2910', 'Arts, Design, Entertainment, Sports, And Media', 'Photographers'], ['2920', 'Arts, Design, Entertainment, Sports, And Media', 'Television, Video, and Motion Picture Camera Operators and Editors'], ['3000', 'Healthcare Practitioners And Technical', 'Chiropractors'], ['3010', 'Healthcare Practitioners And Technical', 'Dentists'], ['3030', 'Healthcare Practitioners And Technical', 'Dieticians and Nutritionists'], ['3040', 'Healthcare Practitioners And Technical', 'Optometrists'], ['3050', 'Healthcare Practitioners And Technical', 'Pharmacists'], ['3060', 'Healthcare Practitioners And Technical', 'Physicians and Surgeons'], ['3110', 'Healthcare Practitioners And Technical', 'Physician Assistants'], ['3120', 'Healthcare Practitioners And Technical', 'Podiatrists'], ['3130', 'Healthcare Practitioners And Technical', 'Registered Nurses'], ['3140', 'Healthcare Practitioners And Technical', 'Audiologists'], ['3150', 'Healthcare Practitioners And Technical', 'Occupational Therapists'], ['3160', 'Healthcare Practitioners And Technical', 'Physical Therapists'], ['3200', 'Healthcare Practitioners And Technical', 'Radiation Therapists'], ['3210', 'Healthcare Practitioners And Technical', 'Recreational Therapists'], ['3220', 'Healthcare Practitioners And Technical', 'Respiratory Therapists'], ['3230', 'Healthcare Practitioners And Technical', 'Speech Language Pathologists'], ['3240', 'Healthcare Practitioners And Technical', 'Therapists, nec'], ['3250', 'Healthcare Practitioners And Technical', 'Veterinarians'], ['3260', 'Healthcare Practitioners And Technical', 'Health Diagnosing and Treating Practitioners, nec'], ['3300', 'Healthcare Practitioners And Technical', 'Clinical Laboratory Technologists and Technicians'], ['3310', 'Healthcare Practitioners And Technical', 'Dental Hygienists'], ['3320', 'Healthcare Practitioners And Technical', 'Diagnostic Related Technologists and Technicians'], ['3400', 'Healthcare Practitioners And Technical', 'Emergency Medical Technicians and Paramedics'], ['3410', 'Healthcare Practitioners And Technical', 'Health Diagnosing and Treating Practitioner Support Technicians'], ['3500', 'Healthcare Practitioners And Technical', 'Licensed Practical and Licensed Vocational Nurses'], ['3510', 'Healthcare Practitioners And Technical', 'Medical Records and Health Information Technicians'], ['3520', 'Healthcare Practitioners And Technical', 'Opticians, Dispensing'], ['3530', 'Healthcare Practitioners And Technical', 'Health Technologists and Technicians, nec'], ['3540', 'Healthcare Practitioners And Technical', 'Healthcare Practitioners and Technical Occupations, nec'], ['3600', 'Healthcare Support', 'Nursing, Psychiatric, and Home Health Aides'], ['3610', 'Healthcare Support', 'Occupational Therapy Assistants and Aides'], ['3620', 'Healthcare Support', 'Physical Therapist Assistants and Aides'], ['3630', 'Healthcare Support', 'Massage Therapists'], ['3640', 'Healthcare Support', 'Dental Assistants'], ['3650', 'Healthcare Support', 'Medical Assistants and Other Healthcare Support Occupations, nec'], ['3700', 'Protective Service', 'First-Line Supervisors of Correctional Officers'], ['3710', 'Protective Service', 'First-Line Supervisors of Police and Detectives'], ['3720', 'Protective Service', 'First-Line Supervisors of Fire Fighting and Prevention Workers'], ['3730', 'Protective Service', 'Supervisors, Protective Service Workers, All Other'], ['3740', 'Protective Service', 'Firefighters'], ['3750', 'Protective Service', 'Fire Inspectors'], ['3800', 'Protective Service', 'Sheriffs, Bailiffs, Correctional Officers, and Jailers'], ['3820', 'Protective Service', 'Police Officers and Detectives'], ['3900', 'Protective Service', 'Animal Control'], ['3910', 'Protective Service', 'Private Detectives and Investigators'], ['3930', 'Protective Service', 'Security Guards and Gaming Surveillance Officers'], ['3940', 'Protective Service', 'Crossing Guards'], ['4000', 'Food Preparation And Serving', 'Chefs and Cooks'], ['4010', 'Food Preparation And Serving', 'First-Line Supervisors of Food Preparation and Serving Workers'], ['4030', 'Food Preparation And Serving', 'Food Preparation Workers'], ['4040', 'Food Preparation And Serving', 'Bartenders'], ['4050', 'Food Preparation And Serving', 'Combined Food Preparation and Serving Workers, Including Fast Food'], ['4060', 'Food Preparation And Serving', 'Counter Attendant, Cafeteria, Food Concession, and Coffee Shop'], ['4110', 'Food Preparation And Serving', 'Waiters and Waitresses'], ['4120', 'Food Preparation And Serving', 'Food Servers, Nonrestaurant'], ['4130', 'Food Preparation And Serving', 'Food preparation and serving related workers, nec'], ['4140', 'Food Preparation And Serving', 'Dishwashers'], ['4150', 'Food Preparation And Serving', 'Host and Hostesses, Restaurant, Lounge, and Coffee Shop'], ['4200', 'Building And Grounds Cleaning And Maintenance', 'First-Line Supervisors of Housekeeping and Janitorial Workers'], ['4210', 'Building And Grounds Cleaning And Maintenance', 'First-Line Supervisors of Landscaping, Lawn Service, and Groundskeeping Workers'], ['4220', 'Building And Grounds Cleaning And Maintenance', 'Janitors and Building Cleaners'], ['4230', 'Building And Grounds Cleaning And Maintenance', 'Maids and Housekeeping Cleaners'], ['4240', 'Building And Grounds Cleaning And Maintenance', 'Pest Control Workers'], ['4250', 'Building And Grounds Cleaning And Maintenance', 'Grounds Maintenance Workers'], ['4300', 'Personal Care And Service', 'First-Line Supervisors of Gaming Workers'], ['4320', 'Personal Care And Service', 'First-Line Supervisors of Personal Service Workers'], ['4340', 'Personal Care And Service', 'Animal Trainers'], ['4350', 'Personal Care And Service', 'Nonfarm Animal Caretakers'], ['4400', 'Personal Care And Service', 'Gaming Services Workers'], ['4420', 'Personal Care And Service', 'Ushers, Lobby Attendants, and Ticket Takers'], ['4430', 'Personal Care And Service', 'Entertainment Attendants and Related Workers, nec'], ['4460', 'Personal Care And Service', 'Funeral Service Workers and Embalmers'], ['4500', 'Personal Care And Service', 'Barbers'], ['4510', 'Personal Care And Service', 'Hairdressers, Hairstylists, and Cosmetologists'], ['4520', 'Personal Care And Service', 'Personal Appearance Workers, nec'], ['4530', 'Personal Care And Service', 'Baggage Porters, Bellhops, and Concierges'], ['4540', 'Personal Care And Service', 'Tour and Travel Guides'], ['4600', 'Personal Care And Service', 'Childcare Workers'], ['4610', 'Personal Care And Service', 'Personal Care Aides'], ['4620', 'Personal Care And Service', 'Recreation and Fitness Workers'], ['4640', 'Personal Care And Service', 'Residential Advisors'], ['4650', 'Personal Care And Service', 'Personal Care and Service Workers, All Other'], ['4700', 'Sales And Related', 'First-Line Supervisors of Sales Workers'], ['4720', 'Sales And Related', 'Cashiers'], ['4740', 'Sales And Related', 'Counter and Rental Clerks'], ['4750', 'Sales And Related', 'Parts Salespersons'], ['4760', 'Sales And Related', 'Retail Salespersons'], ['4800', 'Sales And Related', 'Advertising Sales Agents'], ['4810', 'Sales And Related', 'Insurance Sales Agents'], ['4820', 'Sales And Related', 'Securities, Commodities, and Financial Services Sales Agents'], ['4830', 'Sales And Related', 'Travel Agents'], ['4840', 'Sales And Related', 'Sales Representatives, Services, All Other'], ['4850', 'Sales And Related', 'Sales Representatives, Wholesale and Manufacturing'], ['4900', 'Sales And Related', 'Models, Demonstrators, and Product Promoters'], ['4920', 'Sales And Related', 'Real Estate Brokers and Sales Agents'], ['4930', 'Sales And Related', 'Sales Engineers'], ['4940', 'Sales And Related', 'Telemarketers'], ['4950', 'Sales And Related', 'Door-to-Door Sales Workers, News and Street Vendors, and Related Workers'], ['4965', 'Sales And Related', 'Sales and Related Workers, All Other'], ['5000', 'Office And Administrative Support', 'First-Line Supervisors of Office and Administrative Support Workers'], ['5010', 'Office And Administrative Support', 'Switchboard Operators, Including Answering Service'], ['5020', 'Office And Administrative Support', 'Telephone Operators'], ['5030', 'Office And Administrative Support', 'Communications Equipment Operators, All Other'], ['5100', 'Office And Administrative Support', 'Bill and Account Collectors'], ['5110', 'Office And Administrative Support', 'Billing and Posting Clerks'], ['5120', 'Office And Administrative Support', 'Bookkeeping, Accounting, and Auditing Clerks'], ['5130', 'Office And Administrative Support', 'Gaming Cage Workers'], ['5140', 'Office And Administrative Support', 'Payroll and Timekeeping Clerks'], ['5150', 'Office And Administrative Support', 'Procurement Clerks'], ['5160', 'Office And Administrative Support', 'Bank Tellers'], ['5165', 'Office And Administrative Support', 'Financial Clerks, nec'], ['5200', 'Office And Administrative Support', 'Brokerage Clerks'], ['5220', 'Office And Administrative Support', 'Court, Municipal, and License Clerks'], ['5230', 'Office And Administrative Support', 'Credit Authorizers, Checkers, and Clerks'], ['5240', 'Office And Administrative Support', 'Customer Service Representatives'], ['5250', 'Office And Administrative Support', 'Eligibility Interviewers, Government Programs'], ['5260', 'Office And Administrative Support', 'File Clerks'], ['5300', 'Office And Administrative Support', 'Hotel, Motel, and Resort Desk Clerks'], ['5310', 'Office And Administrative Support', 'Interviewers, Except Eligibility and Loan'], ['5320', 'Office And Administrative Support', 'Library Assistants, Clerical'], ['5330', 'Office And Administrative Support', 'Loan Interviewers and Clerks'], ['5340', 'Office And Administrative Support', 'New Account Clerks'], ['5350', 'Office And Administrative Support', 'Correspondent clerks and order clerks'], ['5360', 'Office And Administrative Support', 'Human Resources Assistants, Except Payroll and Timekeeping'], ['5400', 'Office And Administrative Support', 'Receptionists and Information Clerks'], ['5410', 'Office And Administrative Support', 'Reservation and Transportation Ticket Agents and Travel Clerks'], ['5420', 'Office And Administrative Support', 'Information and Record Clerks, All Other'], ['5500', 'Office And Administrative Support', 'Cargo and Freight Agents'], ['5510', 'Office And Administrative Support', 'Couriers and Messengers'], ['5520', 'Office And Administrative Support', 'Dispatchers'], ['5530', 'Office And Administrative Support', 'Meter Readers, Utilities'], ['5540', 'Office And Administrative Support', 'Postal Service Clerks'], ['5550', 'Office And Administrative Support', 'Postal Service Mail Carriers'], ['5560', 'Office And Administrative Support', 'Postal Service Mail Sorters, Processors, and Processing Machine Operators'], ['5600', 'Office And Administrative Support', 'Production, Planning, and Expediting Clerks'], ['5610', 'Office And Administrative Support', 'Shipping, Receiving, and Traffic Clerks'], ['5620', 'Office And Administrative Support', 'Stock Clerks and Order Fillers'], ['5630', 'Office And Administrative Support', 'Weighers, Measurers, Checkers, and Samplers, Recordkeeping'], ['5700', 'Office And Administrative Support', 'Secretaries and Administrative Assistants'], ['5800', 'Office And Administrative Support', 'Computer Operators'], ['5810', 'Office And Administrative Support', 'Data Entry Keyers'], ['5820', 'Office And Administrative Support', 'Word Processors and Typists'], ['5840', 'Office And Administrative Support', 'Insurance Claims and Policy Processing Clerks'], ['5850', 'Office And Administrative Support', 'Mail Clerks and Mail Machine Operators, Except Postal Service'], ['5860', 'Office And Administrative Support', 'Office Clerks, General'], ['5900', 'Office And Administrative Support', 'Office Machine Operators, Except Computer'], ['5910', 'Office And Administrative Support', 'Proofreaders and Copy Markers'], ['5920', 'Office And Administrative Support', 'Statistical Assistants'], ['5940', 'Office And Administrative Support', 'Office and administrative support workers, nec'], ['6005', 'Farming, Fishing, And Forestry', 'First-Line Supervisors of Farming, Fishing, and Forestry Workers'], ['6010', 'Farming, Fishing, And Forestry', 'Agricultural Inspectors'], ['6040', 'Farming, Fishing, And Forestry', 'Graders and Sorters, Agricultural Products'], ['6050', 'Farming, Fishing, And Forestry', 'Agricultural workers, nec'], ['6100', 'Farming, Fishing, And Forestry', 'Fishing and hunting workers'], ['6120', 'Farming, Fishing, And Forestry', 'Forest and Conservation Workers'], ['6130', 'Farming, Fishing, And Forestry', 'Logging Workers'], ['6200', 'Construction', 'First-Line Supervisors of Construction Trades and Extraction Workers'], ['6210', 'Construction', 'Boilermakers'], ['6220', 'Construction', 'Brickmasons, Blockmasons, and Stonemasons'], ['6230', 'Construction', 'Carpenters'], ['6240', 'Construction', 'Carpet, Floor, and Tile Installers and Finishers'], ['6250', 'Construction', 'Cement Masons, Concrete Finishers, and Terrazzo Workers'], ['6260', 'Construction', 'Construction Laborers'], ['6300', 'Construction', 'Paving, Surfacing, and Tamping Equipment Operators'], ['6320', 'Construction', 'Construction equipment operators except paving, surfacing, and tamping equipment operators'], ['6330', 'Construction', 'Drywall Installers, Ceiling Tile Installers, and Tapers'], ['6355', 'Construction', 'Electricians'], ['6360', 'Construction', 'Glaziers'], ['6400', 'Construction', 'Insulation Workers'], ['6420', 'Construction', 'Painters, Construction and Maintenance'], ['6430', 'Construction', 'Paperhangers'], ['6440', 'Construction', 'Pipelayers, Plumbers, Pipefitters, and Steamfitters'], ['6460', 'Construction', 'Plasterers and Stucco Masons'], ['6500', 'Construction', 'Reinforcing Iron and Rebar Workers'], ['6515', 'Construction', 'Roofers'], ['6520', 'Construction', 'Sheet Metal Workers, metal-working'], ['6530', 'Construction', 'Structural Iron and Steel Workers'], ['6600', 'Construction', 'Helpers, Construction Trades'], ['6660', 'Construction', 'Construction and Building Inspectors'], ['6700', 'Construction', 'Elevator Installers and Repairers'], ['6710', 'Construction', 'Fence Erectors'], ['6720', 'Construction', 'Hazardous Materials Removal Workers'], ['6730', 'Construction', 'Highway Maintenance Workers'], ['6740', 'Construction', 'Rail-Track Laying and Maintenance Equipment Operators'], ['6765', 'Construction', 'Construction workers, nec'], ['6800', 'Extraction', 'Derrick, rotary drill, and service unit operators, and roustabouts, oil, gas, and mining'], ['6820', 'Extraction', 'Earth Drillers, Except Oil and Gas'], ['6830', 'Extraction', 'Explosives Workers, Ordnance Handling Experts, and Blasters'], ['6840', 'Extraction', 'Mining Machine Operators'], ['6940', 'Extraction', 'Extraction workers, nec'], ['7000', 'Installation, Maintenance, And Repair', 'First-Line Supervisors of Mechanics, Installers, and Repairers'], ['7010', 'Installation, Maintenance, And Repair', 'Computer, Automated Teller, and Office Machine Repairers'], ['7020', 'Installation, Maintenance, And Repair', 'Radio and Telecommunications Equipment Installers and Repairers'], ['7030', 'Installation, Maintenance, And Repair', 'Avionics Technicians'], ['7040', 'Installation, Maintenance, And Repair', 'Electric Motor, Power Tool, and Related Repairers'], ['7100', 'Installation, Maintenance, And Repair', 'Electrical and electronics repairers, transportation equipment, and industrial and utility'], ['7110', 'Installation, Maintenance, And Repair', 'Electronic Equipment Installers and Repairers, Motor Vehicles'], ['7120', 'Installation, Maintenance, And Repair', 'Electronic Home Entertainment Equipment Installers and Repairers'], ['7125', 'Installation, Maintenance, And Repair', 'Electronic Repairs, nec'], ['7130', 'Installation, Maintenance, And Repair', 'Security and Fire Alarm Systems Installers'], ['7140', 'Installation, Maintenance, And Repair', 'Aircraft Mechanics and Service Technicians'], ['7150', 'Installation, Maintenance, And Repair', 'Automotive Body and Related Repairers'], ['7160', 'Installation, Maintenance, And Repair', 'Automotive Glass Installers and Repairers'], ['7200', 'Installation, Maintenance, And Repair', 'Automotive Service Technicians and Mechanics'], ['7210', 'Installation, Maintenance, And Repair', 'Bus and Truck Mechanics and Diesel Engine Specialists'], ['7220', 'Installation, Maintenance, And Repair', 'Heavy Vehicle and Mobile Equipment Service Technicians and Mechanics'], ['7240', 'Installation, Maintenance, And Repair', 'Small Engine Mechanics'], ['7260', 'Installation, Maintenance, And Repair', 'Vehicle and Mobile Equipment Mechanics, Installers, and Repairers, nec'], ['7300', 'Installation, Maintenance, And Repair', 'Control and Valve Installers and Repairers'], ['7315', 'Installation, Maintenance, And Repair', 'Heating, Air Conditioning, and Refrigeration Mechanics and Installers'], ['7320', 'Installation, Maintenance, And Repair', 'Home Appliance Repairers'], ['7330', 'Installation, Maintenance, And Repair', 'Industrial and Refractory Machinery Mechanics'], ['7340', 'Installation, Maintenance, And Repair', 'Maintenance and Repair Workers, General'], ['7350', 'Installation, Maintenance, And Repair', 'Maintenance Workers, Machinery'], ['7360', 'Installation, Maintenance, And Repair', 'Millwrights'], ['7410', 'Installation, Maintenance, And Repair', 'Electrical Power-Line Installers and Repairers'], ['7420', 'Installation, Maintenance, And Repair', 'Telecommunications Line Installers and Repairers'], ['7430', 'Installation, Maintenance, And Repair', 'Precision Instrument and Equipment Repairers'], ['7510', 'Installation, Maintenance, And Repair', 'Coin, Vending, and Amusement Machine Servicers and Repairers'], ['7540', 'Installation, Maintenance, And Repair', 'Locksmiths and Safe Repairers'], ['7550', 'Installation, Maintenance, And Repair', 'Manufactured Building and Mobile Home Installers'], ['7560', 'Installation, Maintenance, And Repair', 'Riggers'], ['7610', 'Installation, Maintenance, And Repair', 'Helpers--Installation, Maintenance, and Repair Workers'], ['7630', 'Installation, Maintenance, And Repair', 'Other Installation, Maintenance, and Repair Workers Including Wind Turbine Service Technicians, and Commercial Divers, and Signal and Track Switch Repairers'], ['7700', 'Production', 'First-Line Supervisors of Production and Operating Workers'], ['7710', 'Production', 'Aircraft Structure, Surfaces, Rigging, and Systems Assemblers'], ['7720', 'Production', 'Electrical, Electronics, and Electromechanical Assemblers'], ['7730', 'Production', 'Engine and Other Machine Assemblers'], ['7740', 'Production', 'Structural Metal Fabricators and Fitters'], ['7750', 'Production', 'Assemblers and Fabricators, nec'], ['7800', 'Production', 'Bakers'], ['7810', 'Production', 'Butchers and Other Meat, Poultry, and Fish Processing Workers'], ['7830', 'Production', 'Food and Tobacco Roasting, Baking, and Drying Machine Operators and Tenders'], ['7840', 'Production', 'Food Batchmakers'], ['7850', 'Production', 'Food Cooking Machine Operators and Tenders'], ['7855', 'Production', 'Food Processing, nec'], ['7900', 'Production', 'Computer Control Programmers and Operators'], ['7920', 'Production', 'Extruding and Drawing Machine Setters, Operators, and Tenders, Metal and Plastic'], ['7930', 'Production', 'Forging Machine Setters, Operators, and Tenders, Metal and Plastic'], ['7940', 'Production', 'Rolling Machine Setters, Operators, and Tenders, metal and Plastic'], ['7950', 'Production', 'Cutting, Punching, and Press Machine Setters, Operators, and Tenders, Metal and Plastic'], ['7960', 'Production', 'Drilling and Boring Machine Tool Setters, Operators, and Tenders, Metal and Plastic'], ['8000', 'Production', 'Grinding, Lapping, Polishing, and Buffing Machine Tool Setters, Operators, and Tenders, Metal and Plastic'], ['8010', 'Production', 'Lathe and Turning Machine Tool Setters, Operators, and Tenders, Metal and Plastic'], ['8030', 'Production', 'Machinists'], ['8040', 'Production', 'Metal Furnace Operators, Tenders, Pourers, and Casters'], ['8060', 'Production', 'Model Makers and Patternmakers, Metal and Plastic'], ['8100', 'Production', 'Molders and Molding Machine Setters, Operators, and Tenders, Metal and Plastic'], ['8130', 'Production', 'Tool and Die Makers'], ['8140', 'Production', 'Welding, Soldering, and Brazing Workers'], ['8150', 'Production', 'Heat Treating Equipment Setters, Operators, and Tenders, Metal and Plastic'], ['8200', 'Production', 'Plating and Coating Machine Setters, Operators, and Tenders, Metal and Plastic'], ['8210', 'Production', 'Tool Grinders, Filers, and Sharpeners'], ['8220', 'Production', 'Metal workers and plastic workers, nec'], ['8230', 'Production', 'Bookbinders, Printing Machine Operators, and Job Printers'], ['8250', 'Production', 'Prepress Technicians and Workers'], ['8300', 'Production', 'Laundry and Dry-Cleaning Workers'], ['8310', 'Production', 'Pressers, Textile, Garment, and Related Materials'], ['8320', 'Production', 'Sewing Machine Operators'], ['8330', 'Production', 'Shoe and Leather Workers and Repairers'], ['8340', 'Production', 'Shoe Machine Operators and Tenders'], ['8350', 'Production', 'Tailors, Dressmakers, and Sewers'], ['8400', 'Production', 'Textile bleaching and dyeing, and cutting machine setters, operators, and tenders'], ['8410', 'Production', 'Textile Knitting and Weaving Machine Setters, Operators, and Tenders'], ['8420', 'Production', 'Textile Winding, Twisting, and Drawing Out Machine Setters, Operators, and Tenders'], ['8450', 'Production', 'Upholsterers'], ['8460', 'Production', 'Textile, Apparel, and Furnishings workers, nec'], ['8500', 'Production', 'Cabinetmakers and Bench Carpenters'], ['8510', 'Production', 'Furniture Finishers'], ['8530', 'Production', 'Sawing Machine Setters, Operators, and Tenders, Wood'], ['8540', 'Production', 'Woodworking Machine Setters, Operators, and Tenders, Except Sawing'], ['8550', 'Production', 'Woodworkers including model makers and patternmakers, nec'], ['8600', 'Production', 'Power Plant Operators, Distributors, and Dispatchers'], ['8610', 'Production', 'Stationary Engineers and Boiler Operators'], ['8620', 'Production', 'Water Wastewater Treatment Plant and System Operators'], ['8630', 'Production', 'Plant and System Operators, nec'], ['8640', 'Production', 'Chemical Processing Machine Setters, Operators, and Tenders'], ['8650', 'Production', 'Crushing, Grinding, Polishing, Mixing, and Blending Workers'], ['8710', 'Production', 'Cutting Workers'], ['8720', 'Production', 'Extruding, Forming, Pressing, and Compacting Machine Setters, Operators, and Tenders'], ['8730', 'Production', 'Furnace, Kiln, Oven, Drier, and Kettle Operators and Tenders'], ['8740', 'Production', 'Inspectors, Testers, Sorters, Samplers, and Weighers'], ['8750', 'Production', 'Jewelers and Precious Stone and Metal Workers'], ['8760', 'Production', 'Medical, Dental, and Ophthalmic Laboratory Technicians'], ['8800', 'Production', 'Packaging and Filling Machine Operators and Tenders'], ['8810', 'Production', 'Painting Workers and Dyers'], ['8830', 'Production', 'Photographic Process Workers and Processing Machine Operators'], ['8850', 'Production', 'Adhesive Bonding Machine Operators and Tenders'], ['8860', 'Production', 'Cleaning, Washing, and Metal Pickling Equipment Operators and Tenders'], ['8910', 'Production', 'Etchers, Engravers, and Lithographers'], ['8920', 'Production', 'Molders, Shapers, and Casters, Except Metal and Plastic'], ['8930', 'Production', 'Paper Goods Machine Setters, Operators, and Tenders'], ['8940', 'Production', 'Tire Builders'], ['8950', 'Production', 'Helpers--Production Workers'], ['8965', 'Production', 'Other production workers including semiconductor processors and cooling and freezing equipment operators'], ['9000', 'Transportation And Material Moving', 'Supervisors of Transportation and Material Moving Workers'], ['9030', 'Transportation And Material Moving', 'Aircraft Pilots and Flight Engineers'], ['9040', 'Transportation And Material Moving', 'Air Traffic Controllers and Airfield Operations Specialists'], ['9050', 'Transportation And Material Moving', 'Flight Attendants and Transportation Workers and Attendants'], ['9100', 'Transportation And Material Moving', 'Bus and Ambulance Drivers and Attendants'], ['9130', 'Transportation And Material Moving', 'Driver/Sales Workers and Truck Drivers'], ['9140', 'Transportation And Material Moving', 'Taxi Drivers and Chauffeurs'], ['9150', 'Transportation And Material Moving', 'Motor Vehicle Operators, All Other'], ['9200', 'Transportation And Material Moving', 'Locomotive Engineers and Operators'], ['9230', 'Transportation And Material Moving', 'Railroad Brake, Signal, and Switch Operators'], ['9240', 'Transportation And Material Moving', 'Railroad Conductors and Yardmasters'], ['9260', 'Transportation And Material Moving', 'Subway, Streetcar, and Other Rail Transportation Workers'], ['9300', 'Transportation And Material Moving', 'Sailors and marine oilers, and ship engineers'], ['9310', 'Transportation And Material Moving', 'Ship and Boat Captains and Operators'], ['9350', 'Transportation And Material Moving', 'Parking Lot Attendants'], ['9360', 'Transportation And Material Moving', 'Automotive and Watercraft Service Attendants'], ['9410', 'Transportation And Material Moving', 'Transportation Inspectors'], ['9420', 'Transportation And Material Moving', 'Transportation workers, nec'], ['9510', 'Transportation And Material Moving', 'Crane and Tower Operators'], ['9520', 'Transportation And Material Moving', 'Dredge, Excavating, and Loading Machine Operators'], ['9560', 'Transportation And Material Moving', 'Conveyor operators and tenders, and hoist and winch operators'], ['9600', 'Transportation And Material Moving', 'Industrial Truck and Tractor Operators'], ['9610', 'Transportation And Material Moving', 'Cleaners of Vehicles and Equipment'], ['9620', 'Transportation And Material Moving', 'Laborers and Freight, Stock, and Material Movers, Hand'], ['9630', 'Transportation And Material Moving', 'Machine Feeders and Offbearers'], ['9640', 'Transportation And Material Moving', 'Packers and Packagers, Hand'], ['9650', 'Transportation And Material Moving', 'Pumping Station Operators'], ['9720', 'Transportation And Material Moving', 'Refuse and Recyclable Material Collectors'], ['9750', 'Transportation And Material Moving', 'Material moving workers, nec'], ['9800', 'Military Specific', 'Military Officer Special and Tactical Operations Leaders'], ['9810', 'Military Specific', 'First-Line Enlisted Military Supervisors'], ['9820', 'Military Specific', 'Military Enlisted Tactical Operations and Air/Weapons Specialists and Crew Members'], ['9830', 'Military Specific', 'Military, Rank Not Specified']]


def clean_2014pums(file1='/Users/austinc/Desktop/csv_pus/ss14pusa.csv',file2='/Users/austinc/Desktop/csv_pus/ss14pusb.csv'):
	# clean the raw pums data from the census for 2014
	with open(file1,'rU') as csvfile:
		reader=csv.reader(csvfile)
		data=[row for row in reader]

	print '1 loaded'
	head=data[0]
	occ2010=head.index('OCCP')
	perwt=head.index('PWGTP')
	uhrswork=head.index('WKHP')
	inctot=head.index('PINCP')
	incwage=head.index('WAGP')
	empstat=head.index('ESR')
	wkswork2=head.index('WKW')

	data_2014=[]
	for row in data[1:]:
		try:
			data_2014.append([2014,0,0,0,0,0,int(row[perwt]),int(row[empstat]),int(row[empstat]),int(row[occ2010]),int(row[wkswork2]),int(row[uhrswork]),int(row[inctot]),int(row[incwage])])
		except:
			pass

	print '1 appended'

	with open(file2,'rU') as csvfile:
		reader=csv.reader(csvfile)
		data=[row for row in reader]

	print '2 loaded'
	head=data[0]
	occ2010=head.index('OCCP')
	perwt=head.index('PWGTP')
	uhrswork=head.index('WKHP')
	inctot=head.index('PINCP')
	incwage=head.index('WAGP')
	empstat=head.index('ESR')
	wkswork2=head.index('WKW')

	for row in data[1:]:
		try:
			data_2014.append([2014,0,0,0,0,0,int(row[perwt]),int(row[empstat]),int(row[empstat]),int(row[occ2010]),int(row[wkswork2]),int(row[uhrswork]),int(row[inctot]),int(row[incwage])])
		except:
			pass

	for row in data_2014:
		if row[7]==6:
			row[7]=3
			row[8]=3
		if row[7]==1 or row[7]==2 or row[7]==4 or row[7]==5:
			row[7]=1
			row[8]=1
		if row[7]==3:
			row[7]=2
			row[8]=2

	for row in data_2014:
		if row[10]==6:
			row[10]=1
		if row[10]==5:
			row[10]=2
		if row[10]==4:
			row[10]=3
		if row[10]==3:
			row[10]=4
		if row[10]==2:
			row[10]=5
		if row[10]==1:
			row[10]=6

	data_2014=[row for row in data_2014 if row[7]!=9920]

	return data_2014


def load_ipums_data(file='/Users/austinc/Desktop/usa_00007.csv'):
	# Load the IPUMs extract of years 2006-2013
	with open (file,'rU') as csvfile:
		reader=csv.reader(csvfile)
		data_2006_2013=[row for row in reader]

	return data_2006_2013


def merge_data(data_2014,data_2006_2013):
	# Merge the two data objects and recode occupations.
	newdata=[]
	for row in data_2006_2013[1:]:
		newrow=[int(entry) for entry in row]
		newdata.append(newrow)

	# occupation recoding
	for row in data_2014:
		if row[9]==40 or row[9]==50 or row[9]==60:
			row[9]=30
		if row[9]==135 or row[9]==136 or row[9]==137:
			row[9]=130
		if row[9]==565:
			row[9]=560
		if row[9]==630 or row[9]==640 or row[9]==650:
			row[9]=620
		if row[9]==725:
			row[9]=720
		if row[9]==740:
			row[9]=730
		if row[9]==1005 or row[9]==1006 or row[9]==1007 or row[9]==1030:
			row[9]=1000
		if row[9]==1105:
			row[9]=1100
		if row[9]==1840:
			row[9]=1830
		if row[9]==1860:
			row[9]=1840
		if row[9]==1965:
			row[9]=1960
		if row[9]==2015 or row[9]==2016 or row[9]==2025:
			row[9]=2020
		if row[9]==2105:
			row[9]=2100
		if row[9]==2145:
			row[9]=2140
		if row[9]==2160:
			row[9]=2150
		if row[9]==2710:
			row[9]=2700
		if row[9]==2830:
			row[9]=2810
		if row[9]==3255:
			row[9]=3130
		if row[9]==3245:
			row[9]=3240
		if row[9]==3535:
			row[9]=3530
		if row[9]==3645 or row[9]==3655:
			row[9]==3650
		if row[9]==3850:
			row[9]=3820
		if row[9]==3945 or row[9]==3955:
			row[9]=3950
		if row[9]==4020:
			row[9]=4000
		if row[9]==4465:
			row[9]=4460
		if row[9]==4710:
			row[9]=4700
		if row[9]==8256 or row[9]==8255:
			row[9]=8230
		if row[9]==9120 or row[9]==9110:
			row[9]=9100
		if row[9]==4410:
			row[9]=4430
		if row[9]==340 or row[9]==425:
			row[9]=430
		if row[9]==726:
			row[9]=730
		# if row[9]==5165:
		# 	row[9]=
		if row[9]==1106:
			row[9]=1100
		if row[9]==1107:
			row[9]=1100
		if row[9]==3256:
			row[9]=3260
		if row[9]==3258:
			row[9]=3260
		if row[9]==9415:
			row[9]=9420
		if row[9]==1340:
			row[9]=1530
		if row[9]==3420:
			row[9]=3540
		if row[9]==3648:
			row[9]=3650
		if row[9]==3645:
			row[9]=3650
		if row[9]==3646:
			row[9]=3650
		if row[9]==3647:
			row[9]=3650
		if row[9]==3649:
			row[9]=3650
		if row[9]==3655:
			row[9]=3650
		# if row[9]==7855:
		# 	row[9]=
		if row[9]==3840:
			row[9]=3950


	for row in newdata:
		if row[9]==8060:
			row[9]=8100
		if row[9]==7125:
			row[9]=7120
		if row[9]==6430:
			row[9]=6420
		if row[9]==1230:
			row[9]=1240

	# merge
	final=data_2014+newdata
	final=[row for row in final if type(row[0])==type(1)]
	return final


def format_acs_forinteractive(data):
	# a less stupid algorithm that uses pandas/vectorizes things
	# year[0],datanum[1],serial[2],hhwt[3],gq[4],pernum[5],perwt[6],empstat[7],empstatd[8],occ2010[9],wkswork2[10],uhrswork[11],inctot[12],incwage[13]
	# Little rearranging because I changed datasets and it screwed up all my indices
	data=[[row[0],row[1],row[2],row[3],0,0,row[4],row[5],row[6],row[9],row[10],row[11],row[13],row[7]] for row in data]
	dataf=pd.DataFrame(data,columns=['year','datanum','serial','hhwt','null1','null2','gq','pernum','perwt','occ2010','wkswork2','uhrswork','incwage','empstat'])
	dataf=dataf[dataf['incwage']!=999999]
	dataf['weight_wage']=dataf['incwage']*dataf['perwt']
	print 'dataframe created'

	data_employ=dataf[dataf['empstat']==1]
	data_wages=dataf[dataf['uhrswork']>=35]
	data_wages=data_wages[data_wages['wkswork2']>=4]

	print len(data_employ),len(data_wages)

	professions=list(set(dataf['occ2010']))
	finalrows=[]

	# construct a line for each profession that is:
	# [profession, 2006 wage, 2006 employment, 2006 hours worked, 2007 wage, 2007 employment, 2007 hours worked, ... ]
	for profession in professions:
		print 'profession',profession

		# assemble list of all rows in data that match profession
		temp_prof_w=data_wages[data_wages['occ2010']==profession]
		temp_prof_e=data_employ[data_employ['occ2010']==profession]
		
		# start a new row that begins with the profession id
		new_row=[profession]
		
		# loop through years and find appropriate profession/year combo
		years=range(2006,2015,1)
		for year in years:
			year_rows_w=temp_prof_w[temp_prof_w['year']==year]
			year_rows_e=temp_prof_e[temp_prof_e['year']==year]

			wagenum=year_rows_w['weight_wage'].sum()
			employcount_w=year_rows_w['perwt'].sum()
			hrsnum=0

			employcount_e=year_rows_e['perwt'].sum()

			print wagenum,employcount_w,hrsnum

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

	# First remove professions for which there are no observations in *any* single year except for 2014 - these must be
	# preserved because a change in profession coding could cause this, and all professions need to be included in
	# employment, even if they don't match up over the years.
	print 'Total rows: ',len(data)
	data2=[row for row in data if row[1]!=0 and row[2]!=0 and row[4]!=0 and row[5]!=0 and row[7]!=0 and row[8]!=0 and row[10]!=0 and row[11]!=0 and row[13]!=0 and row[14]!=0 and row[16]!=0 and row[17]!=0 and row[19]!=0 and row[20]!=0 and row[22]!=0 and row[23]!=0 and row[25]!=0 and row[26]!=0]
	data=[row for row in data if row[2]!=0]
	print 'Whole rows: ',len(data)

	# set up low/mid/high divisions based on 2006 wages.

	allemp2006=0
	for row in data:
		allemp2006=allemp2006+row[2]

	data.sort(key=lambda x:x[1])
	cuts=allemp2006/10
	cut_low=cuts*2
	cut_high=cuts*8

	temp=0
	for row in data:
		prev=temp
		temp=temp+row[2]
		if prev<cut_low and temp>cut_low:
			cut1=row[1]
			print 'CUT 1 ',row[1]
		if prev<cut_high and temp>cut_high:
			cut2=row[1]
			print 'CUT 2 ',row[1]

	# and now sort occupations into low/mid/high based on 2006 wage
	low_occs=[row for row in data if row[1]<=cut1]
	mid_occs=[row for row in data if row[1]>cut1 and row[1]<cut2]
	high_occs=[row for row in data if row[1]>=cut2]

	# quick sanity check - number of occupations in each group and the actual cuts
	print len(low_occs),len(mid_occs),len(high_occs)
	# print cut1,cut2

	# now create the first three rows of our eventual data structure by looping through the three
	# occupation lists and building average wage and total employment data for each. Output rows
	# for javascript are:
	# [sector, subsector, 2007 wage, wage growth, type flag, starting employment index (0),
	# emp index 2008, emp index 2009, emp index 2010...]
	for type in [['low',low_occs],['mid',mid_occs],['high',high_occs]]:
		totalemp2006, totalemp2007, totalemp2008, totalemp2009, totalemp2010, totalemp2011, totalemp2012, totalemp2013, totalemp2014 = 0, 0, 0, 0, 0, 0, 0, 0, 0
		average2007, average2014 = 0, 0		
		print type
		temp_row=[type[0],type[0]]

		for row in type[1]:
			average2007=average2007+row[4]*row[5]
			average2014=average2014+row[22]*row[23]

			totalemp2006=totalemp2006+row[2]
			totalemp2007=totalemp2007+row[5]
			totalemp2008=totalemp2008+row[8]
			totalemp2009=totalemp2009+row[11]
			totalemp2010=totalemp2010+row[14]
			totalemp2011=totalemp2011+row[17]
			totalemp2012=totalemp2012+row[20]
			totalemp2013=totalemp2013+row[23]
			totalemp2014=totalemp2014+row[26]

			print row[0],row[23]-row[26]

		average2007=average2007/totalemp2007
		average2014=average2014/totalemp2014

		temp_row.extend([average2007,(average2014-average2007)/average2007,-1,0])
		temp_row.extend([(totalemp2009-totalemp2008)/totalemp2008,(totalemp2010-totalemp2008)/totalemp2008,(totalemp2011-totalemp2008)/totalemp2008,(totalemp2012-totalemp2008)/totalemp2008,(totalemp2013-totalemp2008)/totalemp2008,(totalemp2014-totalemp2008)/totalemp2008])
		inter_rows.append(temp_row)

	# Adjust the last number here to screen out professions with small sample sizes
	# data=[row for row in data if row[2]>150000]

	# Next create rows for each specific occupation. This is pretty easy since data is already in a
	# occupation by occupation format.
	for code in occ_codes:
		print code
		code=[int(code[0]),code[1],code[2]]
		set=[row for row in data if row[0]==code[0]]
		# print set
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
			# make sure wage data exists and exclude occupations below some base size threshhold
			if set[0][25]!=0 and set[0][4]!=0 and set[0][2]>100000:
				new_row=[code[1],code[2],set[0][4],(set[0][25]-set[0][4])/set[0][4],1,0,(set[0][11]-set[0][8])/set[0][8],(set[0][14]-set[0][8])/set[0][8],(set[0][17]-set[0][8])/set[0][8],(set[0][20]-set[0][8])/set[0][8],(set[0][23]-set[0][8])/set[0][8],(set[0][26]-set[0][8])/set[0][8],flag]
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
		print occ
		occ_row=[int(row[0]) for row in occ_codes if row[1]==occ]
		temp_occ=[row for row in data if row[0] in occ_row]
		temp_row=[occ,'none']

		totalemp2006, totalemp2007, totalemp2008, totalemp2009, totalemp2010, totalemp2011, totalemp2012, totalemp2013, totalemp2014 = 0, 0, 0, 0, 0, 0, 0, 0, 0
		average2007, average2014 = 0, 0

		for row in temp_occ:
			average2007=average2007+row[4]*row[5]
			average2014=average2014+row[22]*row[23]

			totalemp2006=totalemp2006+row[2]
			totalemp2007=totalemp2007+row[5]
			totalemp2008=totalemp2008+row[8]
			totalemp2009=totalemp2009+row[11]
			totalemp2010=totalemp2010+row[14]
			totalemp2011=totalemp2011+row[17]
			totalemp2012=totalemp2012+row[20]
			totalemp2013=totalemp2013+row[23]
			totalemp2014=totalemp2014+row[26]

		average2007=average2007/totalemp2007
		average2014=average2014/totalemp2014

		print totalemp2006,totalemp2014

		temp_row.extend([average2007,(average2014-average2007)/average2007,0,0])
		temp_row.extend([(totalemp2009-totalemp2008)/totalemp2008,(totalemp2010-totalemp2008)/totalemp2008,(totalemp2011-totalemp2008)/totalemp2008,(totalemp2012-totalemp2008)/totalemp2008,(totalemp2013-totalemp2008)/totalemp2008,(totalemp2014-totalemp2008)/totalemp2008])
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

