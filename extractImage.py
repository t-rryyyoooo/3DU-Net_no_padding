import argparse
from pathlib import Path
import SimpleITK as sitk
from extractor import extractor as extor
from functions import getImageWithMeta

args = None

def ParseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("imageDirectory", help="$HOME/Desktop/data/kits19/case_00000")
    parser.add_argument("saveSlicePath", help="$HOME/Desktop/data/slice/hist_0.0", default=None)
    parser.add_argument("--patchSize", help="28-44-44", default="28-44-44")
    parser.add_argument("--slide", nargs=3, help="2 2 2", type=int)
    parser.add_argument("--padding", nargs=3, type=int, default=None)
    parser.add_argument("--only_mask",action="store_true" )

    args = parser.parse_args()
    return args

def main(args):
    labelFile = Path(args.imageDirectory) / 'segmentation.nii.gz'
    imageFile = Path(args.imageDirectory) / 'imaging.nii.gz'

    """ Read image and label. """
    label = sitk.ReadImage(str(labelFile))
    image = sitk.ReadImage(str(imageFile))

    if args.slide is not None:
        slide = args.slide
    else:
        slide = None
    
    if args.padding is not None:
        padding = args.padding
    else:
        padding = None

    extractor = extor(
            image = image, 
            label = label,
            patch_size = args.patchSize, 
            slide = slide, 
            padding = padding,
            only_mask = args.only_mask
            )

    extractor.execute()
    patientID = args.imageDirectory.split("/")[-1]
    #extractor.save(args.saveSlicePath, patientID)
    """ Test """
    i, l = extractor.output("Array")
    ll = extractor.restore(l)
    sitk.WriteImage(ll, "test/test.mha", True)


if __name__ == '__main__':
    args = ParseArgs()
    main(args)
