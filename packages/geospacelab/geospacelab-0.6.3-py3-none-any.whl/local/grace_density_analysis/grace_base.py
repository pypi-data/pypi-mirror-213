import datetime
import matplotlib.pyplot as plt
import numpy as np
import pathlib

from geospacelab import preferences as pref

# pref.user_config['visualization']['mpl']['style'] = 'dark'  # or 'light'

import geospacelab.visualization.mpl.dashboards as dashboards
import geospacelab.observatory.earth.geodesy as gd
from geospacelab.observatory.orbit.utilities import LEOToolbox

class GraceAnalysisDNSACC(dashboards.TSDashboard):
    
    def __init__(self, dt_fr=None, dt_to=None, sat_id='AB', add_APEX=True, add_AACGM=True,
                 figure='new', figure_config={'figsize': (12, 8)}, **kwargs):
        if dt_fr is None:
            dt_fr = datetime.datetime(2016, 2, 2, 0)
        if dt_to is None:
            dt_to = datetime.datetime(2016, 2, 4, 0)

        super().__init__(dt_fr=dt_fr, dt_to=dt_to, figure=figure, figure_config=figure_config, **kwargs)
        self.ds_sectors = None

        if 'A' in sat_id:
            self.ds_A = self.dock(datasource_contents=['tud', 'grace', 'dns_acc'], sat_id='A', product_version='v02',
                                  add_APEX=add_APEX, add_AACGM=add_AACGM)

        if 'B' in sat_id:
            self.ds_B = self.dock(datasource_contents=['tud', 'grace', 'dns_acc'], sat_id='B', product_version='v02',
                                  add_APEX=add_APEX, add_AACGM=add_AACGM)

        self.ds_asysym = self.dock(datasource_contents=['wdc', 'asysym'])
        self.ds_ae = self.dock(datasource_contents=['wdc', 'ae'])
        
    def group_by_sector(
        self, 
        sat_id='A', 
        sector_name='N', variable_names=None, 
        boundary_lat=None, sector_cs=None,
        x_grid_res=20*60, y_grid_res=0.5):
        ds_sc = getattr(self, 'ds_' + sat_id.upper())
        ds_leo = LEOToolbox(self.dt_fr, self.dt_to)
        ds_leo.clone_variables(ds_sc)
        ds_leo.group_by_sector(sector_name=sector_name, boundary_lat=boundary_lat, sector_cs=sector_cs)
        ds_leo.griddata_by_sector(sector_name=sector_name, variable_names=variable_names, 
                                  x_grid_res=x_grid_res, y_grid_res=y_grid_res)
        
        self.add_dataset(ds_leo, kind='user-defined')
        self.ds_sectors = self.get_current_dataset()
        return ds_leo
    
    def smooth_along_track(self, sat_id='A', variable_names=None, time_window=450., time_res=10.):
        ds_sc = getattr(self, 'ds_' + sat_id.upper())
        ds_leo = LEOToolbox(self.dt_fr, self.dt_to)
        ds_leo.clone_variables(ds_sc)
        ds_leo.smooth_along_track(
            time_window=time_window, time_res=time_res, 
            variable_names=variable_names)
        for var_name in variable_names:
            ds_sc[var_name + '_AVG'] = ds_leo[var_name+'_AVG']
            ds_sc[var_name + '_RSD'] = ds_leo[var_name+'_RSD']
            ds_sc[var_name + '_RSD_PERC'] = ds_leo[var_name+'_RSD_PERC']
         
        return

    def calc_diff_AB_by_time(self):
        rho_A = self.ds_A['rho_n']
        rho_B = self.ds_B['rho_n']
        lat_A = self.ds_A['SC_GEO_LAT']
        lat_B = self.ds_B['SC_GEO_LAT']
        diff_rho = rho_A.clone()
        diff_rho_abs = rho_A.clone()
        diff_rho.value = (rho_B.value - rho_A.value) * np.sign(lat_B.value - lat_A.value)
        diff_rho_abs.value = np.abs(rho_B.value - rho_A.value)
        diff_rho.label = r'$\Delta\rho_n$'
        diff_rho_abs.label = r'$|\Delta\rho_n|$'
        self.ds_A['DIFF_rho_n'] = diff_rho
        self.ds_A['DIFF_rho_n_ABS'] = diff_rho_abs

        diff_rho_perc = rho_A.clone()
        diff_rho_perc.value = np.abs(rho_B.value - rho_A.value) / rho_A.value * 100
        diff_rho_perc.label = r'$|\Delta\rho_n|/\rho_n^A$*100'
        diff_rho_perc.unit = '%'
        diff_rho_perc.unit_label = None
        self.ds_A['PERC_DIFF_rho_n_ABS'] = diff_rho_perc
        
        diff_rho_perc = rho_A.clone()
        diff_rho_perc.value = (rho_B.value - rho_A.value) * np.sign(lat_B.value - lat_A.value) / rho_A.value * 100
        diff_rho_perc.label = r'$\Delta\rho_n/\rho_n^A$*100'
        diff_rho_perc.unit = '%'
        diff_rho_perc.unit_label = None
        self.ds_A['PERC_DIFF_rho_n'] = diff_rho_perc
    
    def calc_d_between_A_and_B(self):
        ds_A = self.ds_A
        ds_B = self.ds_B

        glat_1 = ds_A['SC_GEO_LAT'].value
        glon_1 = ds_A['SC_GEO_LON'].value
        alt_1 = ds_A['SC_GEO_ALT'].value

        glat_2 = ds_B['SC_GEO_LAT'].value
        glon_2 = ds_B['SC_GEO_LON'].value
        alt_2 = ds_B['SC_GEO_ALT'].value

        r = 6371 + np.nanmean(alt_1.flatten())

        d = gd.calc_great_circle_distance(glat_1, glon_1, glat_2, glon_2, r=r)

        D = self.ds_A.add_variable(var_name='d_AB', value=d)
        D.unit = 'km'
        D.visual.axis[1].unit = 'km'
        D.visual.plot_config.style = '1noE'
        return D

    def quicklook_single_measurements(
            self, sat_id='A', sc_alt_lim=[340, 510], 
            figure_config={'figsize': (12, 8)}, db_layout_config=dict(),
            save_fig=False, file_dir=None, file_name=None):
        db = dashboards.TSDashboard(
            dt_fr=self.dt_fr, dt_to=self.dt_to, figure='new',
            figure_config=figure_config)
        ds = getattr(self, 'ds_' + sat_id)
        rho = ds['rho_n']

        glat = self.assign_variable('SC_GEO_LAT', dataset=ds)
        glat.visual.axis[2].label = 'GRACE-' + sat_id

        glon = self.assign_variable('SC_GEO_LON', dataset=ds)
        
        alt = self.assign_variable('SC_GEO_ALT', dataset=ds)
        alt.unit = 'km'
        alt.label = 'h'
        alt.visual.axis[1].lim = sc_alt_lim
        alt.visual.plot_config.line = {'linestyle': '', 'marker': '.'} 
        
        lst = self.assign_variable('SC_GEO_LST', dataset=ds)
        lst.label = 'LST'
        lst.visual.axis[1].lim = [0, 24]
        lst.visual.plot_config.line = {'linestyle': '', 'marker': '.'}

        glon.visual.axis[1].label = 'GLON'

        flag = self.assign_variable('FLAG', dataset=ds)

        # Dock the dataset for the geomagnetic activity indices.
        sym_h = self.assign_variable('SYM_H', dataset=self.ds_asysym)
        ae = self.assign_variable('AE', dataset=self.ds_ae)

        panel_layouts = [[sym_h, [ae]], [rho], [glat], [alt], [glon, [lst]], [flag]]
        db.set_layout(panel_layouts=panel_layouts, **db_layout_config)
        db.draw()
        if save_fig:
            db.save_figure(file_dir=file_dir, file_name=file_name)
    
        db.show()

    def quicklook_dual_measurements(self, D_lim = [200, 400], 
                figure_config={'figsize': (12, 8)}, db_layout_config=dict(), 
                save_fig=False, file_dir=None, file_name=None):
        if not hasattr(self, 'ds_B'):
            raise ValueError
        if not hasattr(self, 'ds_A'):
            raise ValueError

        db = dashboards.TSDashboard(dt_fr=self.dt_fr, dt_to=self.dt_to, figure='new', figure_config=figure_config)
        rho_A = self.ds_A['rho_n']
        rho_B = self.ds_B['rho_n']
        rho_A.visual.axis[1].label = r'$\rho$'
        rho_A.visual.axis[2].label = 'GRACE-A'
        rho_B.visual.axis[2].label = 'GRACE-B'
        diff_rho = self.ds_A['DIFF_rho_n_ABS']

        diff_rho_perc = self.ds_A['PERC_DIFF_rho_n_ABS']

        glat_A = self.assign_variable('SC_GEO_LAT', dataset=self.ds_A)
        glat_B = self.assign_variable('SC_GEO_LAT', dataset=self.ds_B)
        glat_A.visual.axis[2].label = 'GRACE-A'
        glat_B.visual.axis[2].label = 'GRACE-B'

        glon_A = self.assign_variable('SC_GEO_LON', dataset=self.ds_A)
        glon_B = self.assign_variable('SC_GEO_LON', dataset=self.ds_B)
        lst_A = self.assign_variable('SC_GEO_LST', dataset=self.ds_A)

        glon_A.visual.axis[2].label = 'GRACE-A'
        glon_B.visual.axis[2].label = 'GRACE-C'

        # Dock the dataset for the geomagnetic activity indices.
        sym_h = self.assign_variable('SYM_H', dataset=self.ds_asysym)
        ae = self.assign_variable('AE', dataset=self.ds_ae)

        D = self.ds_A['d_AB']
        D.visual.axis[1].lim = D_lim
        panel_layouts = [[sym_h, [ae]], [rho_A, rho_B], [diff_rho], [diff_rho_perc], [glat_A, glat_B, [D]]]
        db.set_layout(panel_layouts=panel_layouts, **db_layout_config)
        db.draw()
        if save_fig:
            db.save_figure(file_dir=file_dir, file_name=file_name)
    
        db.show()


