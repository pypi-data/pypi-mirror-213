# rail_cmnn
RAIL interface to Melissa Graham's CMNN algorithm.  A slight modification of the original code found here: <br>
[dirac-institute/CMNN_Photoz_estimator](https://github.com/dirac-institute/CMNN_Photoz_Estimator)

See https://ui.adsabs.harvard.edu/abs/2018AJ....155....1G/abstract
for more details on the code
Any use of `rail_cmnn` in a paper or report should cite [Graham et al. (2018)](https://ui.adsabs.harvard.edu/abs/2018AJ....155....1G/abstract).

The current version of the code consists of a training stage, `Inform_CMNNPDF`, that computes colors for a set of training data and an estimation stage `CMNNPDF` that calculates the Mahalanobis distance to each training galaxy for each test galaxy. The mean value of this Guassian PDF can be estimated in one of three ways (see `selection mode` below), and the width is determined by the standard deviation of training galaxy redshifts within the threshold Mahalanobis distance.  Future implementation improvements may change the output format to include multiple Gaussians.

For the color calculation, there is an option for how to treat the "non-detections" in a band: the default choice is to ignore any colors that contain a non-detect magnitude and adjust the number of degrees of freedom in the Mahalanobis distance accordingly (this is how the CMNN algorithm was originally implemented). Or, if the configuration parameter `nondetect_replace` is set to `True` in `Inform_CMNNPDF`, the non-detected magnitudes will be replaced with the 1-sigma limiting magnitude in each band as supplied by the user via the `mag_limits` configuration parameter (or by the default 1-sigma limits if the user does not supply specific numbers). We have not done any exploration of the relative performance of these two choices, but note that there is not a significant performance difference in terms of runtime between the two methods.

`Inform_CMNNPDF` takes in a training data set and returns a model file that simply consists of the computed colors and color errors (magnitude errors added in quadrature) for that dataset, the model to be used in the `CMNNPDF` stage. A modification of the original CMNN algorithm, "nondetections" are now replaced by the 1-sigma limiting magnitudes and the non-detect magnitude errors replaced with a value of 1.0.  The config parameters that can be set by the user for `Inform_CMNNPDF` are:<br>
- `bands`: list of the band names that should be present in the input data.<br>
- `err_bands`: list of the magnitude error column names that should be present in the input data.<br>
- `redshift_col`: a string giving the name for the redshift column present in the input data.<br>
- `mag_limits`: a dictionary with keys that match those in `bands` and a float with the 1 sigma limiting magnitude for each band.<br>
- nondetect_val: float or `np.nan`, the value indicating a non-detection, which will be replaced by the values in `mag_limits`.<br>
- `nondetect_replace`: bool, if set to False (the default) this option ignores colors with non-detected values in the Mahalanobis distance calculation, with a corresponding drop in the degrees of freedom value. If set to True, the method will replace non-detections with the 1-sigma limiting magnitudes specified via `mag_limits` (or default 1-sigma limits if not supplied), and will use all colors in the Mahalanobis distance calculation.


The parameters that can be set via the `config_params` in `CMNNPDF` are described in brief below:<br>
- `bands`, `err_bands`, `redshift_col`, `mag_limits` are all the same as described above for `Inform_CMNNPDF.`<br>
- `ppf_value`: float, usually 0.68 or 0.95, which sets the value of the PPF used in the Mahalanobis distance calculation.<br>
- `selection_mode`: int, selects how the central value of the Gaussian PDF is calculated in the algorithm, if set to `0` randomly chooses from set within the Mahalanobis distance, if set to `1` chooses the nearest neighbor point, if set to `2` adds a distance weight to the random choice.<br>
- `min_n`: int, the minimum number of training galaxies to use.<br>
- `min_thresh`: float, the minimum threshold cutoff.  Values smaller than this threshold value will be ignored.<br>
- `min_dist`: float, the minimum Mahalanobis distance. Values smaller than this will be ignored.<br>
- `bad_redshift_val`: float, in the unlikely case that there are not enough training galaxies, this central redshift will be assigned to galaxies.<br>
- `bad_redshift_err`: float, in the unlikely case that there are not enough training galaxies, this Gaussian width will be assigned to galaxies.<br>
