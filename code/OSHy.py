import ants
import os
import glob
import argparse
import subprocess

class Target_img():

    def __init__(self, img_file:str, denoise:bool, n4bias:bool, out_dir:str, 
                 oshy_data):

        """
        img_file (str): File path to target image. File extension must be nii.gz
        denoise (bool): Target is denoised if True.
        n4bias (bool): Target is N4 bias corrected if True.
        mosaic (bool): Mosaic image will be generated if True.
        out_dir (str): File path to output directory.
        oshy_data (OSHy_data): An object of the OSHy_data class.
        """

        print(f"Reading {img_file}.")

        self.target_img = ants.image_read(img_file)
        self.sub = img_file.split("/")[-1].split("_")[0]
        self.outdir = out_dir.strip()
        self.oshy_data = oshy_data

        #Create sub folder in output directory
        if not os.path.exists(f"{self.outdir}/{self.sub}"):
            os.mkdir(f"{self.outdir}/{self.sub}")

        if denoise:
            self.run_denoise()
        
        if n4bias:
            self.run_n4bias()

        self.native_box = self.get_native_box()
        self.target_cropped = self.crop_target()
        ants.image_write(
            self.target_cropped, 
            filename=f"{self.outdir}/{self.sub}/{self.sub}"\
                      "_cropped_T1w.nii.gz")
        self.segmentation = None
        
    def __repr__(self):
        
        print(self.target_img)
    
    def run_denoise(self):
        """Denoises image.

        Runs ants.denoise_image on the target image.

        Return ANTsImage: An image that has been denoised.
        """
        
        print(f"Denoising {self.sub}.")

        denoised_img = ants.denoise_image(self.target_img)

        return(denoised_img)

    def run_n4bias(self):
        """Runs N4 bias field correction.

        Runs ants.n4_bias_field_correction on the target image.

        Return ANTsImage: An image that has been N4 bias field corrected.
        """

        print(f"Running N4 bias correction on {self.sub}.")

        n4_bias_corrected = ants.n4_bias_field_correction(self.target_img)

        return(n4_bias_corrected)

    def get_native_box(self):
        """Generates a native bounding box.
        
        Create transform files from template space to the target image. A 
        bounding box in template space is transformed into the target
        image's native space.
        
        Return ANTsImage: A bounding box in the target image's native space.
        """

        print(f"Registering {self.sub} to template.")

        template = self.oshy_data.template
        template_box = self.oshy_data.template_box

        registered_dict = ants.registration(template, self.target_img, 'SyN', 
        reg_iterations = (50, 25, 0))

        warped_box = ants.apply_transforms(
            fixed = self.target_img, 
            moving = template_box, 
            transformlist = registered_dict['invtransforms'], 
            interpolator = 'multiLabel'
            )

        return(warped_box)
    
    def crop_target(self):
        """Crops the target image.
        
        Runs ants.crop_image on the target image.
        
        Return ANTsImage: A cropped target image.
        """

        print(f"Cropping {self.sub} with a bounding box.")

        cropped_img = ants.crop_image(self.target_img, 
                                      label_image=self.native_box, label=1)

        return(cropped_img)

    def run_JLF2(self):
        """Runs antsJointLabelFusion2 on the command line.

        Return None
        """

        os.environ['ANTSPATH'] = '/opt/ants-2.3.1/'

        jlf2_command = [
            "antsJointLabelFusion2.sh", 
            "-d", "3",
            "-o", f"{self.outdir}/{self.sub}/{self.sub}_",
            "-t", f"{self.outdir}/{self.sub}/{self.sub}_cropped_T1w.nii.gz"]

        jlf2_command = self.get_atlases(jlf2_command)

        jlf2_command.extend(["-b" ,"1", "-b", "2", "-b" "3", "-b", "4", 
        "-a", "4", "-s", "10"])

        jlf_process = subprocess.Popen(jlf2_command, stdout=subprocess.PIPE, 
                                       stdin=subprocess.PIPE, 
                                       stderr=subprocess.STDOUT)

        jlf_process.wait()

        print(jlf_process.communicate())

        self.segmentation = ants.image_read(
            glob.glob(f"{self.outdir}/{self.sub}/*Label*")[0])


    def get_atlases(self, jlf2_command):
        """Gets atlas and label paths.
        
        Get atlas and label paths, then extends the argument list for JLF2.
        
        Return list: A list of strings.
        """
        
        atlases = self.oshy_data.get_atlases()
        labels = self.oshy_data.get_labels()

        atlases.sort()
        labels.sort()

        for atlas, label in zip(atlases, labels):

            jlf2_command.extend(["-g", atlas])
            jlf2_command.extend(["-l", label])

        return(jlf2_command)


    def create_mosaic(self):
        """Create a mosaic of the JLF segmentation.
        
        Runs ants.plot to create a mosaic of the JLF segmentation. The output
        image is saved in f"{self.outdir}/{self.sub}/"

        Return None
        """

        print(f"Generating a mosaic of {self.sub}.")

        ants.plot(self.target_cropped, self.segmentation, overlay_cmap='jet', 
        overlay_alpha=80, axis=1, slices=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9], 
        title=self.sub, 
        filename=f"{self.outdir}/{self.sub}/{self.sub}_mosaic.png")

    def calc_volume(self):
        """Calculates the label volumes.
        
        Calculates the label volumes by calling ImageMath on the command
        line. The output is saved as a text file.
        
        Return None
        """

        imath_arguments = ["ImageMath", "3", 
        f"{self.outdir}/{self.sub}/{self.sub}_volumes.txt", "LabelStats", 
        glob.glob(f"{self.outdir}/{self.sub}/*Label*")[0],
        f"{self.outdir}/{self.sub}/{self.sub}_cropped_T1w.nii.gz"]

        imath_process = subprocess.Popen(
            imath_arguments, stdout=subprocess.PIPE, stdin=subprocess.PIPE, 
            stderr=subprocess.STDOUT)

        imath_process.wait()

    def resample_segmentation(self):
        """Resamples segmentation to original target.
        
        Runs ants.resample_image_to_target and saves the image. The object
        variable self.segmentation is also updated.
        
        Return None
        """

        resampled_seg = ants.resample_image_to_target(
            self.segmentation, self.target_img, interp_type="genericLabel")
        
        self.segmentation = resampled_seg

        ants.image_write(
            resampled_seg, 
            f"{self.outdir}/{self.sub}/{self.sub}_resampled_Labels.nii.gz")

    def threshold_structures(self):
        """Separates hypothalamus and fornix labels.
        
        Thresholds the segmentation so the hypothalamus and fornix labels
        are in separate files.
        
        Return None
        """

        hypothalamus = ants.threshold_image(self.segmentation, 1, 2)
        fornix = ants.threshold_image(self.segmentation, 3, 4)

        ants.image_write(
            hypothalamus, 
            f"{self.outdir}/{self.sub}/{self.sub}_hypothalamus.nii.gz")

        ants.image_write(
            fornix, 
            f"{self.outdir}/{self.sub}/{self.sub}_fornix.nii.gz")

