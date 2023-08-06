# PyFeats

Open-source software for image feature extraction

A collection of python functions for feature extraction. The features are calculated inside a region-of-interest (ROI) and not for the whole image: the image is actually a polygon.

## 1. Install through pip

Install using the following command:

```console
pip install pyfeats
```

Use calling:

```python
import pyfeats
```

## 2. Features

### 2.1 Textural Features
1. First Order Statistics/Statistical Features (FOS/SF)
2. Gray Level Co-occurence Matrix (GLCM/SGLDM)
3. Gray Level Difference Statistics (GLDS)
4. Neighborhood Gray Tone Difference Matrix (NGTDM)
5. Statistical Feature Matrix (SFM)
6. Law's Texture Energy Measures (LTE/TEM)
7. Fractal Dimension Texture Analysis (FDTA)
8. Gray Level Run Length Matrix (GLRLM)
9. Fourier Power Spectrum (FPS)
10. Shape Parameters
11. Gray Level Size Zone Matrix (GLSZM)
12. Higher Order Spectra (HOS)
13. Local Binary Pattern (LPB)

### 2.2 Morphological Features
1. Grayscale Morphological Analysis
2. Multilevel Binary Morphological Analysis

### 2.3 Histogram Based Features
1. Histogram
2. Multi-region histogram
3. Correlogram

### 2.4 Multi-scale Features
1. Fractal Dimension Texture Analysis (FDTA)
2. Amplitude Modulation – Frequency Modulation (AM-FM)
3. Discrete Wavelet Transform (DWT)
4. Stationary Wavelet Transform (SWT)
5. Wavelet Packets (WP)
6. Gabor Transform (GT)

### 2.5 Other Features
1. Zernikes’ Moments
2. Hu’s Moments
3. Threshold Adjacency Matrix (TAS)
4. Histogram of Oriented Gradients (HOG)


## 3. How to use each feature set
For the following sections, assume
* _f_ is a grayscale image as a numpy ndarray, 
* _mask_ is an image as a numpy ndarray but with 2 values: 0 (zero) and 1 (one) with 1 indicating the ROI, where the features shall be calculated (values outside ROI are ignored),
* _perimeter_ is like _mask_ but indicates the perimeter of the ROI. 

