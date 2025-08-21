import netCDF4
import numpy as np
import math 


days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

days_leap = days[:]
days_leap[1] += 1

for ind, day in enumerate(days):
    days[ind] = day/365.0

for ind, day in enumerate(days_leap):
    days_leap[ind] = day/366.0
    
def average_simulation(r_val, simulation):
    """ 
    Calculates local temperature annual averages (year_avgs) and global annual mean temperatures (global_means) for a given MPI model
    (specified by simulation name, 'simulation', and simulation run number, 'r_val')
    """

    year_avgs = {}
    global_means = {}

    if simulation in ["119", "126", "245", "370", "585"]:
        year_range = (2015, 2101)
    
    elif simulation == "h":
        year_range = (1850, 2015)
    
    else:
        print("inavlid simulation input")
        return None
    
    for year in range(year_range[0], year_range[1]):
        if simulation in ["119", "126", "245", "370", "585"]:
        
            fnd = '/net/fs06/d3/lutjens/bc3/data/raw/CMIP6/MPI-ESM1-2-LR/r' + r_val + 'i1p1f1/ssp' +simulation+ '/tas/250_km/mon/' + str(year) + '/CMIP6_MPI-ESM1-2-LR_r' + r_val + 'i1p1f1_ssp' +simulation+ '_tas_250_km_mon_gn_' + str(year) + '.nc'
        
        else:
            fnd = '/net/fs06/d3/lutjens/bc3/data/raw/CMIP6/MPI-ESM1-2-LR/r' + r_val + 'i1p1f1/historical/tas/250_km/mon/' + str(year) + '/CMIP6_MPI-ESM1-2-LR_r' + r_val + 'i1p1f1_historical_tas_250_km_mon_gn_' + str(year) + '.nc'

        year_sum = np.zeros((96, 192))
        nc=netCDF4.Dataset(fnd)

        #latitudes are rows; longitudes are cols
    
        # leap year
        if year%4 == 0 and year not in (1900, 2101):
            for month in range(0,12): 
                for row in range(year_sum.shape[0]):
                    for col in range(year_sum.shape[1]): 
                        year_sum[row, col] += nc["tas"][month][row, col] * days_leap[month]
                print(year, month)
        else:
            for month in range(0,12): 
                for row in range(year_sum.shape[0]):
                    for col in range(year_sum.shape[1]): 
                        year_sum[row, col] += nc["tas"][month][row, col] * days[month]
                print(year, month)
        
        year_avgs[str(year)] = year_sum

        for year, loc_array in year_avgs.items():
            global_mean = 0
            angle = -math.pi/2 # begins at south pole
            # mean over longitudes (columns) for each latitude (row)
            lat_means = np.mean(loc_array, axis=1)
            for lat_mean in lat_means:
                # integral of cos from lower to upper angle bounds
                global_mean += lat_mean * (math.sin(angle + math.pi/96) - math.sin(angle)) 
                angle += math.pi/96
            global_means[year] = global_mean/2
        

    if simulation in ["119", "126", "245", "370", "585"]:
        np.savez('ssp'+simulation+'_r'+ str(r_val) + 'i1p1f1_year_avgs.npz', **year_avgs)
        np.savez('ssp'+simulation+'_r'+ str(r_val) + 'i1p1f1_global_means.npz', **global_means) 
    else:
        np.savez('historical_model_r' + str(r_val) + 'i1p1f1_year_avgs.npz', **year_avgs)
        np.savez('historical_model_r' + str(r_val) + 'i1p1f1_global_means.npz', **global_means)
        
        
if __name__ == "__main__":
    r_val = input("r_val: ")
    simulation = input("Simulation name (119, 126, 245, 370, 585, or 'h' for historical): ")
    average_simulation(r_val, simulation)