def test_grace_acc():
    # Set the starting and stopping time
    dt_fr = datetime.datetime(2016, 1, 31, 0)
    dt_to = datetime.datetime(2016, 2, 4, 23, 59)
    add_APEX = True  # if True, "SC_APEX_LAT" and "SC_APEX_LON" will be added, default is False

    # Create a dashboard object, equivalent to a datahub object, however, with the additional visulization control.
    db = dashboards.TSDashboard(dt_fr=dt_fr, dt_to=dt_to, figure_config={'figsize': (12, 8)})

    # Dock the datasets. Different datasets store different types of data.
    # Dock the SWARM-A DNS-POD data
    ds_A = db.dock(datasource_contents=['tud', 'grace', 'dns_acc'], sat_id='A', product_version='v02',
                   add_APEX=add_APEX)
    # Dock the SWARM-C DNS-POD data
    ds_B = db.dock(datasource_contents=['tud', 'grace', 'dns_acc'], sat_id='B', product_version='v02',
                   add_APEX=add_APEX)

    # Assign variables from the datasets for visualization.
    rho_n_A = db.assign_variable('rho_n', dataset=ds_A)
    rho_n_B = db.assign_variable('rho_n', dataset=ds_B)
    rho_n_A.visual.axis[1].label = r'$\rho$'
    rho_n_A.visual.axis[2].label = 'GRACE-A'
    rho_n_B.visual.axis[2].label = 'GRACE-B'

    glat_A = db.assign_variable('SC_GEO_LAT', dataset=ds_A)
    glat_B = db.assign_variable('SC_GEO_LAT', dataset=ds_B)
    glat_A.visual.axis[2].label = 'GRACE-A'
    glat_B.visual.axis[2].label = 'GRACE-B'

    glon_A = db.assign_variable('SC_GEO_LON', dataset=ds_A)
    glon_B = db.assign_variable('SC_GEO_LON', dataset=ds_B)
    lst_A = db.assign_variable('SC_GEO_LST', dataset=ds_A)

    glon_A.visual.axis[2].label = 'GRACE-A'
    glon_B.visual.axis[2].label = 'GRACE-C'
    # Dock the dataset for the geomagnetic activity indices.
    ds1 = db.dock(datasource_contents=['wdc', 'asysym'])
    sym_h = db.assign_variable('SYM_H', dataset=ds1)

    # Set the plotting layout
    db.set_layout([[sym_h], [rho_n_A, rho_n_B], [glat_A, glat_B], [glon_A, [lst_A]]])
    db.draw()
    # plt.savefig('swarm_example', dpi=300)
    plt.show()
    # plt.savefig('1.png')
    # Extract the data array from variables:
    rho_n_A_array = rho_n_A.value


