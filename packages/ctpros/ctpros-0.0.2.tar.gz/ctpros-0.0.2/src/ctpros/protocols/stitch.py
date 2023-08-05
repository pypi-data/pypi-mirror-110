import numpy as np
import tkinter.filedialog
import copy, sys
import tqdm
import ctpros as ct
import itertools


def reorient(*imgs, tfm="average"):
    """
    Re-orients transformations to set all images to be (1) relative to the
    frame of the unmatched transformation matrix OR (2) relative to an
    average orientation of all of the matches transformations.

    Parameters:
        ctpros.ImgTemplate[] imgs = list of images to be considered for stitching
        ctpros.AffineTensor tfm = transform to re-orient to, defaults to the average orientation

    """
    if tfm is None:
        return ct.AffineTensor(3)
    elif type(tfm) is str and tfm == "average":  # calculate tfm as average transform
        prod = ct.AffineTensor(3)
        affines = [img.affine.copy() for img in imgs]
        [affine.scale(*(1 / affine.scale())) for affine in affines]
        [prod.affine(img.affine) for img in imgs]
        avg_rot = prod.rotate() / len(imgs)
        avg_trans = prod.translate() / len(imgs)
        tfm = ct.AffineTensor(3).rotate(*avg_rot).translate(*avg_trans)

    # calculates difference from the image transforms to the reference transform
    affine_diff = tfm.copy().inv()

    return affine_diff


def define_voi(imgs, tfm):
    """
    Identifies the volume of interest to be sampled.

    - Calculates the minimum and maximum physical coordinates of an image
    - Sets the minimum value as the sampling origin and difference as the size to be sampled
      at a rate of the affine scaling of the first image in the list

    """
    modified_tfms = [img.affine.copy().affine(tfm) for img in imgs]
    shapes = [img.shape for img in imgs]

    for i, (shape, modified_tfm) in enumerate(zip(shapes, modified_tfms)):
        index_bounds = np.array(
            [
                [0, 0, 0],
                [shape[0] - 1, 0, 0],
                [0, shape[1] - 1, 0],
                [0, 0, shape[2] - 1],
                [shape[0] - 1, shape[1] - 1, 0],
                [shape[0] - 1, 0, shape[2] - 1],
                [0, shape[1] - 1, shape[2] - 1],
                [shape[0] - 1, shape[1] - 1, shape[2] - 1],
            ]
        ).T
        physical_bounds = modified_tfm.dot(index_bounds)

        if not i:  # on first iteration assign
            minpos = physical_bounds.min(1)
            maxpos = physical_bounds.max(1)
        else:  # otherwise update
            minpos[:] = np.minimum(minpos, physical_bounds.min(1))
            maxpos[:] = np.maximum(maxpos, physical_bounds.max(1))

    pos = minpos
    elsize = imgs[0].affine.scale()
    shape = (maxpos - minpos + 1) // elsize + ((maxpos - minpos + 1) % elsize).astype(
        bool
    )
    voi = ct.VOI(pos=pos, shape=shape, elsize=elsize)

    return voi


def resampler(imgs, affine_diff, voi, *, precision="single"):
    """
    Resamples the images within their physical bounds with a given image resolution.

    """
    # loaded_imgs = [img for img in imgs if img.nbytes]  # to be re-loaded after stitching
    # [img.clear() for img in imgs[1:]]

    stitched_img = type(imgs[0])(tuple(voi.shape), dtype=precision)
    stitched_img[:] = 0

    coeff_img = type(imgs[0])(tuple(voi.shape), dtype=np.half)
    coeff_img[:] = 0

    for img in imgs:
        try:
            img.load()
            loaded = True
        except:
            loaded = False
        np.add(
            img.transform.affine(affine_diff, voi, inplace=False),
            stitched_img,
            out=stitched_img,
        )
        if loaded:
            img.clear()

        ones = ct.NDArray(img.shape, dtype="single", verbosity=False)
        ones.affine.affine(img.affine)
        ones[:] = 1
        np.add(
            ones.transform.affine(affine_diff, voi, inplace=False),
            coeff_img,
            out=coeff_img,
        )
        ones.clear()

    stitched_img[coeff_img > 1] /= coeff_img[coeff_img > 1]
    return stitched_img
    #     def sampleimg(i):
    #         stitchedimg[i]+=myimg.transform_affine(
    #             affine=gen.Orientation(3).update("translating",-step*i),
    #             ndspace=samplespace,
    #             elsizes=resolution,
    #             interpolation="linear",
    #             outofbounds="constant",)[0]
    #     if verbose:
    #         for i in tqdm.tqdm(myrange, ascii=True, desc=myimg.filename):
    #             sampleimg(i)
    #     else:
    #         for i in myrange:
    #             sampleimg(i)

    #     myimg.orientation.update("translating",step*stitchedimg.shape[0])
    #     myimg.resize(0,refcheck=False)

    # coeffimg = img.NDImg(ndimg=imgs[0],shape=stitchedimg[i].shape,dtype=np.single)
    # myones =
    # def normalizeimg(i):
    #     coeffimg[:] = 0
    #     for myimg in imgs:
    #         myones =
    #         coeffimg+=myones.transform_affine(
    #             affine=gen.Orientation(3).update("translating",-step*i),
    #             ndspace=samplespace,
    #             elsizes=resolution,
    #             interpolation="linear",
    #             outofbounds="constant",)[0]

    # if verbose:
    #     for i in tqdm.tqdm(myrange,ascii=True,desc="Normalizing"):
    #         normalizeimg(i)
    # else:
    #     for i in myrange:
    #         normalizeimg(i)

    # stitchedimg[coeffimg > 1] /= coeffimg[coeffimg > 1]
    # stitchedimg = stitchedimg.astype(np.int16)
    # return stitchedimg


def stitcher(*imgs, tfm="average", precision="single"):
    """
    Stitches images together based on their affine relationships.

    Parameters:
        ctpros.ImgTemplate[] imgs = list of images to be considered for stitching
        tfm ctpros.AffineTensor tfm = transform to be resampled onto

    """
    affine_diff = reorient(*imgs, tfm=tfm)
    voi = define_voi(imgs, affine_diff)
    stitched_img = resampler(imgs, affine_diff, voi, precision=precision)
    return stitched_img


def main(*argv):
    if imgfiles is None or transformfiles is None:
        return None

    datachecked = imgchecker(imgs, transformfiles)
    if not datachecked:
        print("Not enough information. Missing or redundant .AIM or .tfm files.")
        return None
    imgfiles = [arg for arg in argv if ".tfm" not in arg]
    tfmfiles = [arg for arg in argv if ".tfm" in arg]
    imgs = [ct.ImgTemplate(imgfile) for imgfile in imgfiles]
    tfms = [ct.AffineTensor(tfmfile) for tfmfile in tfmfiles]

    stitcher(imgs, tfms)


if __name__ == "__main__":
    main(*sys.argv[1:])
