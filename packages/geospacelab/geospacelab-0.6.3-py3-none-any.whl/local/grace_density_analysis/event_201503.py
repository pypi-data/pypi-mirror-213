from local.grace_density_analysis.grace_base import *

def smooth_along_trajectory():
    def sector_N():
        sector_name = 'N'
        sector_cs = 'GEO'
        boundary_lat = 30.
        reverse_lat = True
        grace_db = grace_density_analysis_smooth(
            dt_fr, dt_to,
            sat_id=sat_id,
            sector_name=sector_name, sector_cs=sector_cs, boundary_lat=boundary_lat,
            reverse_lat=reverse_lat, zlims=zlims, figure_config=figure_config, 
            db_layout_config=db_layout_config)
        file_name = f"Event201503_GRACE-{sat_id}_smoothed_SECTOR-{sector_name}_CS-{sector_cs}_LAT-{boundary_lat}"
        grace_db.save_figure(file_name=file_name, file_dir=file_dir)
        return grace_db

    def sector_S():
        sector_name = 'S'
        sector_cs = 'GEO'
        boundary_lat = 30.
        reverse_lat = False
        grace_db = grace_density_analysis_smooth(
            dt_fr, dt_to,
            sat_id=sat_id,
            sector_name=sector_name, sector_cs=sector_cs, boundary_lat=boundary_lat,
            reverse_lat=reverse_lat, zlims=zlims, figure_config=figure_config, 
            db_layout_config=db_layout_config)
        file_name = f"Event201503_GRACE-{sat_id}_smoothed_SECTOR-{sector_name}_CS-{sector_cs}_LAT-{boundary_lat}"
        grace_db.save_figure(file_name=file_name, file_dir=file_dir)
        return grace_db

    def sector_ASC():
        sector_name = 'ASC'
        sector_cs = 'GEO'
        boundary_lat = 60.
        reverse_lat = False
        grace_db = grace_density_analysis_smooth(
            dt_fr, dt_to,
            sat_id=sat_id,
            sector_name=sector_name, sector_cs=sector_cs, boundary_lat=boundary_lat,
            reverse_lat=reverse_lat, zlims=zlims, figure_config=figure_config, 
            db_layout_config=db_layout_config)
        file_name = f"Event201503_GRACE-{sat_id}_smoothed_SECTOR-{sector_name}_CS-{sector_cs}_LAT-{boundary_lat}"
        grace_db.save_figure(file_name=file_name, file_dir=file_dir)
        return grace_db

    def sector_DSC():
        sector_name = 'DSC'
        sector_cs = 'GEO'
        boundary_lat = 60.
        reverse_lat = True
        grace_db = grace_density_analysis_smooth(
            dt_fr, dt_to,
            sat_id=sat_id,
            sector_name=sector_name, sector_cs=sector_cs, boundary_lat=boundary_lat,
            reverse_lat=reverse_lat, zlims=zlims, figure_config=figure_config, 
            db_layout_config=db_layout_config)
        file_name = f"Event201503_GRACE-{sat_id}_smoothed_SECTOR-{sector_name}_CS-{sector_cs}_LAT-{boundary_lat}"
        grace_db.save_figure(file_name=file_name, file_dir=file_dir)
        return grace_db

    sat_id = 'A'
    
    zlims = [
        [10e-13, 9e-12],
        [10e-13, 9e-12],
        [-3e-13, 3e-13],
        [-20, 20] 
    ]

    grace_db = sector_N()
    sector_S()
    sector_ASC()
    sector_DSC()
    # grace_db.quicklook_single_measurements(sat_id=sat_id, figure_config=figure_config, db_layout_config=db_layout_config)
    
    # grace_db.quicklook_dual_measurements(figure_config=figure_config, db_layout_config=db_layout_config)
    

