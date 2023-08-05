import tkinter as tk
import time
import numpy as np

from . import backend
from . import tools
from .progressbar import LinkedIterator
from ... import img


class MainFrameMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.structure = {
            "File": self.file_structure(),
            "Classify": self.classify_structure(),
            "Filter": self.filter_structure(),
            "Generic": self.generic_structure(),
            "Numeric": self.numeric_structure(),
            "Register": self.register_structure(),
            "Transform": self.transform_structure(),
            "Protocols": self.protocol_structure(),
            "Help": self.help_structure(),
        }
        self.generate()
        self.master.config(menu=self)

    def generate(self):  # pragma: no cover
        """
        Generates the tkinter structured menubar with submenus down to two levels from dictionary structures.
        """
        self.submenus = {}
        for category, suboptions in self.structure.items():
            self.submenus[category] = {
                "menu": tk.Menu(self, tearoff=0),
                "criteria": lambda: True,
            }
            for label, (content, criteria) in suboptions.items():
                if type(content) == dict:
                    self.submenus[category][label] = {
                        "menu": tk.Menu(self.submenus[category]["menu"], tearoff=0),
                        "criteria": criteria,
                    }
                    self.submenus[category]["menu"].add_cascade(
                        label=label, menu=self.submenus[category][label]["menu"]
                    )
                    if not criteria():
                        self.submenus[category]["menu"].entryconfig(
                            label, state=tk.DISABLED
                        )

                    for sublabel, (command, criteria) in content.items():
                        self.submenus[category][label]["menu"].add_command(
                            label=sublabel, command=command
                        )
                        if not criteria():
                            self.submenus[category][label]["menu"].entryconfig(
                                sublabel, state=tk.DISABLED
                            )

                elif callable(content):
                    self.submenus[category]["menu"].add_command(
                        label=label, command=content
                    )
                    if not criteria():
                        self.submenus[category]["menu"].entryconfig(
                            label, state=tk.DISABLED
                        )
                elif "separator" in label.lower():
                    self.submenus[category]["menu"].add_separator()
            self.add_cascade(label=category, menu=self.submenus[category]["menu"])

    def lambdas(self, function, iterator, offset=0):
        """
        Generates iterative lambda's for buttons which have an indexed input for image reference.

        """
        mydict = dict(
            zip(
                [myimg.filename for myimg in iterator],
                [
                    (
                        (lambda i: (lambda: function(i + offset)))(i + offset),
                        self.criteria_enabled,
                    )
                    for i, _ in enumerate(iterator)
                ],
            )
        )
        return mydict

    def refresh(self):
        """
        Regenerates menu with updated criteria and image-specific dropdowns.

        """
        self.__init__(self.master)

    def criteria_enabled(self):
        return True

    # def criteria_disabled(self):
    #     return False

    def criteria_loadedimg(self):
        return self.master.get_selected_imgs()

    def criteria_twoloadedimgs(self):
        return self.master.get_selected_imgs()[:-1]

    # file

    def file_structure(self):
        """
        For standard button:
            struct = {"label":(function,criteria)}
        For dropdown button:
            struct = {"dropdownlabel":({[$standardbuttons]},criteria)}
        """
        mfm_file = {
            "Open image ...": (self.file_open_image, self.criteria_enabled),
            "Close image ...": (
                self.lambdas(self.file_close_image, self.master.imgs),
                self.criteria_loadedimg,
            ),
            "Close all images ...": (
                self.file_close_all_image,
                self.criteria_loadedimg,
            ),
            "Separator 1": (None, None),
            "Apply affine matrix ...": (
                self.lambdas(self.file_apply_affine, self.master.imgs),
                self.criteria_loadedimg,
            ),
            "Align affine matrix ...": (
                self.lambdas(self.file_align_affine, self.master.imgs),
                self.criteria_loadedimg,
            ),
            "Save affine matrix ...": (
                self.lambdas(self.file_save_affine, self.master.imgs),
                self.criteria_loadedimg,
            ),
            "Separator 2": (None, None),
            "Open VOI ...": (self.file_open_voi, self.criteria_loadedimg),
            "Save VOI ...": (self.file_save_voi, self.criteria_loadedimg),
            "Separator 3": (None, None),
            "Save VOI Crop ...": (
                self.lambdas(self.file_save_crop, self.master.get_selected_imgs()),
                self.criteria_loadedimg,
            ),
        }
        return mfm_file

    def file_open_image(self, *filenames):
        """
        Function associated to the "Open image" button.

        Either receives a list of filenames to be loaded into memory or opens a
        file dialog to request such.

        """
        if not filenames:  # pragma: no cover
            filenames = backend.gui_open(filetypes=img.supported_types)
        if not filenames:  # pragma: no cover
            return
        newimgs = [
            img.ImgTemplate(filename, verbosity=self.master.verbosity)
            for filename in filenames
        ]
        allfilenames = [myimg.filename for myimg in self.master.imgs + newimgs]
        if len(allfilenames) != len(set(allfilenames)):
            raise Exception(
                "Files which attempted to be loaded did not have unique names."
            )
        self.master.add_imgs(*newimgs)

    def file_close_image(self, index):
        """
        Function associated to the "Close image" button.

        Removes the image that is indexed by the given value.

        """

        myimg = self.master.imgs.pop(index)
        if myimg.filename in self.master.get_selected_imgnames():
            index = self.master.get_selected_imgnames().index(myimg.filename)
            self.master.selected_imgnames[index].set("None")
        if self.master.verbosity:  # pragma: no cover
            print("Removed " + myimg.filename + ".")
        self.master.refresh()

    def file_close_all_image(self):
        """
        Function associated to the "Close all images" button.

        Removes all loaded images.

        """
        for _ in range(len(self.master.imgs)):
            self.file_close_image(0)

    def file_apply_affine(self, index, affinename=None):
        """
        Applies an affine transformation to an images orientation.

        """
        if not affinename:  # pragma: no cover
            affinename = tk.filedialog.askopenfilename(filetypes="*.tfm")
        if not affinename:  # pragma: no cover
            return
        affine = img.AffineTensor(affinename)
        self.master.imgs[index].affine.affine(affine)
        self.master.imgframe.refresh()

    def file_align_affine(self, index, affinename=None):
        """
        Applies an affine transformation to an images orientation.

        """
        if not affinename:  # pragma: no cover
            affinename = tk.filedialog.askopenfilename(filetypes="*.tfm")
        if not affinename:  # pragma: no cover
            return
        affine = img.AffineTensor(affinename)
        self.master.imgs[index].affine.align(affine)
        self.master.imgframe.refresh()

    def file_save_affine(self, index, affinename=None):
        """
        Saves the affine tensor associated to the image at GUI's indexed slot.

        """
        if not affinename:  # pragma: no cover
            affinename = tk.filedialog.asksaveasfilename(
                filetypes=[("Affine Tensor", "*.tfm")]
            )
        if not affinename:  # pragma: no cover
            return
        affine = self.master.imgs[index].affine.copy()
        self.master.imgs[index].reset_affine()
        saved_affine = np.dot(affine, self.master.imgs[index].affine.inv())
        saved_affine.saveas(affinename)
        self.master.imgs[index].affine = affine

    def file_open_voi(self, filename=None):
        """
        Function associated to the "Open VOI" button.

        Reads in a binary VOI file.

        """
        if not filename:  # pragma: no cover
            filename = tk.filedialog.askopenfilename(
                filetypes=[("Volume of Interest", ".voi")]
            )
        if not filename:  # pragma: no cover
            return
        voi = img.VOI(filename)
        for field in ["pos", "shape", "elsize"]:
            for value, tkvar in zip(
                getattr(voi, field).ravel(), self.master.voi[field]
            ):
                tkvar.set(value)

    def file_save_voi(self, filename=None):
        """
        Function associated to the "Save VOI" button.

        Writes in a binary VOI file.

        """
        if not filename:  # pragma: no cover
            filename = tk.filedialog.asksaveasfilename(
                filetypes=[("Volume of Interest", ".voi")]
            )
        if not filename:  # pragma: no cover
            return
        self.master.get_selected_imgs()[0].voi.saveas(filename)

    def file_save_crop(self, index, newfilename=None):
        if not newfilename:
            newfilename = tk.filedialog.asksaveasfilename(filetypes=img.supported_types)
        if not newfilename:  # pragma: no cover
            return
        crop = self.master.get_selected_imgs()[index].transform.affine(inplace=False)
        view = crop.view(img.ImgTemplate._getsubclass(newfilename))
        view.saveas(newfilename)
        return view

    # classify

    def classify_structure(self):
        mfm_classify = {
            "Threshold": (
                self.classify_threshold,
                self.criteria_loadedimg,
            ),
            "Otsu - Global": (
                self.classify_otsu_global,
                self.criteria_loadedimg,
            ),
            "Separator 1": (None, None),
            "Canny Edges": (
                self.classify_canny_edges,
                self.criteria_loadedimg,
            ),
            "Separator 2": (None, None),
            "Invert Mask": (
                self.classify_inv,
                self.criteria_loadedimg,
            ),
        }
        return mfm_classify

    def classify_threshold(self):
        backend.Popup(
            self.master,
            "Otsu Global Thresholding",
            "classify.threshold",
            **{
                "val": (
                    "Raw Value",
                    (
                        (
                            backend.IntRangeEntry,
                            10000,
                            {"minval": 1, "maxval": 2 ** 16 - 1},
                        ),
                    ),
                ),
            }
        )

    def classify_otsu_global(self, *args, **kwargs):
        backend.Popup(
            self.master,
            "Otsu Global Thresholding",
            "classify.otsu_global",
            **{
                "n": (
                    "Number",
                    (
                        (
                            backend.IntRangeEntry,
                            1,
                            {"minval": 1, "maxval": 255},
                        ),
                    ),
                ),
            }
        )

    def classify_canny_edges(self, *args, **kwargs):
        backend.Popup(
            self.master,
            "Canny Edge Detection",
            "classify.canny_edge",
            **{
                "sigma": (
                    "Smoothing Factor",
                    (
                        (
                            backend.FloatRangeEntry,
                            1,
                            {"minval": 1, "maxval": 5},
                        ),
                    ),
                ),
            }
        )

    def classify_inv(self, *args, **kwargs):
        backend.Popup(
            self.master,
            "Invert Mask",
            "classify.inv",
        )

    # filter

    def filter_structure(self):
        mfm_filter = {
            "Gaussian Smoothing": (
                self.filter_gauss,
                self.criteria_loadedimg,
            ),
            # "Inverted": (
            #     self.filter_inv,
            #     self.criteria_loadedimg,
            # ),
            # "Mean": (
            #     self.filter_mean,
            #     self.criteria_loadedimg,
            # ),
        }
        return mfm_filter

    def filter_gauss(self):
        backend.Popup(
            self.master,
            "Gaussian Smoothing",
            "filter.gauss",
            **{
                "sigma": (
                    "Smoothing Factor",
                    (
                        (
                            backend.FloatRangeEntry,
                            1,
                            {"minval": 1, "maxval": 5},
                        ),
                    ),
                ),
            }
        )

    # # TODO
    # def filter_inv(self, ind):
    #     pass

    # # TODO
    # def filter_mean(
    #     self,
    #     ind,
    # ):
    #     pass

    # generic

    def generic_structure(self):
        mfm_generic = {
            # "Generic Label": (
            #     self.generic_func,
            #     self.criteria_loadedimg,
            # ),
        }
        return mfm_generic

    # numeric

    def numeric_structure(self):
        mfm_numeric = {
            # "Numeric Label": (
            #     self.numeric_func,
            #     self.criteria_loadedimg,
            # ),
        }
        return mfm_numeric

    # register

    def register_structure(self):
        mfm_register = {
            "True 3D": (
                self.register_true3D,
                self.criteria_twoloadedimgs,
            ),
        }
        return mfm_register

    def register_true3D(self):
        target, reference = self.master.get_selected_imgs()
        target.register.true3D(reference)
        self.master.refresh()

    # transform

    def transform_structure(self):
        mfm_transform = {
            "Distance Transform": (
                self.transform_distance,
                self.criteria_loadedimg,
            ),
        }
        return mfm_transform

    def transform_distance(self):
        backend.Popup(self.master, "Distance Transform", "transform.distance")

    # protocol

    def protocol_structure(self):
        mfm_protocol = {
            # "Protocol": (self.protocol_print_info, self.criteria_enabled)
        }
        return mfm_protocol

    # help

    def help_structure(self):
        mfm_help = {
            # "Sleep": (self.help_sleep, self.criteria_enabled),
            # "Other": (self.help_other, self.criteria_enabled),
        }
        return mfm_help

    def help_sleep(self, *args, **kwargs):  # pragma: no cover
        myiter = range(1, 501)
        w = 1 / np.array(myiter)
        for val in LinkedIterator(myiter, self.master.progressbar, w=w):
            time.sleep(0.01)

    def help_other(self, *args, **kwargs):  # pragma: no cover
        print("other")