### 3.1 Textural Features
#### 3.1.1 First Order Statistics/Statistical Features (FOS/SF)
First Order Statistics (FOS) are calculated from the histogram of the image which is the empirical probability density function for single pixels. The FOS features are the following:  1) mean, 2) standard deviation, 3) median, 4) mode, 5) skewnewss, 6) kurtosis, 7) energy, 8) entropy, 9) minimal gray level, 10) maximal gray leve, 11) coefficient of variation, 12,13,14,15) percentiles (10, 25, 50, 75, 90) and 16) histogram width.
```python
features, labels = pyfeats.fos(f, mask)
```
#### 3.1.2 Gray Level Co-occurence Matrix (GLCM/SGLDM)
The Gray Level Co-occurrence Matrix (GLCM) as proposed by Haralick are based on the estimation of the second-order joint conditional probability density functions. The GLGLCM features are the following:  1) angular second moment, 2) contrast, 3) correlation, 4) sum of squares: variance, 5) inverse difference moment, 6) sum average, 7) sum variance, 8) sum entropy, 9) entropy, 10) difference variance, 11) difference entropy, 12,13) information measures of correlation. For each feature, the mean values and the range of values are computed, and are used as two different features sets.
```python
features_mean, features_range, labels_mean, labels_range = pyfeats.glcm_features(f, ignore_zeros=True)
```
#### 3.1.3 Gray Level Difference Statistics (GLDS)
The Gray Level Difference Statistics (GLDS) algorithm uses first order statistics of local property values based on absolute differences between pairs of gray levels or of average gray levels in order to extract texture measures. The GLDS features are the following:  1) homogeneity, 2) contrast, 3) energy, 4) entropy, 5) mean.
```python
features, labels = pyfeats.glds_features(f, mask, Dx=[0,1,1,1], Dy=[1,1,0,-1])
```
#### 3.1.4 Neighborhood Gray Tone Difference Matrix (NGTDM)
Neighbourhood Gray Tone Difference Matrix (NDTDM) corresponds to visual properties of texture. The NGTDM features are the following:  1) coarseness, 2) contrast, 3) busyness, 4) complexity, 5) strength.
```python
features, labels = pyfeats.ngtdm_features(f, mask, d=1)
```
#### 3.1.5 Statistical Feature Matrix (SFM)
The Statistical Feature Matrix measures the statistical properties of pixel pairs at several distances within an image which are used for statistical analysis. The SFM features are the following: 1) coarseness, 2) contrast, 3) periodicity, 4) roughness.
```python
features, labels = pyfeats.sfm_features(f, mask, Lr=4, Lc=4)
```
#### 3.1.6 Law's Texture Energy Measures (LTE/TEM)
Law’s texture Energy Measures, are derived from three simple vectors of length 3. If these vectors are convolved with themselves, new vectors of length 5 are obtained. By further self-convolution, new vectors of length 7 are obtained. If the column vectors of length l are multiplied by row vectors of the same length, Laws l×l masks are obtained. In order to extract texture features from an image, these masks are convoluted with the image, and the statistics (e.g., energy) of the resulting image are used to describe texture: 1) texture energy from LL kernel, 2) texture energy from EE kernel, 3) texture energy from SS kernel, 4) average texture energy from LE and EL kernels, 5) average texture energy from ES and SE kernels, 6) average texture energy from LS and SL kernels.
```python
features, labels = pyfeats.lte_measures(f, mask, l=7)
```
#### 3.1.7 Fractal Dimension Texture Analysis (FDTA)
Fractal Dimension Texture Analysis (FDTA)  is based on the Fractional Brownian Motion (FBM) Model. The FBM model is used to describe the roughness of nature surfaces. It regards naturally occurring surfaces as the end result of random walks. Such random walks are basic physical processes in our universe. One of the most important parameters to represent a fractal surface is the fractal dimension. A simpler method is to estimate the H parameter (Hurst coefficient). If the image is seen under different resolutions, then the multiresolution fractal (MF) feature vector is obtained.
```python
h, labels = pyfeats.fdta(f, mask, s=3)
```
#### 3.1.8 Gray Level Run Length Matrix (GLRLM)
 A gray level run is a set of consecutive, collinear picture points having the same gray level value. The length of the run is the number of picture points in the run. The GLRLM features are the following: 1) short run emphasis, 2) long run emphasis, 3) gray level non-uniformity, 4) run length non-uniformity, 5) run percentage, 6) low gray level run emphasis, 7) high gray level run emphasis, 8) short low gray level emphasis, 9) short run high gray level emphasis, 10) long run low gray level emphasis, 11) long run high level emphasis.
```python
features, labels = pyfeats.glrlm_features(f, mask, Ng=256)
```
#### 3.1.9 Fourier Power Spectrum (FPS)
For digital pictures, instead of the continuous Fourier transform, one uses the discrete transform. The standard set of texture features based on a ring-shaped samples of the discrete Fourier power spectrum are of the form. Similarly, the features based on a wedge-shaped samples are of the form.
The FPS features are the following: 1) radial sum, 2) angular sum
```python
features, labels = pyfeats.fps(f, mask)
```
#### 3.1.10 Shape Parameters
Shape parameters consists of the following features: 1) x-coordinate maximum length, 2) y-coordinate maximum length, 3) area, 4) perimeter, 5) perimeter2/area
```python
features, labels = pyfeats.shape_parameters(f, mask, perimeter, pixels_per_mm2=1)
```
#### 3.1.11 Gray Level Size Zone Matrix (GLSZM)
Gray Level Size Zone Matrix (GLSZM) quantifies gray level zones in an image. A gray level zone is defined as the number of connected voxels that share the same gray level intensity. A voxel is considered connected if the distance is 1 according to the infinity norm (26-connected region in a 3D, 8-connected region in 2D). The GLSZM features are the following: 1) small zone emphasis, 2) large zone emphasis, 3) gray level non-uniformity, 4) zone-size non-uniformity, 5) zone percentage, 6) low gray level zone emphasis, 7) high gray level zone emphasis, 8) small zone low gray level emphasis, 9) small zone high gray level emphasis, 10) large zone low gray level emphasis, 11) large zone high gray level emphasis, 12 gray level variance, 13) zone-size variance, 14) zone-size entropy.
```python
features, labels = pyfeats.glszm_features(f, mask, connectivity=1)
```
#### 3.1.12 Higher Order Spectra (HOS)
Radon transform transforms two dimensional images with lines into a domain of possible line parameters, where each line in the image will give a peak positioned at the corresponding line parameters. Hence, the lines of the images are transformed into the points in the Radon domain. High Order Spectra (HOS) are spectral components of higher moments. The bispectrum, of a signal is the Fourier transform (FT) of the third order correlation of the signal (also known as the third order cumulant function). The bispectrum, is a complex-valued function of two frequencies. The bispectrum which is the product of three Fourier coefficients, exhibits symmetry and was computed in the non-redundant region. The extracted feature is the entropy 1.
```python
features, labels = pyfeats.hos_features(f, th=[135,140])
```
#### 3.1.13 Local Binary Pattern (LPB)
Local Binary Pattern (LBP), a robust and efficient texture descriptor, was first presented by Ojala. The LBP feature vector, in its simplest form, is determined using the following method: A circular neighbourhood is considered around a pixel. P points are chosen on the circumference of the circle with radius R such that they are all equidistant from the centre pixel. . These P points are converted into a circular bit-stream of 0s and 1s according to whether the gray value of the pixel is less than or greater than the gray value of the centre pixel. Ojala et al. (2002) introduced the concept of uniformity in texture analysis. The uniform fundamental patterns have a uniform circular structure that contains very few spatial transitions U (number of spatial bitwise 0/1 transitions). In this work, a rotation invariant measure using uniformity measure U was calculated. Only patterns with U less than 2 were assigned the LBP code i.e., if the number of bit transitions in the circular bit-stream is less than or equal to 2, the centre pixel was labelled as uniform. Energy and entropy of the LBP image, constructed over different scales are used as feature descriptors.
```python
features, labels = pyfeats.lbp_features(f, mask, P=[8,16,24], R=[1,2,3])
```

