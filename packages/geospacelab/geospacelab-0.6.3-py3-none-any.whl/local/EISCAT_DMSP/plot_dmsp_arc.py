import copy
import datetime
import numpy as np

import geospacelab.visualization.mpl as mpl
from geospacelab.visualization.mpl.dashboards import TSDashboard
from geospacelab.visualization.mpl.geomap.geodashboards import GeoDashboard


def dmsp_plot():
    dt_c = datetime.datetime(2010, 6, 16, 15, 16, 16)
    sat_id = 'f18'
    site = 'ESR'
    Sigma_lim = [0, 30]
    file_path_cdt = '/home/lei/01-Work/01-Project/OY21-VisitingPhD/20100616_mono/fig2.pkl'

    fig = mpl.create_figure(figsize=(12, 8))

    add_ssusi_dashboard(fig, dt_c, sat_id, site=site)
    add_cdt_dashboard(fig, dt_c, file_path_cdt, sat_id, site=site, Sigma_lim=Sigma_lim)

    fig.show()
    fig.savefig('fig2_arc.png')


def add_cdt_dashboard(fig, dt_c, file_path, sat_id, time_span=10, site=None, Sigma_lim =[0, 30]):
    import pickle

    with open(file_path, 'rb') as f_pickle:
        data = pickle.load(f_pickle)

    dts = np.array(data['UT'])

    timeline_extra_labels = ['GEO_LAT', 'GEO_LON', 'AACGM_LAT', 'AACGM_MLT']
    db = fig.add_dashboard(label='Conductivity', dashboard_class=TSDashboard,
                           dt_fr=dts[0], dt_to=dts[-1], timeline_extra_labels=timeline_extra_labels)

    ds_e = db.dock(
        datasource_contents=['madrigal', 'satellites', 'dmsp', 'e'],
        dt_fr = dts[0], dt_to = dts[-1], sat_id=sat_id, replace_orbit=True)

    ds_1 = db.add_dataset(kind='UserDefined')
    ds_1.clone_variables(ds_e)
    ds_1['SC_DATETIME'].value = dts[:, np.newaxis]
    ds_1['jE_e'].value = np.flip(10**data['electron energy'].T, axis=1)
    ds_1['jE_e'].visual.plot_config.colorbar = {'cax_label_config': {'size': 8}}
    ds_1['jE_i'].value = np.flip(10**data['ion energy'].T, axis=1)
    ds_1['jE_i'].visual.plot_config.colorbar = {'cax_label_config': {'size': 8}}
    ds_1['JE_e'].value = data['I_e'][:, np.newaxis]
    ds_1['JE_e'].unit = 'ergs/cm2/s'
    ds_1['JE_e'].unit_label = r'ergs/cm$^2$/s'
    ds_1['JE_i'].value = data['I_i'][:, np.newaxis]
    ds_1['JE_e'].visual.axis[1].lim = [None, None]
    ds_1['JE_i'].unit = 'ergs/cm2/s'
    ds_1['JE_i'].unit_label = r'ergs/cm$^2$/s'
    ds_1['E_e_MEAN'].value = 10**data['\x08ar{E}_e'][:, np.newaxis]
    ds_1['E_i_MEAN'].value = 10**data['\x08ar{E}_i'][:, np.newaxis]

    var = ds_1.add_variable(var_name='Sigma_P_R87')
    var.label = r'$\Sigma_P^{R87}$'
    var.value = data['P_e'][:, np.newaxis]
    var.unit = 'mhos'
    var.depends[0] = copy.deepcopy(ds_1['E_e_MEAN'].depends[0])
    var.visual = ds_1['E_e_MEAN'].visual.clone()
    var.visual.axis[1].lim = Sigma_lim
    var.visual.axis[1].scale = 'linear'
    var.visual.axis[1].label = r'$\Sigma_P$'
    var.visual.axis[1].unit = '@v.unit'
    var.visual.axis[2].label = '@v.label'

    var = ds_1.add_variable(var_name='Sigma_H_R87')
    var.label = r'$\Sigma_H^{R87}$'
    var.value = data['H_e'][:, np.newaxis]
    var.unit = 'mhos'
    var.depends[0] = copy.deepcopy(ds_1['E_e_MEAN'].depends[0])
    var.visual = ds_1['E_e_MEAN'].visual.clone()
    var.visual.axis[1].lim = Sigma_lim
    var.visual.axis[1].scale = 'linear'
    var.visual.axis[1].label = r'$\Sigma_H$'
    var.visual.axis[1].unit = '@v.unit'
    var.visual.axis[2].label = '@v.label'

    var = ds_1.add_variable(var_name='Sigma_P_G01')
    var.label = r'$\Sigma_P^{G01}$'
    var.value = data['P_i'][:, np.newaxis]
    var.unit = 'mhos'
    var.depends[0] = copy.deepcopy(ds_1['E_e_MEAN'].depends[0])
    var.visual = ds_1['E_e_MEAN'].visual.clone()
    var.visual.axis[1].lim = Sigma_lim
    var.visual.axis[1].scale = 'linear'
    var.visual.axis[1].label = r'$\Sigma_P$'
    var.visual.axis[1].unit = '@v.unit'
    var.visual.axis[2].label = '@v.label'

    var = ds_1.add_variable(var_name='Sigma_H_G01')
    var.label = r'$\Sigma_H^{G01}$'
    var.value = data['H_i'][:, np.newaxis]
    var.unit = 'mhos'
    var.depends[0] = copy.deepcopy(ds_1['E_e_MEAN'].depends[0])
    var.visual = ds_1['E_e_MEAN'].visual.clone()
    var.visual.axis[1].lim = Sigma_lim
    var.visual.axis[1].scale = 'linear'
    var.visual.axis[1].label = r'$\Sigma_H$'
    var.visual.axis[1].unit = '@v.unit'
    var.visual.axis[2].label = '@v.label'

    panel_layouts = [
        [ds_1['jE_e']],
        [ds_1['jE_i']],
        [ds_1['JE_e'], ds_1['JE_i']],
        [ds_1['E_e_MEAN'], ds_1['E_i_MEAN']],
        [ds_1['Sigma_P_R87'], ds_1['Sigma_P_G01']],
        [ds_1['Sigma_H_R87'], ds_1['Sigma_H_G01']],
    ]
    db.set_layout(panel_layouts, top=0.95, bottom=0.12, left=0.5, right=0.88)
    db.draw()
    db.add_vertical_line(dt_c)