def dual_AB_shift():
    def sector_N():
        sector_name = 'N'
        sector_cs = 'GEO'
        boundary_lat = 30.
        reverse_lat = True
        grace_db = grace_density_analysis_dual_diff_shift(
            dt_fr, dt_to,
            time_shift=time_shift, t_res=time_res, sector_name=sector_name, sector_cs=sector_cs, boundary_lat=boundary_lat,
            reverse_lat=reverse_lat, zlims=zlims, figure_config=figure_config, 
            db_layout_config=db_layout_config)
        file_name = f"Event201503_GRACE-AB_SHIFT-{str(time_shift)}_SECTOR-{sector_name}_CS-{sector_cs}_LAT-{boundary_lat}"
        grace_db.save_figure(file_name=file_name, file_dir=file_dir)
        return grace_db

    def sector_S():
        sector_name = 'S'
        sector_cs = 'GEO'
        boundary_lat = 30.
        reverse_lat = False
        grace_db = grace_density_analysis_dual_diff_shift(
            dt_fr, dt_to,
            time_shift=time_shift, t_res=time_res, sector_name=sector_name, sector_cs=sector_cs, boundary_lat=boundary_lat,
            reverse_lat=reverse_lat, zlims=zlims, figure_config=figure_config, 
            db_layout_config=db_layout_config)
        file_name = f"Event201503_GRACE-AB_SHIFT-{str(time_shift)}_SECTOR-{sector_name}_CS-{sector_cs}_LAT-{boundary_lat}"
        grace_db.save_figure(file_name=file_name, file_dir=file_dir)
        return grace_db

    def sector_ASC():
        sector_name = 'ASC'
        sector_cs = 'GEO'
        boundary_lat = 60.
        reverse_lat = False
        grace_db = grace_density_analysis_dual_diff_shift(
            dt_fr, dt_to,
            time_shift=time_shift, t_res=time_res, sector_name=sector_name, sector_cs=sector_cs, boundary_lat=boundary_lat,
            reverse_lat=reverse_lat, zlims=zlims, figure_config=figure_config,
            db_layout_config=db_layout_config
            )
        file_name = f"Event201503_GRACE-AB_SHIFT-{str(time_shift)}_SECTOR-{sector_name}_CS-{sector_cs}_LAT-{boundary_lat}"
        grace_db.save_figure(file_name=file_name, file_dir=file_dir)
        return grace_db

    def sector_DSC():
        sector_name = 'DSC'
        sector_cs = 'GEO'
        boundary_lat = 60.
        reverse_lat = True
        grace_db = grace_density_analysis_dual_diff_shift(
            dt_fr, dt_to,
            time_shift=time_shift, t_res=time_res, sector_name=sector_name, sector_cs=sector_cs, boundary_lat=boundary_lat,
            reverse_lat=reverse_lat, zlims=zlims, figure_config=figure_config,
            db_layout_config=db_layout_config)
        file_name = f"Event201503_GRACE-AB_SHIFT-{str(time_shift)}_SECTOR-{sector_name}_CS-{sector_cs}_LAT-{boundary_lat}"
        grace_db.save_figure(file_name=file_name, file_dir=file_dir)
        return grace_db

    time_res = 1.
    time_shift = 34.
    zlims = [
        [10e-13, 10e-12],
        [-13e-14, 13e-14],
        [-3e-15, 3e-15]
    ]
    grace_db = sector_N()
    sector_S()
    sector_ASC()
    sector_DSC()
    

def dual_AB_diff():
    def sector_N():
        sector_name = 'N'
        sector_cs = 'GEO'
        boundary_lat = 30.
        reverse_lat = True
        grace_db = grace_density_analysis_dual_diff(
            dt_fr, dt_to,
            sector_name=sector_name, sector_cs=sector_cs, boundary_lat=boundary_lat,
            reverse_lat=reverse_lat, zlims=zlims, figure_config=figure_config, 
            db_layout_config=db_layout_config)
        file_name = f"Event201503_GRACE-AB_DIFF_SECTOR-{sector_name}_CS-{sector_cs}_LAT-{boundary_lat}"
        grace_db.save_figure(file_name=file_name, file_dir=file_dir)
        return grace_db

    def sector_S():
        sector_name = 'S'
        sector_cs = 'GEO'
        boundary_lat = 30.
        reverse_lat = False
        grace_db = grace_density_analysis_dual_diff(
            dt_fr, dt_to,
            sector_name=sector_name, sector_cs=sector_cs, boundary_lat=boundary_lat,
            reverse_lat=reverse_lat, zlims=zlims, figure_config=figure_config, 
            db_layout_config=db_layout_config)
        file_name = f"Event201503_GRACE-AB_DIFF_SECTOR-{sector_name}_CS-{sector_cs}_LAT-{boundary_lat}"
        grace_db.save_figure(file_name=file_name, file_dir=file_dir)
        return grace_db

    def sector_ASC():
        sector_name = 'ASC'
        sector_cs = 'GEO'
        boundary_lat = 60.
        reverse_lat = False
        grace_db = grace_density_analysis_dual_diff(
            dt_fr, dt_to,
            sector_name=sector_name, sector_cs=sector_cs, boundary_lat=boundary_lat,
            reverse_lat=reverse_lat, zlims=zlims, figure_config=figure_config,
            db_layout_config=db_layout_config)
        file_name = f"Event201503_GRACE-AB_DIFF_SECTOR-{sector_name}_CS-{sector_cs}_LAT-{boundary_lat}"
        grace_db.save_figure(file_name=file_name, file_dir=file_dir)
        return grace_db

    def sector_DSC():
        sector_name = 'DSC'
        sector_cs = 'GEO'
        boundary_lat = 60.
        reverse_lat = True
        grace_db = grace_density_analysis_dual_diff(
            dt_fr, dt_to,
            sector_name=sector_name, sector_cs=sector_cs, boundary_lat=boundary_lat,
            reverse_lat=reverse_lat, zlims=zlims, figure_config=figure_config, db_layout_config=db_layout_config)
        file_name = f"Event201503_GRACE-AB_DIFF_SECTOR-{sector_name}_CS-{sector_cs}_LAT-{boundary_lat}"
        grace_db.save_figure(file_name=file_name, file_dir=file_dir)
        return grace_db

    zlims = [
        [10e-13, 10e-12],
        [-13e-14, 13e-14],
        [-10, 10]
    ]
    file_dir = "/home/lei/01-Work/01-Project/UTA20-IT_Storm/GRACE_Data_Analysis/201503_StPatrickStorm/"
    grace_db = sector_N()
    sector_S()
    sector_ASC()
    sector_DSC()
    # sat_id = 'A'
    # grace_db.quicklook_single_measurements(sat_id=sat_id)
    # grace_db.quicklook_dual_measurements()


