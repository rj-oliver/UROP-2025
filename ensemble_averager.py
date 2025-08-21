import numpy as np
ensemble_year_avgs={}
ensemble_global_mean = {}

def calculate_ensemble_averages(r_max):
    """ 
    Averages annual local temperatures (year_avgs) and global mean temperatures (global_mean) for r_max number of simulation runs. 
    Saves averaged local temperatures and global mean temperatures in separate .npz files.
    """
    for model in ["119", "126", "245", "370", "585"]:
        for r_val in range(1,r_max+1):

    
            year_avgs = np.load('ssp' + model + '_r' + str(r_val) + 'i1p1f1_year_avgs.npz')
            global_mean = np.load('ssp' + model + '_r' + str(r_val) + 'i1p1f1_global_means.npz')
            for year in year_avgs.keys():
                if r_val == 1:
                    ensemble_year_avgs[year] = np.divide(year_avgs[year], r_max)
                    ensemble_global_mean[year] = np.divide(global_mean[year], r_max)
                else:
                    ensemble_year_avgs[year] += np.divide(year_avgs[year], r_max)
                    ensemble_global_mean[year] += np.divide(global_mean[year], r_max)

        np.savez(str(r_max)+'r_ssp' + model + '_ensemble_year_avgs.npz', **ensemble_year_avgs)
        np.savez(str(r_max)+'r_ssp' + model + '_ensemble_global_mean.npz', **ensemble_global_mean)
    
    for r_val in range(1,r_max+1):
        year_avgs = np.load('historical_model_r' + str(r_val) + 'i1p1f1_year_avgs.npz')
        global_mean = np.load('historical_model_r' + str(r_val) + 'i1p1f1_global_means.npz')
    

        for year in year_avgs.keys():

            if r == 1:
                ensemble_year_avgs[year] = np.divide(year_avgs[year], r_max)
                ensemble_global_mean[year] = np.divide(global_mean[year], r_max)
            elif year == "1989" and r == 8:
                # year 1989 of r=8 data displays as "nan", should be discarded
                print("discarding 'nan' data from year 1989 of r8i1p1f1 simulation")
                continue
            elif year == "1989" and r_max >= 8:
                # if at least 8 simulations are averaged, and year is 1989, only r_max-1 simulations should be averaged, as r=8 is discarded.
                ensemble_year_avgs[year] += np.divide(year_avgs[year], r_max-1)
                ensemble_global_mean[year] += np.divide(global_mean[year], r_max-1)
            else:
                ensemble_year_avgs[year] += np.divide(year_avgs[year], r_max)
                ensemble_global_mean[year] += np.divide(global_mean[year], r_max)

    np.savez(str(r_max)+'r_historical_model_ensemble_year_avgs.npz', **ensemble_year_avgs)
    np.savez(str(r_max)+'r_historical_model_ensemble_global_mean.npz', **ensemble_global_mean)

if __name__ == "__main__":    
    calculate_ensemble_averages(50)