def test_grace_wind():
    # Set the starting and stopping time
    dt_fr = datetime.datetime(2016, 3, 13, 0)
    dt_to = datetime.datetime(2016, 3, 20, 23, 59)
    add_APEX = True  # if True, "SC_APEX_LAT" and "SC_APEX_LON" will be added, default is False

    # Create a dashboard object, equivalent to a datahub object, however, with the additional visulization control.
    db = dashboards.TSDashboard(dt_fr=dt_fr, dt_to=dt_to, figure_config={'figsize': (12, 8)})

    # Dock the datasets. Different datasets store different types of data.
    # Dock the SWARM-A DNS-POD data
    ds_A = db.dock(datasource_contents=['tud', 'grace', 'wnd_acc'], sat_id='A', product_version='v02',
                   add_APEX=add_APEX)
    # Dock the SWARM-C DNS-POD data
    ds_B = db.dock(datasource_contents=['tud', 'grace', 'wnd_acc'], sat_id='B', product_version='v02',
                   add_APEX=add_APEX)

    # Assign variables from the datasets for visualization.
    u_A = db.assign_variable('u_CROSS', dataset=ds_A)
    u_B = db.assign_variable('u_CROSS', dataset=ds_B)
    u_A.visual.axis[1].label = r'$u$'
    u_A.visual.axis[2].label = 'GRACE-A'
    u_B.visual.axis[2].label = 'GRACE-B'

    glat_A = db.assign_variable('SC_GEO_LAT', dataset=ds_A)
    glat_B = db.assign_variable('SC_GEO_LAT', dataset=ds_B)
    glat_A.visual.axis[2].label = 'GRACE-A'
    glat_B.visual.axis[2].label = 'GRACE-B'

    glon_A = db.assign_variable('SC_GEO_LON', dataset=ds_A)
    glon_B = db.assign_variable('SC_GEO_LON', dataset=ds_B)
    lst_A = db.assign_variable('SC_GEO_LST', dataset=ds_A)

    glon_A.visual.axis[2].label = 'GRACE-A'
    glon_B.visual.axis[2].label = 'GRACE-C'
    # Dock the dataset for the geomagnetic activity indices.
    ds1 = db.dock(datasource_contents=['wdc', 'asysym'])
    sym_h = db.assign_variable('SYM_H', dataset=ds1)

    # Set the plotting layout
    db.set_layout([[sym_h], [u_A, u_B], [glat_A, glat_B], [glon_A, [lst_A]]])
    db.draw()
    # plt.savefig('swarm_example', dpi=300)
    plt.show()
    # plt.savefig('2.png')
    # Extract the data array from variables:
    rho_n_A_array = u_A.value
    