def load_cdt_data(ds, file_path):
    pass

def add_ssusi_dashboard(fig, dt_c, sat_id, pole='N', orbit_id=None, band='LBHS', site=None):
    dt_fr = dt_c - datetime.timedelta(minutes=30)
    dt_to = dt_c + datetime.timedelta(minutes=30)
    db = fig.add_dashboard(label='SSUSI', dashboard_class=GeoDashboard, dt_fr=dt_fr, dt_to=dt_to)
    db.set_layout(1, 1, left=0.03, right=0.33, bottom=0.1, top=0.9, )
    ds_ssusi = db.dock(datasource_contents=['jhuapl', 'dmsp', 'ssusi', 'edraur'], pole=pole, sat_id=sat_id, orbit_id=orbit_id)
    ds_s1 = db.dock(
        datasource_contents=['madrigal', 'satellites', 'dmsp', 'e'],
        dt_fr=dt_fr,
        dt_to=dt_to,
        sat_id=sat_id, replace_orbit=True)
    # Add a polar map panel to the dashboard. Currently the style is the fixed MLT at mlt_c=0. See the keywords below:
    panel_dmsp = db.add_polar_map(
        row_ind=0, col_ind=0, style='mlt-fixed', cs='AACGM',
        mlt_c=0., pole=pole, ut=dt_c, boundary_lat=55., mirror_south=True
    )
    # Get the variables: LBHS emission intensiy, corresponding times and locations
    lbhs = db.assign_variable('GRID_AUR_' + band, dataset=ds_ssusi)
    dts = db.assign_variable('DATETIME', dataset=ds_ssusi).value.flatten()
    mlat = db.assign_variable('GRID_MLAT', dataset=ds_ssusi).value
    mlon = db.assign_variable('GRID_MLON', dataset=ds_ssusi).value
    mlt = db.assign_variable(('GRID_MLT'), dataset=ds_ssusi).value

    # Search the index for the time to plot, used as an input to the following polar map
    ind_t = ds_ssusi.get_time_ind(ut=dt_c, time_res=90*60)
    lbhs_ = lbhs.value[ind_t]
    mlat_ = mlat[ind_t]
    mlon_ = mlon[ind_t]
    mlt_ = mlt[ind_t]

    # Some settings for plotting.
    pcolormesh_config = lbhs.visual.plot_config.pcolormesh
    # Overlay the SSUSI image in the map.
    ipc = panel_dmsp.overlay_pcolormesh(
        data=lbhs_, coords={'lat': mlat_, 'lon': mlon_, 'mlt': mlt_}, cs='AACGM', **pcolormesh_config)
    # Add a color bar
    panel_dmsp.add_colorbar(ipc, c_label=band + " (R)", c_scale=pcolormesh_config['c_scale'], left=1.08, bottom=0.1,
                            width=0.05, height=0.7)

    # Overlay the gridlines
    panel_dmsp.overlay_gridlines(lat_res=5, lon_label_separator=5)

    # Overlay the coastlines in the AACGM coordinate
    panel_dmsp.overlay_coastlines()

    # Overlay the satellite trajectory with ticks
    sc_dt = ds_s1['SC_DATETIME'].value.flatten()
    sc_lat = ds_s1['SC_GEO_LAT'].value.flatten()
    sc_lon = ds_s1['SC_GEO_LON'].value.flatten()
    sc_alt = ds_s1['SC_GEO_ALT'].value.flatten()
    sc_coords = {'lat': sc_lat, 'lon': sc_lon, 'height': sc_alt}
    panel_dmsp.overlay_sc_trajectory(sc_ut=sc_dt, sc_coords=sc_coords, cs='GEO')

    # Overlay sites
    if site is not None:
        if site == 'ESR':
            lat = 78.15
            lon = 16.02
        elif site == 'TRO':
            lat = 69.58
            lon = 19.23
        else:
            raise NotImplementedError
        panel_dmsp.overlay_sites(
            site_ids=[site], coords={'lat': [lat], 'lon': [lon], 'height': 0.},
            cs='GEO', marker='o', markersize=6, color='k', alpha=1, markerfacecolor='r', markeredgecolor='k')

    # Add the title and save the figure
    polestr = 'North' if pole == 'N' else 'South'
    panel_dmsp.add_title(
        title='DMSP/SSUSI, ' + band + ', ' + sat_id.upper() + ', ' + polestr + ', ' + dt_c.strftime(
            '%Y-%m-%d %H%M UT'))


if __name__ == "__main__":
    dmsp_plot()