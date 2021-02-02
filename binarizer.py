import SimpleITK as sitk
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.io import imread, imshow
from skimage.util import img_as_ubyte
from skimage.filters.rank import entropy
from skimage.color import rgb2gray

# TODO: Fix the dimensions of images by making it generalised
# TODO: Create separate function for saving images
# TODO: Figure out a nice way to display inline images and plots in Pycharm
# TODO: Redo Renyi function by modifying Max Entropy Function
# TODO: Add IsoData, Huang, Li and sk image entropy filters as separate functions
# TODO: Add ThresholdSegmentationLevelSetImageFilter as separate function
# TODO: Try a combination of couple of these filters. or to create your own class of filters and functions
# Done: Huang and Li is done. Not useful. Shanbag is done, could be quite useful.
# Done: Combo filters done.


plt.rcParams['figure.figsize'] = [8, 6]
plt.rcParams['figure.dpi'] = 100
plt.rcParams["savefig.format"] = 'tif'

_path = "C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/data/foxp2/"

# sample_path = "C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/data/sample/"
sample_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/data/foxp2/'
# nrrd_path = "C:/Users/keshavgubbi/Desktop/filestructure/mocktransf/PmCH1/individual_transformed"
# outpath = "C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/foxp2/renyi/"
# outpath = 'C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/{}/'.format(line)
foxp2_outpath = 'C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/foxp2/'


def image_details(image):
    print("**********************")
    print("Size:", image.GetSize())
    print("PixelIDType:", image.GetPixelIDTypeAsString())
    print("Voxel Size:", image.GetSpacing())


"""
def save_image(seg_image):
    print("saving")
    fig = plt.figure(edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])
    plt.axis("Off")

    # plt.imsave("C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/multiotsu_{}.tif".format(img),
    #           multi_otsu_segmented_image, cmap="gray")
    if not os.path.exists(outpath):
        print("path doesn't exist. Creating now....")
        os.makedirs(outpath)
        plt.imsave(os.path.join(outpath, "{}".format(seg_image) + ".tiff"), seg_image, cmap="gray")
"""


def threshold_using_OtsuFilter(img):
    image = sitk.ReadImage(os.path.join(sample_path, filename))
    # image_details(image)
    w, h = image.GetSize()

    # global otsu filter
    otsu_filter = sitk.OtsuThresholdImageFilter()
    otsu_filter.SetInsideValue(0)
    otsu_filter.SetOutsideValue(1)
    otsu_segmented_image = otsu_filter.Execute(image)
    otsu_segmented_image = np.reshape(otsu_segmented_image, (h, w))

    # plt.title('otsu_{}'.format(img))
    # plt.imshow(otsu_segmented_image, cmap='gray')
    # plt.savefig(os.path.join(outpath, 'otsu_{}'.format(img)), dpi=100)

    ax.axis("Off")
    # plt.show()
    plt.imsave(os.path.join(outpath, "otsu_{}".format(img) + ".tiff"), otsu_segmented_image, cmap="gray")

    return otsu_segmented_image


