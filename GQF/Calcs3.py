from datetime import timedelta as timedelta
try:
    import pandas as pd
except:
    pass


def QF(areaCodes, timeStepEnd, timeStepDuration, annualEnergyUse, diurnalProfiles, dailyEnergy, pop, trans, diurnalTrans,
       workingProfiles, dailyFactor, prop, hoc):
    '''
    Calculate all energy fluxes for the specified time step and spatial area ID
    :param areaCodes: The feature ID of the spatial area (as appears in energyUse.getEnergyTable())
    :param timeStepEnd: datetime() featuring the end of the time step
    :param timeStepDuration: int() number of seconds covered by the model time step
    :param annualEnergyUse: EnergyUseData object populated with data
    :param diurnalProfiles: EnergyProfile object populated with data
    :param pop: PopulationData object
    :param trans: Transport object
    :param diurnalTrans: TransportProfiles object
    :param area: Areas of the output features
    :param workingProfiles: HumanActivityProfiles object
    :param dailyFactor
    :param prop: Proportions of fluxes to include (dict of {sector or road fuel: {fuel or number}})
    :param hoc: Heat of combustion [J/km] {petrol: float, diesel: float}
    :return: Building energy QF components for this time step
    '''
    dailyFactor = dailyFactor.getFact(timeStepEnd - timedelta(
        seconds=timeStepDuration))  # Get daily factors at start of time bin to ensure correct day
    de = annualEnergyUse.getDomesticElecValue(areaCodes, timeStepEnd)
    ie = annualEnergyUse.getIndustrialElecValue(areaCodes, timeStepEnd)
    dg = annualEnergyUse.getDomesticGasValue(areaCodes, timeStepEnd)
    ig = (annualEnergyUse.getIndustrialGasValue(areaCodes, timeStepEnd))

    ElecRho = de / (ie + 0.00001)
    ElecSum = de + ie
    NewElDom = dailyFactor * ElecRho * ElecSum / (1.0 + dailyFactor * ElecRho)
    NewElInd = ElecSum / (1.0 + dailyFactor * ElecRho)

    GasRho = dg / (ig + 0.00001)
    GasSum = dg + ig

    NewGasDom = dailyFactor * GasRho * GasSum / (1.0 + dailyFactor * GasRho)

    NewGasInd = GasSum / (1.0 + dailyFactor * GasRho)

    columns = ['ElDmUnr',
               'ElDmE7',
               'ElId',
               'GasDm',
               'GasId',
               'OthrId',
               'BldTotDm',
               'BldTotId',
               'BldTot',
               'Mcyc',
               'Taxi',
               'Car',
               'Bus',
               'LGV',
               'Rigd',
               'Art',
               'TransTot',
               'Metab',
               'AllTot']
    # at later point do something with mods to find total hours in time period
    WattHour = pd.DataFrame(columns=columns, index=areaCodes)

    # TODO: fix the pandas value assignment issues below:
    # incorrect way of setting values
    WattHour.loc[areaCodes,columns[0]] = prop['domestic']['elec'] * \
        diurnalProfiles.getDomElec(timeStepEnd, timeStepDuration)[0] * \
        dailyEnergy.getElec(timeStepEnd, timeStepDuration)[0] * \
        NewElDom  # El dom unrestr
    WattHour.loc[areaCodes,columns[1]] = prop['domestic']['eco7'] * \
        diurnalProfiles.getEconomy7(timeStepEnd, timeStepDuration)[0] * \
        dailyEnergy.getElec(timeStepEnd, timeStepDuration)[0] * \
        annualEnergyUse.getEconomy7ElecValue(areaCodes, timeStepEnd)

    WattHour.loc[areaCodes,columns[2]] = prop['industrial']['elec'] * \
        diurnalProfiles.getIndElec(timeStepEnd, timeStepDuration)[0] * \
        dailyEnergy.getElec(timeStepEnd, timeStepDuration)[0] * \
        NewElInd  # El industrial

    WattHour.loc[areaCodes,columns[3]] = prop['domestic']['gas'] * \
        diurnalProfiles.getDomGas(timeStepEnd, timeStepDuration)[0] * \
        dailyEnergy.getGas(timeStepEnd, timeStepDuration)[0] * \
        NewGasDom  # Gas domestic

    WattHour.loc[areaCodes,columns[4]] = prop['industrial']['gas'] * \
        diurnalProfiles.getIndGas(timeStepEnd, timeStepDuration)[0] * \
        dailyEnergy.getGas(timeStepEnd, timeStepDuration)[0] * \
        NewGasInd  # Gas industrial

    WattHour.loc[areaCodes,columns[5]] = prop['industrial']['crude_oil'] * \
        diurnalProfiles.getIndGas(timeStepEnd, timeStepDuration)[0] * \
        dailyEnergy.getGas(timeStepEnd, timeStepDuration)[0] * \
        annualEnergyUse.getIndustrialOtherValue(
            areaCodes, timeStepEnd)  # Assume same behaviour as gas

    WattHour.loc[areaCodes,columns[6]] = WattHour.loc[areaCodes,columns[0]] + \
        WattHour.loc[areaCodes,columns[1]] + \
        WattHour.loc[areaCodes,columns[3]]  # total buildings domestic

    WattHour.loc[areaCodes,columns[7]] = WattHour.loc[areaCodes,columns[2]] + \
        WattHour.loc[areaCodes,columns[4]] + \
        WattHour.loc[areaCodes,columns[5]]  # total buildings industrial

    WattHour.loc[areaCodes,columns[8]] = WattHour.loc[areaCodes,columns[6]] + \
        WattHour.loc[areaCodes,columns[7]]  # total buildings

    # TRANSPORT: Take fuel consumption density [kg/m2] for petrol and diesel, convert to heat
    # Heat of combustion shorthand
    dslHoc = hoc['diesel']['gross']
    petHoc = hoc['petrol']['gross']

    # Scaling factor shorthand(determines whether latent and/or sensible heat should be included)
    # Factor of 86400 to convert from J/m2/day to J/m2/s (W/m2)
    dslSc = prop['diesel']
    petSc = prop['petrol']
    # print('Fuel cons density (kg/m2)', trans.getCar(areaCodes, 'petrol', timeStepEnd))
    # print('HoC (J km -1)', petHoc)
    # print('J m-2 day-1', petHoc * trans.getCar(areaCodes, 'petrol', timeStepEnd))
    # print('J m-2 s-1', (petHoc * trans.getCar(areaCodes, 'petrol', timeStepEnd) /86400))
    # issue with mean or sum division of transport profile could be coming out here
    # comes as HoC * profile time * fuel proportion
    # cardiur = diurnalTrans.getCar(timeStepEnd, timeStepDuration)[0]
    # print('printing getCar Diurnal', type(cardiur))
    # print('getCar Diurnal:', cardiur)
    # print('HoC:', petHoc, dslHoc)
    # print(areaCodes)
    # print('FC:', trans.getCar(areaCodes, 'petrol', timeStepEnd))
    # print('Sc:', petSc, dslSc)
    WattHour.loc[areaCodes,columns[9]] = (petHoc * trans.getMotorcycle(areaCodes, 'petrol', timeStepEnd) * petSc +
                                       dslHoc * trans.getMotorcycle(areaCodes, 'diesel', timeStepEnd) * dslSc) * \
        diurnalTrans.getMotorcycle(timeStepEnd, timeStepDuration)[0]/86400.0  # motorcycles

    WattHour.loc[areaCodes,columns[10]] = (petHoc * trans.getTaxi(areaCodes, 'petrol', timeStepEnd) * petSc +
                                        dslHoc * trans.getTaxi(areaCodes, 'diesel', timeStepEnd) * dslSc) * \
        diurnalTrans.getTaxi(timeStepEnd, timeStepDuration)[0]/86400.0  # Taxis

    WattHour.loc[areaCodes,columns[11]] = (petHoc * trans.getCar(areaCodes, 'petrol', timeStepEnd) * petSc +
                                        dslHoc * trans.getCar(areaCodes, 'diesel', timeStepEnd) * dslSc) * \
        diurnalTrans.getCar(timeStepEnd, timeStepDuration)[0]/86400.0  # Cars

    WattHour.loc[areaCodes,columns[12]] = (petHoc * trans.getBus(areaCodes, 'petrol', timeStepEnd) * petSc +
                                        dslHoc * trans.getBus(areaCodes, 'diesel', timeStepEnd) * dslSc) * \
        diurnalTrans.getBus(timeStepEnd, timeStepDuration)[0]/86400.0  # Bus

    WattHour.loc[areaCodes,columns[13]] = (petHoc * trans.getLGV(areaCodes, 'petrol', timeStepEnd) * petSc +
                                        dslHoc * trans.getLGV(areaCodes, 'diesel', timeStepEnd) * dslSc) * \
        diurnalTrans.getLGV(timeStepEnd, timeStepDuration)[0]/86400.0  # LGVs

    WattHour.loc[areaCodes,columns[14]] = (petHoc * trans.getRigid(areaCodes, 'petrol', timeStepEnd) * petSc +
                                        dslHoc * trans.getRigid(areaCodes, 'diesel', timeStepEnd) * dslSc) * \
        diurnalTrans.getRigid(timeStepEnd, timeStepDuration)[0]/86400.0  # Rigid HGVs

    WattHour.loc[areaCodes,columns[15]] = (petHoc * trans.getArtic(areaCodes, 'petrol', timeStepEnd) * petSc +
                                        dslHoc * trans.getArtic(areaCodes, 'diesel', timeStepEnd) * dslSc) * \
        diurnalTrans.getArtic(timeStepEnd, timeStepDuration)[0]/86400.0  # Articulated HGVs

    WattHour[columns[16]] = WattHour[columns[9:16]].sum(
        axis=1)  # Calculate grand total across transport

    # METABOLISM
    # Home:Work balance of people.  1=Workday population, 0= Residential Population
    activeFraction = workingProfiles.getFraction(
        timeStepEnd, timeStepDuration)[0]
    a = prop['metab'] * workingProfiles.getWattPerson(timeStepEnd, timeStepDuration)[0] *\
        ((1-activeFraction)*pop.getResPopValue(areaCodes, timeStepEnd) +
         activeFraction*pop.getWorkPopValue(areaCodes, timeStepEnd))

    WattHour[columns[17]] = a
    WattHour.loc[areaCodes,columns[18]] = WattHour.loc[areaCodes,columns[8]] + \
        WattHour.loc[areaCodes,columns[16]] + WattHour.loc[areaCodes,columns[17]]
    return WattHour.astype('float16')
