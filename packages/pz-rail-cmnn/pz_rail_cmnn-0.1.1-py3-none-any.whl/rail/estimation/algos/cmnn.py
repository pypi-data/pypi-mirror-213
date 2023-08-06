"""
Implementation of the color-matched nearest neighbor (CMNN) algorithm
See https://ui.adsabs.harvard.edu/abs/2018AJ....155....1G/abstract
for more details
"""

import numpy as np
import qp
from scipy.stats import chi2
from ceci.config import StageParameter as Param
from rail.estimation.estimator import CatEstimator, CatInformer
from rail.core.common_params import SHARED_PARAMS


def _computecolordata(data, column_names, err_names):
    """
    make a dataset consisting of N-1 colors and errors in quadrature.
    """
    numcols = len(column_names)
    numerrcols = len(err_names)
    if numcols != numerrcols:  # pragma: no cover
        raise ValueError("number of magnitude and error columns must be the same!")
    coldata = np.array(data[column_names[0]] - data[column_names[1]])
    errdata = np.array(data[err_names[0]]**2 + data[err_names[1]]**2)
    for i in range(numcols - 2):
        tmpcolor = data[column_names[i + 1]] - data[column_names[i + 2]]
        tmperr = np.sqrt(data[err_names[i + 1]]**2 + data[err_names[i + 2]]**2)
        coldata = np.vstack((coldata, tmpcolor))
        errdata = np.vstack((errdata, tmperr))
    return coldata.T, errdata.T


class Inform_CMNNPDF(CatInformer):
    """compute colors and color errors for CMNN training set and
       store in a model file that will be used by the CMNNPDF stage
    """
    name = 'Inform_CMNNPDF'
    config_options = CatInformer.config_options.copy()
    config_options.update(bands=SHARED_PARAMS,
                          err_bands=SHARED_PARAMS,
                          redshift_col=SHARED_PARAMS,
                          mag_limits=SHARED_PARAMS,
                          nondetect_val=SHARED_PARAMS,
                          nondetect_replace=Param(bool, False, msg="set to True to replace non-detects,"
                                                  " False to ignore in distance calculation"))

    def __init__(self, args, comm=None):
        """ Constructor
        Do CatInformer specific initialization, then check on bands """
        CatInformer.__init__(self, args, comm=comm)

    def run(self):
        if self.config.hdf5_groupname:
            training_data = self.get_data('input')[self.config.hdf5_groupname]
        else:  # pragma: no cover
            training_data = self.get_data('input')
        specz = np.array(training_data[self.config['redshift_col']])

        # replace nondetects
        for col, err in zip(self.config.bands, self.config.err_bands):
            if np.isnan(self.config.nondetect_val):  # pragma: no cover
                mask = np.isnan(training_data[col])
            else:
                mask = np.isclose(training_data[col], self.config.nondetect_val)
            if self.config.nondetect_replace:
                training_data[col][mask] = self.config.mag_limits[col]
                training_data[err][mask] = 1.0  # could also put 0.757 for 1 sigma, but slightly inflated seems good
            else:
                training_data[col][mask] = np.nan
                training_data[err][mask] = np.nan

        col_data, col_err = _computecolordata(training_data,
                                              self.config.bands,
                                              self.config.err_bands)

        self.model = dict(train_color=col_data, train_err=col_err, truez=specz,
                          nondet_choice=self.config.nondetect_replace)
        self.add_data('model', self.model)