class OSHy_data():

    def __init__(self, tesla:str, bimodal:bool):

        """
        tesla (str): Magnet strenght of images.
        bimodal (bool): True if Joint Label Fusion priors are to be bimodal.
        """

        self.tesla = tesla
        self.bimodal = bimodal
        self.template = self.get_template()
        self.template_box = self.get_template_box()
        self.atlas_list = self.get_atlases()
        self.label_list = self.get_labels()

    def get_template(self):
        """Retrieves the template.
        
        Retrieves the template at the given tesla magnet strength.

        Return ANTsImage: A template image.
        """

        self.template = ants.image_read(
            f"/OSHy/templates/{self.tesla}T_template.nii.gz")

        return(self.template)

    def get_template_box(self):
        """Retrieves the template bounding box.
        
        Retrieves the template bounding box at the given tesla magnet strength.

        Return ANTsImage: A bounding box in template space.
        """

        self.template_box = ants.image_read(
            f"/OSHy/templates/{self.tesla}T_box.nii.gz")

        return(self.template_box)

    def get_atlases(self):
        """Retrieves the atlas intensity images.
        
        Retrieves the atlas filenames at the given the tesla magnet 
        strength.

        Return list: A list of strings.
        """

        if self.bimodal:
            atlas_files = glob.glob(f"/OSHy/atlases/{self.tesla}T/*")
        else:
            atlas_files = glob.glob(f"/OSHy/atlases/{self.tesla}T/*T1w*")

        return(atlas_files)

    def get_labels(self):
        """Retrieves the labels for each atlas.
        
        Retrieves the atlas label filenames at the given tesla magnet strength.

        Return list: A list of strings.
        """

        label_files = glob.glob(f"/OSHy/atlases/{self.tesla}T/*label*")

        if self.bimodal:
            label_files.extend(label_files)
        
        return(label_files)

def convert_to_bool(b_str:str):
    
    """Converts a string to a boolean.
    
    b_str (str): A string that spells out True or False, regardless of
                 capitilisation.

    Return bool
    """

    if b_str.upper() == "TRUE":
        return True
    else:
        return False

if __name__ == "__main__":

    my_args = argparse.ArgumentParser()

    my_args.add_argument("-t", "--target", required=True, nargs="+",
        help = "A string or strings in a list pointing to the target image(s)."\
               " Must end in nii.gz.")
    my_args.add_argument("-d", "--denoise", required=True,
        help = "A boolean indicating if denoising is to be run on the target"\
             " image.")
    my_args.add_argument("-n", "--n4bias", required=True,
        help="A boolean indicating if N4 bias correction is to be run on the"\
             " target image.")
    my_args.add_argument("-m", "--mosaic", required=True,
        help = "A boolean indicating if a mosaic image is to be plotted after"\
               " running Joint Label Fusion.")
    my_args.add_argument("-o", "--outdir", required=True,
        help = "A string pointing to the output directory.")
    my_args.add_argument("-x", "--tesla", required=True,
        help = "An integer (either 3 or 7) indicating the magnet strength.")
    my_args.add_argument("-b", "--bimodal", required=True,
        help = "A boolean indicating if bimodal priors are to be used."\
               " If FALSE, then only unimodal priors will be used.")
    
    args = vars(my_args.parse_args())

    #f = open(f"{args['outdir']}/OSHy_volumes.txt", "x")

    oshy_dat = OSHy_data(args['tesla'], 
                         convert_to_bool(args['bimodal']))

    for target in args['target']:
        my_image = Target_img(img_file = target, 
        denoise = convert_to_bool(args['denoise']), 
        n4bias = convert_to_bool(args['n4bias']),
        out_dir = args['outdir'],
        oshy_data = oshy_dat)

        my_image.segmentation = my_image.run_JLF2()

        if convert_to_bool(args['mosaic']):
            my_image.create_mosaic()

        my_image.calc_volume()
        my_image.resample_segmentation()
        my_image.threshold_structures()
