from scipy.spatial import Voronoi
from tyssue.utils import utils
from tyssue import Sheet, SheetGeometry
from tyssue.generation import three_faces_sheet, extrude
from numpy.testing import assert_almost_equal
from tyssue import Monolayer, config


def test_scaled_unscaled():

    sheet = Sheet('3faces_3D', *three_faces_sheet())
    SheetGeometry.update_all(sheet)

    def mean_area():
        return sheet.face_df.area.mean()

    prev_area = sheet.face_df.area.mean()

    sc_area = utils.scaled_unscaled(mean_area, 2,
                                    sheet, SheetGeometry)
    post_area = sheet.face_df.area.mean()
    assert post_area == prev_area
    assert_almost_equal(sc_area / post_area, 4.)




def test_modify():

    datasets, _ = three_faces_sheet()
    extruded = extrude(datasets, method='translation')
    mono = Monolayer('test', extruded,
                     config.geometry.bulk_spec())
    mono.update_specs(config.dynamics.quasistatic_bulk_spec(),
                      reset=True)
    modifiers = {
        'apical' : {
            'edge': {'line_tension': 1.},
            'face': {'contractility': 0.2},
            },
        'basal' : {
            'edge': {'line_tension': 3.},
            'face': {'contractility': 0.1},
            }
        }

    utils.modify_segments(mono, modifiers)
    assert mono.edge_df.loc[mono.apical_edges,
                            'line_tension'].unique()[0] == 1.
    assert mono.edge_df.loc[mono.basal_edges,
                            'line_tension'].unique()[0] == 3.
