import SimpleITK as sitk
import os
import matplotlib.pyplot as plt
import numpy as np
#import tracemalloc
#tracemalloc.start()

plt.rcParams['figure.figsize'] = [8, 6]
plt.rcParams['figure.dpi'] = 100
plt.rcParams["savefig.format"] = 'tif'

_path = "C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/data/foxp2/"

#sample_path = "C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/data/sample/"
sample_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/data/foxp2/'
#nrrd_path = "C:/Users/keshavgubbi/Desktop/filestructure/mocktransf/PmCH1/individual_transformed"
#outpath = "C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/foxp2/renyi/"
outpath = 'C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/PmCH1/multi_otsu/'


def threshold_using_Renyi_Filter(img):
    # image = sitk.ReadImage(os.path.join(path, filename))
    #print(os.path.join(sample_path, filename))
    image = sitk.ReadImage(os.path.join(sample_path, filename))
    # image_details(image)
    print("place 1")
    renyi_filter = sitk.RenyiEntropyThresholdImageFilter()
    print(renyi_filter.GetNumberOfHistogramBins())
    renyi_filter.SetInsideValue(0)
    renyi_filter.SetOutsideValue(1)
    renyi_image = renyi_filter.Execute(image)

    print("renyi threshold:", renyi_filter.GetThreshold())
    renyi_image = np.reshape(renyi_image, (974, 597))

    # **Inline Display of Image**
    fig = plt.figure(edgecolor='k')
    ax = fig.add_axes([0, 0, 1, 1])
    plt.axis("Off")
    # plt.title('renyi_{}'.format(img))
    # plt.imshow(renyi_image, cmap='gray')
    # plt.show()

    # **Saving Image**
    print("saving")
    plt.imsave("C:/Users/keshavgubbi/Desktop/ATLAS/S5-Binarizing/Output/foxp2/renyi/renyi_{}.jpg".format(img), renyi_image, cmap="gray")

    return renyi_image


for filename in os.listdir(sample_path):
    if filename.endswith(".nrrd") or filename.endswith(".tif"):
        #print(os.path.join(sample_path, filename))
        renyi_thresh_image = threshold_using_Renyi_Filter(filename)
        #pass

#snapshot = tracemalloc.take_snapshot()
#top_stats = snapshot.statistics('lineno')

#print("[ Top 10 ]")
#for stat in top_stats[:10]:
#    print(stat)