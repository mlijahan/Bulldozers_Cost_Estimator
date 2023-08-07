
""" Calculation of heavy equipment Cost for a particular activity"""

import numpy as np
import math


activity = input("Insert the title of the activity:\n\n")
machine_type = input("Insert the type of machine:\n\n")
manufacturer = input("Insert the manufacturer name of machine:\n\n")
model_name = input("Insert the model name of machine:\n\n")
delivered_price_dollars = float(input("Please enter delivered price of machine in $ "
                                      "(including taxes, freight, and installation)):\n"))
sales_tax_percent = float(input("Please enter sale's tax percent of machine in %:\n"))
interest_percent = float(input("Please enter interest percent of machine in %:\n"))   # Interest on the investment
insurance_percent= float(input("Please enter insurance percent of machine in %:\n"))
tax_percent= float(input("Please enter annually tax percent of machine in %:\n"))
work_hours= int(input("Please enter the number of hours that machine has worked:\n"))
capacity_crankcase_gallon= float(input("Please enter crankcase capacity of machine in gallon:\n"))
hours_lubricating_changes = float(input("Please enter hours between lubricating changes of machine:\n"))
fuel_price = float(input("Please insert price of per gallon of fuel $:\n"))
lubricant_price = float(input("Please insert cost of lubricating ($):\n\n"))
operator_wage = float(input("Please enter operator wage per hour($):\n\n"))
rental_hourly_cost = float(input("Please enter rental cost per hour($):\n\n"))
tire_price = float(input("Please insert total price of tires($):\n"))
temperature = int(input("Insert the mean of the temperature in duration of doing activity (C) :\n\n"))
altitude = int(input("Insert the mean of the elevation of the job site (m) :\n\n"))
power = int(input("Insert the power of the bulldozer (hp):\n\n"))
load_factor = input("Please insert loader application:\n(a) 'low'\n(b) 'medium'\n(c) 'high'\n\n ")

# ******************************************** OWNERSHIP COSTS *********************************************************

def depreciation_value(sales_tax_percent):
    price_sale_tax = (delivered_price_dollars * sales_tax_percent) / 100
    price_after_sale_tax = delivered_price_dollars + price_sale_tax
    net_value_depreciation = price_after_sale_tax - price_sale_tax
    return net_value_depreciation

def machine_name(manufacturer, model_name):
    """ Define the fullname of machine as:
    Mnufacturer's name + Tractor's model name + type of blade of bulldozer (S( Straight blade), U( Universal blade), SU(Semi U),...)"""
    manufacturer_case = manufacturer.upper()
    model_case = model_name.upper()
    machine_type_case = machine_type.upper()
    machinename = f'{machine_type_case} {manufacturer_case} {model_case}'
    return machinename


def depreciation(expected_use = 20000):
    """ Depreciation represents the decline in market value of a piece of equipment due to age, wear,
        deterioration, and obsolescence."""
    depreciations = depreciation_value(sales_tax_percent) / expected_use
    return depreciations


def useful_life(expected_use = 20000, expected_use_annually = 1590):
    usefull_lifes = expected_use / expected_use_annually
    return np.round(usefull_lifes)


def interest_cost(expected_use_annually = 1590):
    interestcost = ((depreciation_value(sales_tax_percent) * (interest_percent / 100)) *
                    ((useful_life() + 1) / (2 * useful_life())))\
                      / expected_use_annually
    return np.round(interestcost, 2)


def insurance_cost(expected_use_annually =1590):
    insurancecost = ((depreciation_value(sales_tax_percent) * (insurance_percent / 100)) *
                     ((useful_life() + 1) / (2 * useful_life())))\
                           / expected_use_annually
    return np.round(insurancecost, 2)


def taxes_cost(expected_use_annually =1590):
    taxcost = ((depreciation_value(sales_tax_percent) * (tax_percent / 100)) *
               ((useful_life() + 1) / (2 * useful_life())))\
                       / expected_use_annually
    return np.round(taxcost, 2)


def total_hourly_ownership_cost():
    total_ownership_cost = depreciation() + interest_cost() + insurance_cost() + taxes_cost()
    print(np.round(total_ownership_cost))
    return np.round(total_ownership_cost)

# ******************************************** OPERATIONAL COSTS *********************************************************

def year_of_operation():
    year_operation = work_hours /1590
    return round(year_operation)