def grace_density_analysis_smooth(
        dt_fr, dt_to, sat_id='A', sector_name=None, sector_cs=None, 
        boundary_lat=None, reverse_lat=False, zlims=None, interp=True, 
        db_layout_config=dict(), **kwargs):
    if zlims is None:
        zlims = [
            [5e-13, 5e-12],
            [5e-13, 5e-12],
            [-3e-13, 3e-13],
            [-20, 20] 
        ]

    grace_db = GraceAnalysisDNSACC(dt_fr, dt_to, sat_id=sat_id, **kwargs)
    if interp:
        if 'A' in sat_id:
            grace_db.ds_A = grace_db.ds_A.interp_evenly()
        if 'B' in sat_id:
            grace_db.ds_B = grace_db.ds_A.interp_evenly()
            
    grace_db.smooth_along_track(sat_id=sat_id, variable_names=['rho_n'])
    variable_names = ['rho_n', 'rho_n_AVG', 'rho_n_RSD', 'rho_n_RSD_PERC']
    reverse_lat = reverse_lat
    grace_db.group_by_sector(
        sat_id=sat_id, 
        sector_name=sector_name, variable_names=variable_names, 
        boundary_lat=boundary_lat, sector_cs=sector_cs)

    v_1 = grace_db.assign_variable('SECTOR_' + sector_name + '_GRID_rho_n', dataset=grace_db.ds_sectors)
    v_1.visual.axis[1].reverse = reverse_lat
    v_1.visual.axis[2].lim = zlims[0]
    v_1.visual.axis[1].ticks = list(range(-360, 360, 30))

    v_2 = grace_db.assign_variable('SECTOR_' + sector_name + '_GRID_rho_n_AVG', dataset=grace_db.ds_sectors)
    v_2.visual.axis[1].reverse = reverse_lat
    v_1.visual.axis[2].lim = zlims[1]
    v_2.visual.axis[1].ticks = list(range(-360, 360, 30))

    v_3 = grace_db.assign_variable('SECTOR_' + sector_name + '_GRID_rho_n_RSD', dataset=grace_db.ds_sectors)
    v_3.visual.axis[1].reverse = reverse_lat
    v_3.visual.axis[2].lim = zlims[2]
    v_3.visual.axis[1].ticks = list(range(-360, 360, 30))
    
    v_4 = grace_db.assign_variable('SECTOR_' + sector_name + '_GRID_rho_n_RSD_PERC', dataset=grace_db.ds_sectors)
    v_4.visual.axis[1].reverse = reverse_lat
    v_4.visual.axis[2].lim = zlims[3]
    v_4.visual.axis[1].ticks = list(range(-360, 360, 30))

    v_5 = grace_db.ds_asysym['SYM_H']
    v_5.visual.plot_config.line.update(color='purple', linewidth=0.5)

    # v_6 = grace_db.ds_ae['AE']
    # v_6.visual.axis[1].lim = [0, 1300]
    # v_6.visual.plot_config.line.update(color='purple', linewidth=0.5)
    
    panel_layouts = [[v_1, [v_5]], [v_2], [v_3], [v_4]]
    grace_db.set_layout(panel_layouts=panel_layouts, **db_layout_config)
    grace_db.draw()
    for panel in grace_db.panels.values():
        ax = panel.major_ax
        grace_db.ds_sectors.format_pseudo_lat_label(ax, sector_name)
    sector_str = sector_str_map[sector_name]
    title = ', '.join(('GRACE-' + sat_id, 'DNS-ACC', sector_str, sector_cs))
    grace_db.add_title(title=title)
    subtitle = r'ASC: $\sim$' + '{:4.1f}'.format(np.mean(grace_db.ds_sectors.ascending_nodes['GEO_LST'])) + ' LST' + \
               r', DSC: $\sim$' + '{:4.1f}'.format(np.mean(grace_db.ds_sectors.descending_nodes['GEO_LST'])) + ' LST'
    grace_db.add_text(x=0.5, y=1.04, text=subtitle, ha='center')
    # grace_db.show()
    # grace_db.quicklook_single_measurements()
    # grace_db.quicklook_dual_measurements()
    return grace_db



