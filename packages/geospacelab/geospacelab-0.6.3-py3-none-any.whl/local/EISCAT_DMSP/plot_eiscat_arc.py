import copy
import datetime
import numpy as np

import geospacelab.visualization.mpl as mpl
from geospacelab.visualization.mpl.dashboards import TSDashboard
from geospacelab.visualization.mpl.geomap.geodashboards import GeoDashboard


def eiscat_plot():

    dt_c = datetime.datetime(2010, 6, 16, 15, 16, 16)
    dt_fr = dt_c - datetime.timedelta(hours=4)
    dt_to = dt_c + datetime.timedelta(hours=4)
    site = 'ESR'
    antenna = '42m'
    modulation = ''
    data_file_type = 'eiscat-hdf5'
    Sigma_lim = [0, 30]
    file_path_cdt = '/home/lei/01-Work/01-Project/OY21-VisitingPhD/20100616_mono/fig3.pkl'

    fig = mpl.create_figure(figsize=(8, 8))

    add_eiscat_dashboard(
        fig, file_path_cdt, dt_c, dt_fr, dt_to, site, antenna, modulation, data_file_type, Sigma_lim)

    fig.show()
    fig.savefig('fig3_arc.png')


def add_eiscat_dashboard(fig, file_path, dt_c, dt_fr, dt_to, site, antenna, modulation, data_file_type, Sigma_lim):
    import pickle

    with open(file_path, 'rb') as f_pickle:
        data = pickle.load(f_pickle)

    dts = np.array(data['UT'])
    inds = np.where((dts>=dt_fr) & (dts<=dt_to))[0]
    db = fig.add_dashboard(label='Conductivity', dashboard_class=TSDashboard,
                           dt_fr=dt_fr, dt_to=dt_to)

    ds_eiscat = db.dock(datasource_contents=['madrigal', 'isr', 'eiscat'], dt_fr=dt_fr, dt_to=dt_to, site=site,
                        antenna=antenna, modulation=modulation, data_file_type=data_file_type, load_mode='AUTO', allow_load=True)

    ds_1 = db.add_dataset(kind='UserDefined')
    ds_1.clone_variables(ds_eiscat)
    ds_1['DATETIME'].value = dts[inds, np.newaxis]
    ds_1['HEIGHT'].value = np.tile(data['height'], (len(inds), 1))
    ds_1['n_e'].value = 10**data['N_e'][:, inds].T
    ds_1['n_e'].visual.axis[1].lim = [80, 180]

    var = ds_1['sigma_P'] = ds_1['n_e'].clone()
    var.label = r'$\sigma_P$'
    value = 10**data['Pedersen_conductivity'][:, inds]
    var.value = value.T
    var.unit = 'mhos/m'
    var.unit_label = None
    var.visual.axis[1].lim = [80, 180]
    var.visual.axis[2].lim = [5e-7, 1e-3]
    
    var = ds_1['sigma_H'] = ds_1['n_e'].clone()
    var.label = r'$\sigma_H$'
    value = 10**data['Hall_conductivity'][:, inds]
    var.value = value.T
    var.unit = 'mhos/m'
    var.unit_label = None
    var.visual.axis[1].lim = [80, 180]
    var.visual.axis[2].lim = [5e-7, 1e-3]
    
    var = ds_1.add_variable(var_name='Sigma_P_Standard')
    var.label = r'$\Sigma_P^{Standard}$'
    var.value = np.array(data['Pedersen_conductance'][inds])[:, np.newaxis]
    var.unit = 'mhos'
    var.group = r'$\Sigma_P$'
    var.depends[0] = {'UT': 'DATETIME'}
    plot_config_1d = {
        'linestyle':        '',
        'linewidth':        1.5,
        'marker':           '.',
        'markersize':       3,
    }
    var.visual.plot_config.style = '1P'
    var.visual.plot_config.line = plot_config_1d
    var.visual.axis[1].lim = Sigma_lim
    var.visual.axis[1].scale = 'linear'
    var.visual.axis[1].label = '@v.group'
    var.visual.axis[1].unit = '@v.unit'
    var.visual.axis[2].label = '@v.label'
    
    var = ds_1['Sigma_H_Standard'] = ds_1['Sigma_P_Standard'].clone() 
    var.label = r'$\Sigma_H^{Standard}$'
    var.value = np.array(data['Hall_conductance'])[inds][:, np.newaxis]
    
    var = ds_1['Sigma_P_EUV'] = ds_1['Sigma_P_Standard'].clone() 
    var.label = r'$\Sigma_P^{EUV}$'
    var.value = np.array(data['Pedersen_conductance from EUV'])[inds][:, np.newaxis]
    
    var = ds_1['Sigma_H_EUV'] = ds_1['Sigma_P_Standard'].clone() 
    var.label = r'$\Sigma_H^{EUV}$'
    var.value = np.array(data['Hall_conductance from EUV'])[inds][:, np.newaxis]     

    panel_layouts = [
        [ds_1['n_e']],
        [ds_1['sigma_P']],
        [ds_1['sigma_H']],
        [ds_1['Sigma_P_EUV'], ds_1['Sigma_P_Standard']],
        [ds_1['Sigma_H_EUV'], ds_1['Sigma_H_Standard']],
    ]

    db.set_layout(panel_layouts, top=0.92, bottom=0.09, left=0.12, right=0.85)
    db.draw()
    db.add_vertical_line(dt_c)
    title = site + ', ' + antenna + ', ' + ds_eiscat.experiment + ', ' + dt_c.strftime('%Y-%m-%d %H%M%S UT')
    db.add_title(x=0.5, y=1.02, title=title, append_time=False)


if __name__ == "__main__":
    eiscat_plot()