### 3.2 Morphological Features
#### 3.2.1 Gray-scale Morphological Analysis
In multilevel binary morphological analysis different components are extracted and investigated for their geometric properties. Three binary images are generated by thresholding. Here, binary image outputs are represented as sets of image coordinates where image intensity meets the threshold criteria. Overall, this multilevel decomposition is closely related to a three-level quantization of the original image intensity.  For each binary image the pattern spectrum is calculated. The Grayscale Morphological Features are the following: 1) mean cumulative distribution functions (CDF) and 2) mean probability density functions (PDF) of the pattern spectra  using the cross $"+"$ as a structural element of the grayscale image.
```python
pdf, cdf = pyfeats.grayscale_morphology_features(f, N)
```
#### 3.2.2 Multilevel Binary Morphological Analysis
Same as above but with grayscale image. The difference lies in the calculation of the pattern spectrum.
```python
pdf_L, pdf_M, pdf_H, cdf_L, cdf_M, cdf_H = pyfeats.multilevel_binary_morphology_features(img, mask, N=30, thresholds=[25, 50]):
```

### 3.3 Histogram Based Features
#### 3.3.1 Histogram
Histogram: The grey level histogram of the ROI of the image.
```python
H, labels = pyfeats.histogram(f, mask, bins=32)
```
#### 3.3.2 Multi-region histogram
A number of equidistant ROIs are identified by eroding the image outline by a factor based on the image size. The histogram is computed for each one of the regions as described above
```python
features, labels = pyfeats.multiregion_histogram(f, mask, bins, num_eros=3, square_size=3)
```
#### 3.3.3 Correlogram
Correlograms are histograms, which measure not only statistics about the features of the image, but also consider the spatial distribution of these features. In this work two correlograms are implemented for the ROI of the  image:

* based on the distance of the distribution of the pixels’ gray level values from the centre of the image, and
* based on their angle of distribution.

For each pixel the distance and the angle from the image centre is calculated and for all pixels with the same distance or angle their histograms are computed. In order to make the comparison between images of different sizes feasible, the distance correlograms is normalized. The angle of the correlogram is allowed to vary among possible values starting from the left middle of the image and moving clockwise. The resulting correlograms are matrices.
```python
Hd, Ht, labels = pyfeats.correlogram(f, mask, bins_digitize=32, bins_hist=32, flatten=True)
```