def grace_density_analysis_dual_diff_shift(
        dt_fr, dt_to, time_shift=40., t_res=10., 
        sector_name=None, sector_cs=None, boundary_lat=None, reverse_lat=False, 
        interp=True, zlims=None,
        db_layout_config=dict(), **kwargs):

    if zlims is None:
        zlims = [
            [5e-13, 5e-12],
            [-8e-14, 8e-14],
            [-2e-15, 2e-15]
        ]
    
    dt_fr_1 = dt_fr - datetime.timedelta(minutes=30)
    dt_to_1 = dt_to + datetime.timedelta(minutes=30)
    grace_db = GraceAnalysisDNSACC(dt_fr_1, dt_to_1, **kwargs)
    if interp:
        ds_A = grace_db.ds_A.interp_evenly(time_res=t_res)
        ds_B = grace_db.ds_B.interp_evenly(time_res=t_res)
    else:
        ds_A = grace_db.ds_A
        ds_B = grace_db.ds_B 

    N = int(np.fix(time_shift/t_res))
    rho_shift = ds_A['rho_n'].flatten() - np.roll(ds_B['rho_n'].flatten(), N)
    d_rho_dt = (ds_A['rho_n'].flatten() - np.roll(ds_B['rho_n'].flatten(), N)) / time_shift

    var = ds_A['rho_n'].clone()
    ds_A['delta_rho_n'] = var
    var.value = rho_shift[:, np.newaxis]
    var.label = r'$\delta \rho_n$'

    var = ds_A['rho_n'].clone()
    ds_A['partial_deriv_rho_n'] = var
    var.value = d_rho_dt[:, np.newaxis]
    var.label = r'$\partial \rho_n / \partial t$'
    var.unit = 'kg m-3'
    var.unit_label = r'kg$\cdot$m$^{-3}$$\cdot$s$^{-1}$'

    variable_names = ['rho_n', 'delta_rho_n', 'partial_deriv_rho_n']
    reverse_lat = reverse_lat
    grace_db.ds_A = ds_A
    grace_db.group_by_sector(
        sat_id='A',
        sector_name=sector_name, variable_names=variable_names,
        boundary_lat=boundary_lat, sector_cs=sector_cs)

    v_1 = grace_db.assign_variable('SECTOR_' + sector_name + '_GRID_rho_n', dataset=grace_db.ds_sectors)
    v_1.visual.axis[1].reverse = reverse_lat
    v_1.visual.axis[2].lim = zlims[0]
    v_1.visual.axis[1].ticks = list(range(-360, 360, 30))

    v_2 = grace_db.assign_variable('SECTOR_' + sector_name + '_GRID_delta_rho_n', dataset=grace_db.ds_sectors)
    v_2.visual.axis[1].reverse = reverse_lat
    v_2.visual.axis[2].lim = zlims[1]
    v_2.visual.axis[1].ticks = list(range(-360, 360, 30))

    v_3 = grace_db.assign_variable('SECTOR_' + sector_name + '_GRID_partial_deriv_rho_n', dataset=grace_db.ds_sectors)
    v_3.visual.axis[2].unit = '@v.unit_label'
    v_3.visual.axis[1].reverse = reverse_lat
    v_3.visual.axis[2].lim = zlims[2]
    v_3.visual.axis[1].ticks = list(range(-360, 360, 30))

    v_4 = grace_db.ds_asysym['SYM_H']
    v_4.visual.plot_config.line.update(color='purple')
    panel_layouts = [[v_1, [v_4]], [v_2], [v_3]]
    grace_db.set_layout(panel_layouts=panel_layouts, **db_layout_config)
    grace_db.draw(dt_fr=dt_fr, dt_to=dt_to)
    for panel in grace_db.panels.values():
        ax = panel.major_ax
        grace_db.ds_sectors.format_pseudo_lat_label(ax, sector_name)
    sector_str = sector_str_map[sector_name]
    title = ', '.join(('GRACE-AB', 'DNS-ACC', f'Shift: {str(time_shift)}', sector_str, sector_cs))
    grace_db.add_title(title=title)
    subtitle = r'ASC: $\sim$' + '{:4.1f}'.format(np.mean(grace_db.ds_sectors.ascending_nodes['GEO_LST'])) + ' LST' + \
               r', DSC: $\sim$' + '{:4.1f}'.format(np.mean(grace_db.ds_sectors.descending_nodes['GEO_LST'])) + ' LST'
    grace_db.add_text(x=0.5, y=1.04, text=subtitle, ha='center')
    # grace_db.show()
    # grace_db.quicklook_single_measurements()

    return grace_db


