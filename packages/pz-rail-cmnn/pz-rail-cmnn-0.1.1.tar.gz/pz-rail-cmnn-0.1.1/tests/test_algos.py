import numpy as np
import pytest
from rail.core.stage import RailStage
from rail.core.data import DataStore, TableHandle
from rail.core.algo_utils import one_algo
from rail.core.utils import RAILDIR
from rail.estimation.algos import cmnn

default_dict = {'zmin': 0.0, 'zmax': 3.0, 'nzbins': 301, 'min_n': 4}


@pytest.mark.parametrize("out_method,zb_expected",
                         [
                             (0, np.array([0.15, 0.14, 0.12,
                                           0.13, 0.15, 0.12, 0.15,
                                           0.14, 0.12, 0.15])),
                             (1, np.array([0.11, 0.15, 0.14,
                                           0.13, 0.11, 0.13, 0.15,
                                           0.15, 0.11, 0.11])),
                             (2, np.array([0.15, 0.10, 0.12,
                                           0.13, 0.11, 0.13, 0.15,
                                           0.14, 0.11, 0.14]))
                         ])
                         
def test_cmnn(out_method, zb_expected):
    train_config_dict = default_dict.copy()
    estim_config_dict = default_dict.copy()
    train_config_dict["hdf5_groupname"] = "photometry"
    train_config_dict["model"] = "model.tmp"

    estim_config_dict["hdf5_groupname"] = "photometry"
    estim_config_dict["model"] = "model.tmp"
    estim_config_dict["selection_mode"] = out_method
    # zb_expected = np.array([0.13, 0.13, 0.13, 0.12, 0.12, 0.13, 0.12, 0.13,
    #                         0.12, 0.12])
    train_algo = cmnn.Inform_CMNNPDF
    pz_algo = cmnn.CMNNPDF
    results, rerun_results, rerun3_results = one_algo("CMNN", train_algo, pz_algo, train_config_dict, estim_config_dict)
    assert np.isclose(results.ancil['zmode'], zb_expected, atol=0.02).all()
    assert np.isclose(results.ancil['zmode'], rerun_results.ancil['zmode']).all()


def test_cmnn_nondetect_replace():
    train_config_dict = default_dict.copy()
    estim_config_dict = default_dict.copy()
    train_config_dict["hdf5_groupname"] = "photometry"
    train_config_dict["model"] = "model.tmp"
    train_config_dict["nondetect_replace"] = True

    estim_config_dict["hdf5_groupname"] = "photometry"
    estim_config_dict["model"] = "model.tmp"
    zb_expected = np.array([0.11, 0.15, 0.14, 0.13, 0.11, 0.13, 0.15, 0.15,
                            0.11, 0.11])
    train_algo = cmnn.Inform_CMNNPDF
    pz_algo = cmnn.CMNNPDF
    results, rerun_results, rerun3_results = one_algo("CMNN", train_algo, pz_algo, train_config_dict, estim_config_dict)
    assert np.isclose(results.ancil['zmode'], zb_expected, atol=0.02).all()
    assert np.isclose(results.ancil['zmode'], rerun_results.ancil['zmode']).all()


def test_missing_groupname_keyword():
    config_dict = default_dict.copy()
    with pytest.raises(ValueError):
        _ = cmnn.CMNNPDF.make_stage(**config_dict)


def test_wrong_modelfile_keyword():
    RailStage.data_store.clear()
    config_dict = default_dict.copy()
    config_dict["hdf5_groupname"] = "photometry"
    config_dict["model"] = "notreal.pkl"
    with pytest.raises(FileNotFoundError):
        pz_algo = cmnn.CMNNPDF.make_stage(**config_dict)
        assert pz_algo.model is None