### 3.4 Multi-scale Features
#### 3.4.1 Fractal Dimension Texture Analysis (FDTA)
See 3.1.7.
```python
h, labels = pyfeats.fdta(f, mask, s=3)
```
#### 3.4.2 Amplitude Modulation – Frequency Modulation (AM-FM)
We consider multi-scale Amplitude Modulation – Frequency Modulation (AM-FM) representations, under least-square approximations, for images. For each image an instantaneous amplitude (IA), an the instantaneous phase (IP) and an instantaneous frequency (IF) is calculated for a specific component. Given the input discrete image, we first apply the Hilbert transform to form a 2D extension of the 1D analytic signal. The result is processed through a collection of bandpass filters with the desired scale. Each processing block will produce the IA, the IP and the IF. The AM-FM features are the following: Histogram of the 1) low, 2) medium, 3) high and 4) dc reconstructed images.
```python
features, labels = pyfeats.amfm_features(f, bins=32)
```
#### 3.4.3 Discrete Wavelet Transform (DWT)
The Discrete Wavelet Transform (DWT) of a signal is defined as its inner product with a family of functions. For images, i.e., 2-D signals, the 2-D DWT can be used. This consists of a DWT on the rows of the image and a DWT on the columns of the resulting image. The result of each DWT is followed by down sampling on the columns and rows, respectively. The decomposition of the image yields four sub-images for every level. Each approximation sub-image is decomposed into four sub images named approximation, detail-horizontal, detail-vertical, and detail-diagonal sub-image respectively. Each detail sub-image is the result of a convolution with two half-band filters. The DWT features are the following: 1) mean and 2) standard deviation of the absolute value of detail sub-images of the DWT.
```python
features, labels = pyfeats.dwt_features(f, mask, wavelet='bior3.3', levels=3)
```
#### 3.4.4 Stationary Wavelet Transform (SWT)
The 2-D Stationary Wavelet Transform (SWT) is similar to the 2-D DWT, but no down sampling is performed. Instead, up sampling of the low-pass and high-pass filters is carried out. The SWT features are the following: 1) mean and 2) standard deviation of the absolute value of detail sub-images of the SWT.
```python
features, labels = pyfeats.swt_features(f, mask, wavelet='bior3.3', levels=3)
```
#### 3.4.5 Wavelet Packets (WP)
The 2-D Wavelet Packets (WP) decomposition is a simple modification of the 2-D DWT, which offers a richer space-frequency representation. The first level of analysis is the same as that of the 2-D DWT. The second, as well as all subsequent levels of analysis consist of decomposing every sub image, rather than only the approximation sub image, into four new sub images. The WP features are the following: 1) mean and 2) standard deviation of the absolute value of detail sub-images of the Wavelet Decomposition.
```python
features, labels = pyfeats.wp_features(f, mask, wavelet='cof1', maxlevel=3) 
```
#### 3.4.6 Gabor Transform (GT)
The Gabor Transform (GT) of an image consists in convolving that image with the Gabor function, i.e., a sinusoidal plane wave of a certain frequency and orientation modulated by a Gaussian envelope. Frequency and orientation representations of Gabor filters are similar to those of the human visual system, rendering them appropriate for texture segmentation and classification. The GT features are the following: 1) mean and 2) standard deviation of the absolute value of detail sub-images of the GT of the image.
```python
features, labels = pyfeats.gt_features(f, mask, deg=4, freq=[0.05, 0.4])
```

### 3.5 Other Features
#### 3.5.1 Zernikes’ Moments
In image processing, computer vision and related fields, an image moment is a certain particular weighted average (moment) of the image pixels' intensities, or a function of such moments, usually chosen to have some attractive property or interpretation. 
Zernikes’ moment is a kind of orthogonal complex moments and its kernel is a set of Zernike complete orthogonal polynomials defined over the interior of the unit disc in the polar coordinates space. Zernike's Moments are: 1-25) orthogonal moments invariants with respect to translation.
```python
features, labels = pyfeats.zernikes_moments(f, radius=9)
```
#### 3.5.2 Hu’s Moments
In image processing, computer vision and related fields, an image moment is a certain particular weighted average (moment) of the image pixels' intensities, or a function of such moments, usually chosen to have some attractive property or interpretation. 
Hu’s Moments are: 1-7) moments invariants with respect to translation, scale, and rotation.
```python
features, labels = pyfeats.hu_moments(f)
```
#### 3.5.3 Threshold Adjacency Matrix (TAS)
```python
features, labels = pyfeats.tas_features(f)
```
#### 3.5.4 Histogram of Oriented Gradients (HOG)
```python
fd, labels = pyfeats.hog_features(f, ppc=8, cpb=3)
```