class CMNNPDF(CatEstimator):
    """Color Matched Nearest Neighbor Estimator
    Note that there are several modifications from the original CMNN, mainly that
    the original estimator dropped non-detections from the Mahalnobis distance
    calculation. However, there is information in a non-detection, so instead here
    I've replaced the non-detections with 1 sigma limit and a magnitude
    uncertainty of 1.0 and fixed the degrees of freedom to be the number of
    magnitude bands minus one.

    Current implementation returns a single Gaussian for each galaxy with a width
    determined by the std deviation of all galaxies within the range set by the
    ppf value.

    There are three options for how to choose the central value of the Gaussian
    and that option is set using the `selection_mode` config parameter (integer):
    option 0: randomly choose one of the neighbors within the PPF cutoff
    option 1: choose the value with the smallest Mahalnobis distance
    option 2: random choice as in option 0, but weighted by distance

    If a test galaxy does not have enough training galaxies it is
    assigned a redshift `bad_redshift_val` and a width `bad_redshift_err`, both
    of which are config parameters that can be set by the user.  Note that this
    should only happen if the number of training galaxies is smaller than
    min_n, which is unlikely, but is included here for completeness.
    """
    name = 'CMNNPDF'
    config_options = CatEstimator.config_options.copy()
    config_options.update(zmin=SHARED_PARAMS,
                          zmax=SHARED_PARAMS,
                          nzbins=SHARED_PARAMS,
                          bands=SHARED_PARAMS,
                          err_bands=SHARED_PARAMS,
                          nondetect_val=SHARED_PARAMS,
                          mag_limits=SHARED_PARAMS,
                          redshift_col=SHARED_PARAMS,
                          seed=Param(int, 66, msg="random seed used in selection mode"),
                          ppf_value=Param(float, 0.68, msg="PPF value used in Mahalanobis distance"),
                          selection_mode=Param(int, 1, msg="select which mode to choose the redshift estimate:"
                                               "0: randomly choose, 1: nearest neigh, 2: weighted random"),
                          min_n=Param(int, 25, msg="minimum number of training galaxies to use"),
                          min_thresh=Param(float, 0.0001, msg="minimum threshold cutoff"),
                          min_dist=Param(float, 0.0001, msg="minimum Mahalanobis distance"),
                          bad_redshift_val=Param(float, 99., msg="redshift to assign bad redshifts"),
                          bad_redshift_err=Param(float, 10., msg="Gauss error width to assign to bad redshifts")
                          )

    def __init__(self, args, comm=None):
        """ Constructor:
        Do Estimator specific initialization """
        self.truezs = None
        self.model = None
        self.zgrid = None
        CatEstimator.__init__(self, args, comm=comm)
        usecols = self.config.bands.copy()
        usecols.append(self.config.redshift_col)
        self.usecols = usecols

    def open_model(self, **kwargs):
        CatEstimator.open_model(self, **kwargs)
        if self.model is None:  # pragma: no cover
            return
        self.train_color = self.model['train_color']
        self.train_err = self.model['train_err']
        self.truez = self.model['truez']
        self.nondet_choice = self.model['nondet_choice']

    def _process_chunk(self, start, end, data, first):
        print(f"Process {self.rank} estimating PZ PDF for rows {start:,} - {end:,}")
        # replace nondetects
        for col, err in zip(self.config.bands, self.config.err_bands):
            if np.isnan(self.config.nondetect_val):  # pragma: no cover
                mask = np.isnan(data[col])
            else:
                mask = np.isclose(data[col], self.config.nondetect_val)
            if self.nondet_choice:
                data[col][mask] = self.config.mag_limits[col]
                data[err][mask] = 1.0  # could also put 0.757 for 1 sigma, but slightly inflated seems good
            else:
                data[col][mask] = np.nan
                data[err][mask] = np.nan

        test_color, test_err = _computecolordata(data,
                                                 self.config.bands,
                                                 self.config.err_bands)
        num_gals = test_color.shape[0]
        ncols = test_color.shape[1]
        # chi2.ppf calculation is slow and repeated a bunch if nondet_choice is false
        # so precompute the potential values here and put in a lookup table
        thresh_table = np.zeros(ncols + 1)
        thresh_table[0] = 0.0  # this will never be used, just put in a zero
        for ii in range(1, ncols + 1):
            thresh_table[ii] = chi2.ppf(self.config.ppf_value, float(ii))
        chunk_pz = np.zeros(num_gals)
        chunk_pze = np.zeros(num_gals)
        chunk_ncm = np.zeros(num_gals, dtype=int)
        chunk_colused = np.zeros(num_gals, dtype=int)
        rng = np.random.default_rng(seed=self.config.seed + start)
        for ii in range(num_gals):
            MahalanobisDistance = np.nansum((test_color[ii] - self.train_color)**2 / test_err[ii]**2, axis=1, dtype='float')
            # original CMNN algorithm determines degrees of freedom in a roundabout way that takes into account
            # non-detect bands.  I think with the replacement of non-detects with 1 sigma limit and large error
            # we should be ok to set this to just be num_bands - 1
            if self.nondet_choice:
                deg_of_freedom = len(self.config.bands) - 1
                threshold = chi2.ppf(self.config.ppf_value, deg_of_freedom)
                chunk_colused[ii] = deg_of_freedom
            else:
                doftest = ~np.isnan(test_color[ii])
                deg_of_freedom = np.nansum((test_color[ii]**2 + self.train_color**2 + 1.0) / (test_color[ii]**2 + self.train_color**2 + 1.0),
                                           axis=1, dtype='int')
                ntrain = len(deg_of_freedom)
                # this is the slow way to do things, comment out and replace!
                # threshold = np.array([chi2.ppf(self.config.ppf_value, deg_of_freedom[xx]) for xx in range(ntrain)])
                # lookup table-based way to get thresholds
                threshold = np.array([thresh_table[deg_of_freedom[xx]] for xx in range(ntrain)])
                chunk_colused[ii] = np.sum(doftest)
            # find the indices of galaxies meeting CMNN subset criteria
            index = np.where((threshold > self.config.min_thresh) &
                             (MahalanobisDistance > self.config.min_dist) &
                             (MahalanobisDistance <= threshold))[0]

            if len(index) >= self.config.min_n:

                # choose randomly from the color matched sample
                if self.config.selection_mode == 0:
                    rival = rng.choice(index, size=1, replace=False)[0]
                    out_pz = self.truez[rival]
                    out_pze = np.std(self.truez[index])
                    del rival

                # choose the nearest neighbor, the best color match
                if self.config.selection_mode == 1:
                    tx = np.where(MahalanobisDistance[index] == np.nanmin(MahalanobisDistance[index]))[0]
                    if len(tx) == 1:
                        rval = tx[0]
                    if len(tx) > 1:  # pragma: no cover
                        # if there's more than one best match (rare but possible), choose randomly
                        rval = rng.choice(tx, size=1, replace=False)[0]
                    out_pz = self.truez[index[rval]]
                    out_pze = np.std(self.truez[index])
                    del tx, rval

                # weight by how good the color match is and then choose randomly
                if self.config.selection_mode == 2:
                    tweights = float(1.00) / MahalanobisDistance[index]
                    weights = tweights / np.sum(tweights)
                    rival = rng.choice(index, size=1, replace=False, p=weights)[0]
                    out_pz = self.truez[rival]
                    out_pze = np.std(self.truez[index])
                    del tweights, weights, rival
                Ncm = len(index)
            else:
                # if there are not enough training galaxies within threshold distance, expand search:
                index2 = np.where((threshold > 0.00010) & (MahalanobisDistance > 0.00010))[0]
                if len(index2 > self.config.min_n):
                    tempMD = MahalanobisDistance[index2]
                    tempTZ = self.truez[index2]
                    # identify the nearest neighbors and use them as the CMNN subset
                    # create a sorted list of min_Nn
                    sx = np.argsort(tempMD)
                    new_MD = np.asarray(tempMD[sx[0:self.config.min_n]], dtype='float')
                    new_TZ = np.asarray(tempTZ[sx[0:self.config.min_n]], dtype='float')
                    if self.nondet_choice:
                        lim_DOF = deg_of_freedom
                    else:
                        tmpDOF = deg_of_freedom[index2]
                        new_DOF = np.asarray(tmpDOF[sx[0:self.config.min_n]], dtype='float')
                        lim_DOF = new_DOF[-1]
                        del new_DOF
                    del tempMD, tempTZ, sx
                    # calculate the new 'effective PPF' based on the most distant nearest neighbor
                    new_ppf_value = chi2.cdf(new_MD[-1], lim_DOF)
                    # inflate the photo-z error appropriately
                    temp = np.std(new_TZ)
                    out_pze = temp * (new_ppf_value / self.config.ppf_value)
                    del temp, new_ppf_value
                    if self.config.selection_mode == 0:
                        rval = rng.choice(self.config.min_n, size=1, replace=False)[0]
                        out_pz = new_TZ[rval]
                        del rval
                    if self.config.selection_mode == 1:
                        out_pz = new_TZ[0]
                    if self.config.selection_mode == 2:
                        tweights = float(1.00) / new_MD
                        weights = tweights / np.sum(tweights)
                        cx = rng.choice(self.config.min_n, size=1, replace=False, p=weights)[0]
                        out_pz = new_TZ[cx]
                        del tweights, weights, cx
                    del new_MD, new_TZ
                    Ncm = self.config.min_n
                else:  # pragma: no cover
                    # I think this would only happen if there are less than min_n gals in training set
                    out_pz = self.config.bad_redshift_val
                    out_pze = self.config.bad_redshift_err
                    Ncm = 0
            chunk_pz[ii] = out_pz
            chunk_pze[ii] = out_pze
            chunk_ncm[ii] = Ncm
        ens = qp.Ensemble(qp.stats.norm, data=dict(loc=np.expand_dims(chunk_pz, -1),
                                                   scale=np.expand_dims(chunk_pze, -1)))
        ens.set_ancil(dict(ncolors=chunk_colused, zmode=chunk_pz, Ncm=chunk_ncm))
        self._do_chunk_output(ens, start, end, first)