def grace_density_analysis_dual_diff(
    dt_fr, dt_to, sector_name=None, sector_cs=None, boundary_lat=None, reverse_lat=False, 
    interp=True, zlims=None,
    db_layout_config=dict(), **kwargs):
    grace_db = GraceAnalysisDNSACC(dt_fr, dt_to)
    
    if zlims is None:
        zlims = [
           [5e-13, 5e-12],
           [-3e-13, 3e-13],
           [-10, 10] 
        ]
        
    if interp:
        grace_db.ds_A = grace_db.ds_A.interp_evenly()
        grace_db.ds_B = grace_db.ds_B.interp_evenly()

    grace_db.calc_d_between_A_and_B()
    grace_db.calc_diff_AB_by_time()
    variable_names = ['rho_n', 'DIFF_rho_n', 'PERC_DIFF_rho_n']
    reverse_lat = reverse_lat
    grace_db.group_by_sector(
        sat_id='A', 
        sector_name=sector_name, variable_names=variable_names, 
        boundary_lat=boundary_lat, sector_cs=sector_cs)

    v_1 = grace_db.assign_variable('SECTOR_' + sector_name + '_GRID_rho_n', dataset=grace_db.ds_sectors)
    v_1.visual.axis[1].reverse = reverse_lat
    v_1.visual.axis[2].lim = zlims[0]
    v_1.visual.axis[1].ticks = list(range(-360, 360, 30))

    v_2 = grace_db.assign_variable('SECTOR_' + sector_name + '_GRID_DIFF_rho_n', dataset=grace_db.ds_sectors)
    v_2.visual.axis[1].reverse = reverse_lat
    v_2.visual.axis[2].lim = zlims[1]
    v_2.visual.axis[1].ticks = list(range(-360, 360, 30))

    v_3 = grace_db.assign_variable('SECTOR_' + sector_name + '_GRID_PERC_DIFF_rho_n', dataset=grace_db.ds_sectors)
    v_3.visual.axis[1].reverse = reverse_lat
    v_3.visual.axis[2].lim = zlims[2]
    v_3.visual.axis[1].ticks = list(range(-360, 360, 30))

    v_4 = grace_db.ds_asysym['SYM_H']
    v_4.visual.plot_config.line.update(color='purple')
    panel_layouts = [[v_1, [v_4]], [v_2], [v_3]]
    grace_db.set_layout(panel_layouts=panel_layouts, **db_layout_config)
    grace_db.draw()
    for panel in grace_db.panels.values():
        ax = panel.major_ax
        grace_db.ds_sectors.format_pseudo_lat_label(ax, sector_name)
    sector_str = sector_str_map[sector_name]
    title = ', '.join(('GRACE-A&B', 'DNS-ACC', sector_str, sector_cs))
    grace_db.add_title(title=title)
    subtitle = r'ASC: $\sim$' + '{:4.1f}'.format(np.mean(grace_db.ds_sectors.ascending_nodes['GEO_LST'])) + ' LST' + \
               r', DSC: $\sim$' + '{:4.1f}'.format(np.mean(grace_db.ds_sectors.descending_nodes['GEO_LST'])) + ' LST'
    grace_db.add_text(x=0.5, y=1.04, text=subtitle, ha='center')
    # grace_db.show()
    # grace_db.quicklook_single_measurements()
    # grace_db.quicklook_dual_measurements()
    return grace_db