def yeardigits():
    yeardigit = sum(range(year_of_operation()+1))
    print(yeardigit)
    return(yeardigit)


def hourly_repair_cost(Lifetime_repair_cost_factor=0.6, expected_use_annually = 1590):
    Lifetime_repair_cost = Lifetime_repair_cost_factor * depreciation_value(sales_tax_percent)
    Hourlyrepair_cost = (year_of_operation() / yeardigits()) * (Lifetime_repair_cost / expected_use_annually)
    return np.round(Hourlyrepair_cost, 2)


def tire_repair_replacement_costs():
    expected_tirelife = []
    site_conditions = input("Please insert site condition:\n(a) Zone A: Almost all tires actually wear through the tread due to abrasion.\
                       \n(b) Zone B: Some tires wear out normally while others fail prematurely due to rock cuts, impacts and non-repairable punctures.\
                       \n(c) Zone C: Few, if any, tires wear through the tread because of non-repairable damages, usually from rock cuts, impacts or continuous overloading\n\n ")

    if site_conditions == 'a':
        expected_tirelife.append(4500)

    elif site_conditions == 'b':
        expected_tirelife.append(2100)

    else:
        expected_tirelife.append(750)

    tire_repair_replacement_costss = tire_price / np.array(expected_tirelife)
    return np.round(tire_repair_replacement_costss, 2)


def manual_fuel_consumption_factor():
    work_condition = input("Please insert work condition:\n(a) 'Favorable'\n(b) 'Average'\n(c) 'Unfavorable'\n\n ")
    max_fuel_consumption_factor = []

    if work_condition == 'a':
        max_fuel_consumption_factor.append(0.028)

    elif work_condition == 'b':
        max_fuel_consumption_factor.append(0.038)

    else:
        max_fuel_consumption_factor.append(0.052)
    return np.array(max_fuel_consumption_factor)


def manual_load_factor():
    max_load_factor = []

    if load_factor == 'a':
        max_load_factor.append(0.5)

    elif load_factor == 'b':
        max_load_factor.append(0.65)

    else:
        max_load_factor.append(0.8)
    return np.array(max_load_factor)


def height_air_pressure(altitude):
    """ Define the air pressure (CmhG) of job site in dependence of the height (m) of site above the see """
    height_above_see_m = [0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000]     # possible heights of jobsites
    airpress_cmhg = [76, 73.3, 70.66, 68.07, 65.58, 63.17, 60.83, 58.6, 56.41, 54.25, 52.2]
    y_new = np.interp(altitude, height_above_see_m, airpress_cmhg)
    return y_new


def site_temprature_effect(temperature):
    """ Define the Temperature of job site in K """
    temp = (273 + temperature) / 288.6    # convert temperature in Celsius to Kelvin
    Temperature = math.sqrt(temp)
    return Temperature


def real_power():
    """ Real Horsepower Rating in job site condition (Elevation&Temperature of job site make changes in Rated power SAE"""
    power_real = power / ((76/height_air_pressure(altitude)) * site_temprature_effect(temperature))
    real_power = np.round(power_real, 2)
    return real_power


def manual_fuel_consumption_cost():
    fuel_consumption_cost = manual_fuel_consumption_factor() * manual_load_factor() * fuel_price * real_power()
    return(fuel_consumption_cost)


def Lubricating_oil_cost():
    quantity_of_oil_required = real_power()* manual_load_factor()
    Lubricating_Cost = (((0.006 * quantity_of_oil_required) / 7.4) +
                             (capacity_crankcase_gallon / hours_lubricating_changes))\
                            * lubricant_price

    return np.round(Lubricating_Cost, 2)


def operating_cost_per_hour():
    operating_costs_per_hour = hourly_repair_cost() + tire_repair_replacement_costs() +\
                               manual_fuel_consumption_cost() + Lubricating_oil_cost()
    return np.round(operating_costs_per_hour, 2)


def total_cost_per_hour():
    total_hourly_cost = total_hourly_ownership_cost() + operating_cost_per_hour() + operator_wage + rental_hourly_cost
    print(print(f'"Total cost of {machine_name(manufacturer, model_name)}" during doing '
                f'"{activity}" is "{np.round(total_hourly_cost[0], 2)}" $'))
    return (np.round(total_hourly_cost, 2))


def main():

    return total_cost_per_hour()

if __name__ == "__main__":
    main()