def dual_diff_shift_time_estimate():
    def analysis():
        dt_fr_1 = dt_fr - datetime.timedelta(minutes=30)
        dt_to_1 = dt_to + datetime.timedelta(minutes=30)
        grace_db = GraceAnalysisDNSACC(dt_fr_1, dt_to_1)
        ds_A = grace_db.ds_A.interp_evenly(time_res=t_res)
        ds_B = grace_db.ds_B.interp_evenly(time_res=t_res)
        return ds_A, ds_B

    t_res = 1.
    ds_A, ds_B = analysis()

    plt.figure()
    plt.plot(ds_A['SC_DATETIME'].flatten(), ds_A['SC_GEO_LAT'].flatten())
    plt.plot(ds_B['SC_DATETIME'].flatten(), ds_B['SC_GEO_LAT'].flatten())
    plt.ylabel("SC_LAT")

    plt.figure()
    plt.plot(ds_A['SC_DATETIME'].flatten(), ds_A['SC_GEO_LON'].flatten())
    plt.plot(ds_B['SC_DATETIME'].flatten(), ds_B['SC_GEO_LON'].flatten())
    plt.ylabel("SC_LON")

    plt.figure()
    avg_diff = []
    for i in range(80):
        N = int(np.fix(i/t_res))
        diff_lat = ds_A['SC_GEO_LAT'].flatten() - np.roll(ds_B['SC_GEO_LAT'].flatten(), N)
        avg_diff.append(np.nanmean(np.abs(diff_lat)))
    plt.plot(range(80), avg_diff)
    plt.xlim([0.5, 80.5])
    plt.ylim([0, 3])
    plt.xlabel("Time shift (s)")
    plt.ylabel('Averaged latitude difference')

    plt.figure()
    avg_diff = []
    for i in range(80):
        N = int(np.fix(i/t_res))
        diff_lat = ds_A['SC_GEO_LON'].flatten() - np.roll(ds_B['SC_GEO_LON'].flatten(), N)
        avg_diff.append(np.nanmean(np.abs(diff_lat)))
    plt.plot(range(80), avg_diff)
    plt.xlim([30, 40])
    plt.ylim([0, 5])
    plt.xlabel("Time shift (s)")
    plt.ylabel('Averaged longitude difference')
    plt.savefig(file_dir + 'time_shift_corr_zoom.png')
    

file_dir = "/home/lei/01-Work/01-Project/UTA20-IT_Storm/GRACE_Data_Analysis/201503_StPatrickStorm/"

dt_fr = datetime.datetime(2015, 3, 16, 20)
dt_to = datetime.datetime(2015, 3, 18, 2)

dt_fr_1 = datetime.datetime(2015, 3, 16, 0)
dt_to_1 = datetime.datetime(2015, 3, 26, 0)

figure_config = {'figsize': (15, 8)}
db_layout_config = {'bottom': 0.08, 'left': 0.12, 'right': 0.82}

if __name__ == '__main__':
    # overview_sigle_satellite(
    #    dt_fr, dt_to, save_fig=True, file_dir=file_dir, file_name='overview_201503', sc_alt_lim=[360, 450],
    #    figure_config=figure_config, db_layout_config=db_layout_config)
    
    # overview_dual_satellites(
    #    dt_fr, dt_to, save_fig=True, file_dir=file_dir, file_name='overview_201503_dual', D_lim=[240, 280],
    #    figure_config=figure_config, db_layout_config=db_layout_config)
    smooth_along_trajectory()
    
    # dual_AB_diff()
    # dual_diff_shift_time_estimate()
    # dual_AB_shift()