def threshold_using_multiOtsu_Filter(img):
    print(os.path.join(sample_path, filename))
    image = sitk.ReadImage(os.path.join(sample_path, filename))
    # image_details(image)
    w, h = image.GetSize()

    multi_otsu_filter = sitk.OtsuMultipleThresholdsImageFilter()
    multi_otsu_segmented_image = multi_otsu_filter.Execute(image)
    multi_otsu_segmented_image = np.reshape(multi_otsu_segmented_image, (h, w))

    # **Inline Display of Image**
    fig = plt.figure(edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("Off")

    # plt.title('multiotsu_{}'.format(img))
    # plt.imshow(multi_otsu_segmented_image, cmap='gray')
    # plt.show()
    # print("saving")

    # plt.imsave("C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/multiotsu_{}.tif".format(img),
    #           multi_otsu_segmented_image, cmap="gray")
    plt.imsave(os.path.join(outpath, "multi_otsu_{}".format(img) + ".tiff"), multi_otsu_segmented_image, cmap="gray")

    return multi_otsu_segmented_image


def threshold_using_Renyi_Filter(img):
    # image = sitk.ReadImage(os.path.join(path, filename))
    print(os.path.join(sample_path, filename))
    image = sitk.ReadImage(os.path.join(sample_path, filename))
    # image_details(image)
    w, h = image.GetSize()

    renyi_filter = sitk.RenyiEntropyThresholdImageFilter()
    renyi_filter.SetInsideValue(0)
    renyi_filter.SetOutsideValue(1)
    renyi_image = renyi_filter.Execute(image)

    print("renyi threshold:", renyi_filter.GetThreshold())
    renyi_image = np.reshape(renyi_image, (h, w))

    # **Inline Display of Image**
    fig = plt.figure(edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("Off")
    # plt.title('renyi_{}'.format(img))
    # plt.imshow(renyi_image, cmap='gray')
    # plt.show()

    # **Saving Image**
    print("saving")
    # plt.imsave("C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/foxp2/renyi/renyi_{}.jpg".format(img),
    #           renyi_image,cmap="gray")
    plt.imsave(os.path.join(outpath, "renyi_{}".format(img) + ".tiff"), renyi_image, cmap="gray")
    return renyi_image


def threshold_using_Yen_Filter(img):
    print(os.path.join(sample_path, filename))
    image = sitk.ReadImage(os.path.join(sample_path, filename))
    # image_details(image)
    w, h = image.GetSize()

    yen_filter = sitk.YenThresholdImageFilter()
    yen_filter.SetInsideValue(0)
    yen_filter.SetOutsideValue(1)
    yen_filter_segmented_image = yen_filter.Execute(image)
    yen_filter_segmented_image = np.reshape(yen_filter_segmented_image, (h, w))
    print(" yen_filter Threshold:", yen_filter.GetThreshold())

    # **Inline Display of Image**
    fig = plt.figure(edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("Off")
    # plt.title('yen_{}'.format(img))
    # plt.imshow(yen_filter_segmented_image, cmap='gray')
    # plt.show()
    # print("saving")
    plt.imsave(os.path.join(outpath, "yen_{}".format(img) + ".tiff"), yen_filter_segmented_image, cmap="gray")

    return yen_filter_segmented_image


def threshold_using_intermode_Filter(img):
    print(os.path.join(sample_path, filename))
    #image = sitk.ReadImage(os.path.join(sample_path, filename))
    image = cv2.imread(os.path.join(sample_path, filename), 0)
    # image_details(image)
    #w, h = image.GetSize()

    # smooth_filter = sitk.SmoothingRecursiveGaussianImageFilter()
    # print(dir(smooth_filter))
    # smooth_image = smooth_filter.Execute(image)

    Intermodes_filter = sitk.IntermodesThresholdImageFilter()
    Intermodes_filter.SetInsideValue(0)
    Intermodes_filter.SetOutsideValue(1)
    #Intermodes_filter.SetNumberOfHistogramBins(16)
    #print(dir(Intermodes_filter))

    # print(Intermodes_filter.GetMaximumSmoothingIterations())
    #Intermodes_filter.SetMaximumSmoothingIterations(1000000)
    image = cv2.equalizeHist(image)
    intermodes_segmented_image = Intermodes_filter.Execute(image)
    #intermodes_segmented_image = np.reshape(intermodes_segmented_image, (h, w))
    print("Threshold:", Intermodes_filter.GetThreshold())
    #print(Intermodes_filter.GetNumberOfThreads())
    #print(Intermodes_filter.GetNumberOfHistogramBins())
    #print(Intermodes_filter.GetMaskValue())

    # **Inline Display of Image**
    fig = plt.figure(edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("Off")

    # plt.imsave("C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/foxp2/intermode_{}.jpg".format(img),
    #           intermodes_filter_segmented_image, cmap="gray")
    plt.imsave(os.path.join(outpath, "intermode_{}".format(img) + ".tiff"), intermodes_segmented_image,
               cmap="gray")
    return intermodes_segmented_image


def threshold_using_MaxEntropy_Filter(img):
    print(os.path.join(sample_path, filename))
    image = sitk.ReadImage(os.path.join(sample_path, filename))
    # image_details(image)
    w, h = image.GetSize()

    MaxEntropy_filter = sitk.MaximumEntropyThresholdImageFilter()
    MaxEntropy_filter.SetInsideValue(0)
    MaxEntropy_filter.SetOutsideValue(1)
    maxentropy_filter_segmented_image = MaxEntropy_filter.Execute(image)
    maxentropy_image = np.reshape(maxentropy_filter_segmented_image, (h, w))
    print(" MaxEntropy_filter Threshold:", MaxEntropy_filter.GetThreshold())

    # **Inline Display of Image**
    fig = plt.figure(edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("Off")

    #plt.imsave("C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/MaxEntropy_{}.jpg".format(img),
    #           maxentropy_image, cmap="gray")
    plt.imsave(os.path.join(outpath, "max_entropy_{}".format(img) + ".tiff"), maxentropy_image, cmap="gray")

    return maxentropy_image


def threshold_using_li_filter(img):
    print(os.path.join(sample_path, filename))
    image = sitk.ReadImage(os.path.join(sample_path, filename))
    # image_details(image)
    w, h = image.GetSize()

    li_filter = sitk.LiThresholdImageFilter()
    li_filter.SetInsideValue(0)
    li_filter.SetOutsideValue(1)
    li_filter_segmented_image = li_filter.Execute(image)
    li_filter_image = np.reshape(li_filter_segmented_image, (h, w))
    print(" Li Threshold:", li_filter.GetThreshold())

    # **Inline Display of Image**
    fig = plt.figure(edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("Off")

    #plt.imsave("C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/Li_{}.jpg".format(img), li_filter_image,
    #           cmap="gray")
    plt.imsave(os.path.join(outpath, "max_entropy_{}".format(img) + ".tiff"), li_filter_image, cmap="gray")

    return li_filter_image


def threshold_using_shanbhag_filter(img):
    print(os.path.join(sample_path, filename))
    image = sitk.ReadImage(os.path.join(sample_path, filename))
    # image_details(image)
    w, h = image.GetSize()

    Shanbhag_filter = sitk.ShanbhagThresholdImageFilter()
    Shanbhag_filter.SetInsideValue(0)
    Shanbhag_filter.SetOutsideValue(1)
    Shanbhag_filter_segmented_image = Shanbhag_filter.Execute(image)
    Shanbhag_filter_segmented_image = np.reshape(Shanbhag_filter_segmented_image, (h, w))
    print(" Shanbhag Threshold:", Shanbhag_filter.GetThreshold())

    # **Inline Display of Image**
    fig = plt.figure(edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("Off")

    plt.imsave(os.path.join(outpath, "Shanbhag_{}".format(img) + ".tiff"), Shanbhag_filter_segmented_image, cmap="gray")

    return Shanbhag_filter_segmented_image


def threshold_using_combo_filter(img):
    print(os.path.join(sample_path, filename))
    image = sitk.ReadImage(os.path.join(sample_path, filename))
    # image_details(image)
    w, h = image.GetSize()

    Shanbhag_filter = sitk.ShanbhagThresholdImageFilter()
    Shanbhag_filter.SetInsideValue(0)
    Shanbhag_filter.SetOutsideValue(1)
    MaxEntropy_filter = sitk.MaximumEntropyThresholdImageFilter()
    MaxEntropy_filter.SetInsideValue(0)
    MaxEntropy_filter.SetOutsideValue(1)

    MaxEntropy_filter_image = MaxEntropy_filter.Execute(image)
    print(" MaxEntropy Threshold:", MaxEntropy_filter.GetThreshold())
    combo_segmented_image = Shanbhag_filter.Execute(MaxEntropy_filter_image)
    print(" Shanbhag Threshold:", Shanbhag_filter.GetThreshold())
    combo_segmented_image = np.reshape(combo_segmented_image, (h, w))

    # **Inline Display of Image**
    fig = plt.figure(edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("Off")

    plt.imsave(os.path.join(outpath, "Combo_{}".format(img) + ".tiff"), combo_segmented_image, cmap="gray")

    return combo_segmented_image


def threshold_using_combo1_filter(img):
    print(os.path.join(sample_path, filename))
    image = sitk.ReadImage(os.path.join(sample_path, filename))
    # image_details(image)
    w, h = image.GetSize()

    Shanbhag_filter = sitk.ShanbhagThresholdImageFilter()
    Shanbhag_filter.SetInsideValue(0)
    Shanbhag_filter.SetOutsideValue(1)
    Shanbhag_image = Shanbhag_filter.Execute(image)
    print(" Shanbhag Threshold:", Shanbhag_filter.GetThreshold())
    multi_otsu_filter = sitk.OtsuMultipleThresholdsImageFilter()
    combo1_segmented_image = multi_otsu_filter.Execute(Shanbhag_image)
    combo1_segmented_image = np.reshape(combo1_segmented_image, (h, w))

    # **Inline Display of Image**
    fig = plt.figure(edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("Off")

    plt.imsave(os.path.join(outpath, "Combo1_{}".format(img) + ".tiff"), combo1_segmented_image, cmap="gray")

    return combo1_segmented_image


def threshold_otsu_using_opencv(img):
    img = cv2.imread(img, 0)
    imgarray = np.asarray(img)
    # Otsu thresholding
    ret2, th2 = cv2.threshold(imgarray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # th2 is the thresholded image
    # plt.imshow(th2, cmap="gray")
    # plt.show()
    cv2.imwrite(os.path.join(outpath, "otsu_opencv_{}".format(img) + ".tiff"), th2)
    return th2


def threshold_using_adaptivemean_opencv(img):
    print(os.path.join(sample_path, filename))
    image = cv2.imread(os.path.join(sample_path, filename), 0)
    image = cv2.medianBlur(image, 5)
    #ret, th1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(image, 127, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    print("saving adaptive mean")
    plt.imsave("C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/Am_{}.jpg".format(img), th2, cmap="gray")
    return th2


def threshold_using_adaptivegaussian_opencv(img):
    print(os.path.join(sample_path, filename))
    image = cv2.imread(os.path.join(sample_path, filename), 0)
    image = cv2.medianBlur(image, 5)
    # ret, th1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    th3 = cv2.adaptiveThreshold(image, 127, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    print("saving adaptive gaussian")
    plt.imsave("C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/ag_{}.jpg".format(img), th3,
               cmap="gray")
    return th3


def threshold_clahe(img):
    print(os.path.join(sample_path, filename))
    image = cv2.imread(os.path.join(sample_path, filename), 0)
    equ = cv2.equalizeHist(image)
    #plt.hist(image.flat, bins=100, range=(0, 255))
    #plt.hist(equ.flat, bins=100, range=(0, 255))
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2, 2))
    clahe_image = clahe.apply(image)
    #plt.hist(clahe_image.flat, bins=100, range=(100, 255))
    plt.imsave(os.path.join(outpath, "clahe_{}".format(img) + ".tiff"), clahe_image, cmap="gray")
    return clahe_image



def threshold_sk_entropy(img):
    print(os.path.join(sample_path, filename))
    image = imread(os.path.join(sample_path, filename))
    image_gray = rgb2gray(image)
    entropy_image = entropy(image_gray, disk(10))
    plt.imsave(os.path.join(outpath, "sk_entropy_{}".format(img) + ".tiff"), entropy_image, cmap="gray")
    return entropy_image


# *********************
line_name = input("enter line_name:")

for filename in os.listdir(sample_path):
    if filename.endswith(".nrrd") or filename.endswith(".tif"):
        outpath = 'C:/Users/keshavgubbi/Desktop/test/Output/{}/'.format(line_name)
        #print(os.path.join(sample_path, filename))

        # opencv_thresh_image = threshold_otsu_using_OpenCV(filename)
        # otsu_thresh_image = threshold_using_OtsuFilter(filename)
        #multi_otsu_thresh_image = threshold_using_multiOtsu_Filter(filename)
        # renyi_thresh_image = threshold_using_Renyi_Filter(filename)
        # yen_filter_segmented_image = threshold_using_Yen_Filter(filename)
        #intermodes_filter_segmented_image = threshold_using_intermode_Filter(filename)
        # maxentropy_image = threshold_using_MaxEntropy_Filter(filename)
        #adaptive_mean_image = threshold_using_adaptivemean_opencv(filename)
        #adaptive_gaussian_image = threshold_using_adaptivegaussian_opencv(filename)
        # li_filter_image = threshold_using_li_filter(filename)
        # alternative_im_image = threshold_using_alternative_im(filename)
        # Shanbhag_filter_image = threshold_using_shanbhag_filter(filename)
        # combo_segmented_image = threshold_using_combo_filter(filename)
        combo1_segmented_image = threshold_using_combo1_filter(filename)
        #clahe_segmented_image = threshold_clahe(filename)
        #sk_entropy_image = threshold_sk_entropy(filename)