def overview_sigle_satellite(dt_fr, dt_to, sat_id='A', 
                             save_fig=False, file_dir=None, file_name=None, 
                             sc_alt_lim=[320, 510], db_layout_config=dict(), **kwargs):
    db = GraceAnalysisDNSACC(dt_fr, dt_to, sat_id=sat_id, **kwargs)
    db.quicklook_single_measurements(
        sc_alt_lim=sc_alt_lim, save_fig=save_fig, file_dir=file_dir, file_name=file_name,
        db_layout_config=db_layout_config)

    
def overview_dual_satellites(
        dt_fr, dt_to, save_fig=False, file_dir=None, file_name=None, 
        D_lim=[200, 400], db_layout_config=dict(), interp=True, **kwargs):
    db = GraceAnalysisDNSACC(dt_fr, dt_to, **kwargs)
    
    db.ds_A = db.ds_A.interp_evenly()
    db.ds_B = db.ds_B.interp_evenly() 
    db.calc_d_between_A_and_B()
    db.calc_diff_AB_by_time()
    db.quicklook_dual_measurements(D_lim=D_lim, 
                                   db_layout_config=db_layout_config)
    if save_fig:
        db.save_figure(file_dir=file_dir, file_name=file_name)

sector_str_map = {'N': 'Pole: North', 'S': 'Pole: South', 'ASC': 'Ascending', 'DSC': 'Descending'}