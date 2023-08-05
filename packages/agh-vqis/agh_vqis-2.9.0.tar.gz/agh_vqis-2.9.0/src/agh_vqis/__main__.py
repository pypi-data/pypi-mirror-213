# Authors: Jakub Nawała <jnawala@agh.edu.pl>, Filip Korus <fkorus@student.agh.edu.pl>
# Created: June 1, 2021
import argparse
import logging

import numpy as np
import pandas as pd
import pims
from cpbd.compute import compute
from pims import PyAVVideoReader

from ._logger import setup_console_and_file_logger
from .utils import ugc
from .utils.helpers import *

logger = setup_console_and_file_logger(__name__, log_file_name=f"{__name__}.log", level=logging.INFO)

allowed_mm_file_extensions = ['.jpg', '.jpeg', '.png', '.ts', '.mp4', '.y4m', '.mov', '.avi', '.mkv', '.gif', '.bmp']


def _run_agh_viqs(mm_file_path: Path, binary_path: Path, selected_vqis=32767):
    """
    Runs 15 VQ AGH's Video Quality Indicators (VQIs) on an input video or image (identified by *video_path*) and returns
    Pandas DataFrame with results.

    :param mm_file_path: path to a video or image file to process
    :param binary_path: path to a binary executable computing VQIs
    :param selected_vqis: a positive 16-bit integer stating which VQIs to run (all are run by default)
    :return: Pandas DataFrame with VQIs results or -1 if an error occurred
    """

    if binary_path is None:
        executable_file = get_executable_filename()
        binary_path = Path('/'.join(__file__.split('/')[:-1]) if platform.system() != 'Windows' else '\\'.join(__file__.split('\\')[:-1]), 'binaries/', executable_file)

    if not os.access(binary_path.resolve(), os.X_OK):
        logger.error(f'{str(binary_path.resolve())} file is not executable')
        return -1

    logger.debug('Creating working directory')
    random_folder_name = generate_uuid()
    mkdir(random_folder_name)
    yuv_file_path = Path(random_folder_name, mm_file_path.stem + '.yuv')

    logger.debug(f'Converting {str(mm_file_path.resolve())} to yuv format')
    convert_to_yuv(mm_file_path, yuv_file_path)

    video_width, video_height, _, FPS = get_mm_file_properties(mm_file_path)

    logger.debug('Calling VQIs binary file')

    sfs_call_elems = [str(binary_path.resolve()), str(yuv_file_path.resolve()), str(video_width), str(video_height), str(selected_vqis), str(FPS)]
    system_call(sfs_call_elems, logger)

    logger.debug(f'{sfs_call_elems[0]} binary file was successfully executed')

    vqis_csv_path = Path(random_folder_name, mm_file_path.stem + '.csv')

    mv_file(Path('./metricsResultsCSV.csv').resolve(), vqis_csv_path.resolve())

    vqis_res_df = pd.read_csv(vqis_csv_path, sep=r'\s+')

    logger.debug('Removing working directory')
    rmdir(random_folder_name)

    return vqis_res_df


def _colourfulness(frame: np.ndarray):
    """
    Runs Colourfulness image quality indicator (IQI) on a single video frame (see the *frame* parameter). Returns
    Colourfulness IQI result for this frame.

    Importantly, this code is based on Mohit Lamba's implementation of Colourfulness IQI in Matlab. See the following
    gist for more info:
     https://gist.github.com/MohitLamba94/7d40393f2fc1a478c84a6c5a4faaafdb

    :param frame: a 3-dimensional numpy ndarray representing a single video frame. First two dimensions correspond to
     image size (height x width). The last dimension corresponds to three colour channels: red, green and blue.
    :return: Colourfulness IQI result for the input video frame
    """
    # r_ch --- red channel, g_ch --- green channel, b_ch --- blue channel
    r_ch, g_ch, b_ch = frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]

    # rg = R - G
    rg = np.abs(r_ch - g_ch)
    rg = rg.flatten()

    # yb = 1/2(R + G) - B
    yb = np.abs((0.5 * r_ch + 0.5 * g_ch) - b_ch)
    yb = yb.flatten()

    # standard deviation and the mean value of the pixel cloud along direction, respectively
    std_rg = rg.std()
    mean_rg = rg.mean()

    std_yb = yb.std()
    mean_yb = yb.mean()

    std_rgyb = np.sqrt((std_rg ** 2) + (std_yb ** 2))
    mean_rgyb = np.sqrt((mean_rg ** 2) + (mean_yb ** 2))

    colourfulness = std_rgyb + (.3 * mean_rgyb)
    return colourfulness


def get_colourfulness_iqi(mm_file_path: Path, is_video=True):
    """
    Computes the Colourfulness image quality indicator (IQI) for each frame of an input video (as identified by the
    *video_path* path). Returns a Pandas Series with Colourfulness IQI for each video frame of the input video.

    :param mm_file_path: path to a multimedia file (video or image) to process
    :param is_video: a flag indicating whether we are processing a video (True, the default) or an image
    :return: Pandas Series with Colourfulness IQI for each video frame of the input video
    """
    if is_video:
        mm_material = PyAVVideoReader(str(mm_file_path))
    else:
        mm_material = pims.open(str(mm_file_path))  # PIMS, by default, reads each file as a series of images
    # Store Colourfulness IQI results for the input image or for all video frames in Pandas Series
    # s --- series
    colourfulness_s = pd.Series(np.zeros(len(mm_material)))
    for frame in mm_material[:]:  # frame is in the RGB24 pixel format (i.e., 3 channels, 8 bits long each)
        colourfulness = _colourfulness(frame)
        logger.debug(f"Colourfulness IQI for the {frame.frame_no}-th frame: {colourfulness:.5f}")
        colourfulness_s.loc[frame.frame_no] = colourfulness

    return colourfulness_s


def convert_to_grayscale_itur_bt601_7(frame: np.ndarray):
    """
    Converts RGB input frame (*frame*) to a single channel uint8 grayscale image. Importantly, the conversion is done
    according to coefficients defined in Rec. ITU-R BT.601.7.

    :param frame: a 3-dimensional (height x width x no. of channels) numpy ndarray representing an RGB image
    :return: 2-dimensional uint8 numpy ndarray with a grayscale version of the input frame
    """
    assert frame.ndim == 3, "Input frame given does not seem to be a colourful image. Exiting."
    gray_frame = np.zeros((frame.shape[0], frame.shape[1]))
    gray_frame = frame[:, :, 0] * .2989  # 0th channel = red channel
    gray_frame += frame[:, :, 1] * .587  # 1st channel = green channel
    gray_frame += frame[:, :, 2] * .114  # 2nd channel = blue channel
    gray_frame_uint8 = gray_frame.astype(np.uint8)
    return gray_frame_uint8


def _blur_amount(frame: np.ndarray):
    """
    Runs Blur Amount IQI for a single grayscale video frame (see the *frame* parameter). Returns Blur Amount IQI result
    for this frame.

    :param frame: a 2-dimensional 8-bit uint numpy ndarray representing a single video frame (as a grayscale image).
     The two dimensions correspond to image size (height x width).
    :return: Blur Amount IQI result for the input frame
    """
    # Transform the input video frame to grayscale
    gray_frame = convert_to_grayscale_itur_bt601_7(frame)
    blur_amount = compute(gray_frame)
    return blur_amount


def get_blur_amount_iqi(mm_file_path: Path, is_video=True):
    """
    Computes the Blur Amount Image Quality Indicator (IQI) on the input image or video (as identified by the
    *mm_file_path* path). The function returns Pandas Series with Blur Amount IQI result for each video frame in the
    input video (the Series has a length of 1, if the input is an image).

    :param mm_file_path: path to a multimedia file (video or image) to process
    :param is_video: a flag indicating whether we are processing a video (True, the default) or an image
    :return: Pandas Series with Blur Amount IQI for each video frame of the input video (or with a single entry if the
     input is an image)
    """
    if is_video:
        mm_material = PyAVVideoReader(str(mm_file_path))
    else:
        mm_material = pims.open(str(mm_file_path))  # PIMS, by default, reads each file as a series of images
    # Compute Blur Amount IQI for the input image or for each frame of the input video
    # s --- series
    blur_amount_s = pd.Series(np.zeros(len(mm_material)))
    for frame in mm_material[:]:
        blur_amount = _blur_amount(frame)
        logger.debug(f"Blur Amount IQI for the {frame.frame_no}-th frame: {blur_amount:.5f}")
        blur_amount_s.loc[frame.frame_no] = blur_amount
    return blur_amount_s


def _ugc(in_path: Path, results_vqis: pd.DataFrame):
    _, _, FPS, _ = get_mm_file_properties(in_path)

    # Get a list of shots
    scene_list_out = ugc.find_scenes(str(in_path))

    if len(scene_list_out) == 0:
        return None

    shots_data = ugc.get_shots_data(scene_list_out, results_vqis)
    shots_data = ugc.ugc(results_vqis, shots_data)

    return [{
        'range_start': int(item['frames_range'].split(', ')[0]) - 1,
        'range_end': int(item['frames_range'].split(', ')[1]) - 1,
        'ugc': item['ugc']
    } for item in shots_data]


def get_ugc_iqi(in_path: Path, nb_frames: int, results_vqis: pd.DataFrame):
    shots = _ugc(in_path, results_vqis)

    if shots is None:
        return None

    ugc_s = pd.Series(np.zeros(nb_frames))
    for frame in range(nb_frames):
        for shot in shots:
            if  shot['range_start'] <= frame <= shot['range_end']:
                ugc_s.loc[frame] = shot['ugc']
                break

    return ugc_s


def store_results(results: dict, in_video_path: Path, out_filename_base="agh_vqis_colourfulness_blur_amount"):
    """
    Stores results of image quality indicators (IQIs) calculated on (all) video frames of the input video.

    :param results: a dictionary of objects with IQIs results
    :param in_video_path: path to the input video that was processed
    :param out_filename_base: part of an output CSV filename independent of input video filename
    :return: nothing yet
    """
    assert len(results) != 0
    # Generate a filename that reflects to what input video it belongs to
    out_filename = "_".join(["VQIs", "for", in_video_path.stem]) + ".csv"
    # Handle the case when only one type of IQI was run
    # if len(results) == 1:
    #     iqi_enum, res = results.popitem()
    #     out_filename = "_".join([f"{iqi_enum.name}", out_filename])
    #     try:
    #         res.columns = res.columns.str.replace(':', '')
    #     except AttributeError:
    #         pass
    #     logger.info(f"Storing {iqi_enum.name} results in the {out_filename} file")
    #     res.to_csv(out_filename, index=False)
    #     return
    # More than one IQI type was run -> merge results for different IQIs
    iqi_enum, res = results.popitem()
    # res.columns = res.columns.str.replace(':', '')
    # out_filename = "_".join([f"{iqi_enum.name}", out_filename])
    while len(results) != 0:  # when this loop is finished, res will hold all results merged into one DataFrame
        next_iqi_enum, next_res = results.popitem()
        res = pd.merge(res, next_res, left_index=True, right_index=True)
        # out_filename = "_".join([f"{next_iqi_enum.name}", out_filename])

    res.columns = res.columns.str.replace(':', '')
    res.to_csv(out_filename, index=False)
    logger.info(f"All results stored in the {out_filename} file")
    return


def parse_user_input(cli: bool = False, options: dict = {}):
    """
    Parses user input (as provided through the command line).

    :return: nothing yet
    """
    parser = argparse.ArgumentParser(description="Computes image quality indicators (IQIs) for the input image or for"
                                                 " each video frame"
                                                 " from an input video. If no specific set of IQIs to compute is"
                                                 " selected, 15 AGH VQIs are run by default.")
    if cli:
        parser.add_argument("path",
                            help="Path to a multimedia file (image or video) to process or path to a folder with "
                                 "multimedia materials"
                                 " (photos or videos) to process", type=Path)
    parser.add_argument("-c", "--colourfulness", help="a flag indicating whether to run the Colourfulness image"
                                                      " quality indicator", action="store_true")
    parser.add_argument("-b", "--blur-amount", help="a flag indicating whether to run the Blur Amount image"
                                                    " quality indicator", action="store_true")
    parser.add_argument("-u", "--ugc", help="a flag indicating whether to run the ugc video"
                                                    " quality indicator", action="store_true")
    parser.add_argument("-v", "--vqis", help="a flag indicating whether to run the 15 AGH video"
                                             " quality indicators (VQIs). The VQIS argument must be a number"
                                             " specifying which VQIs to run. Each VQI represents a subsequent bit"
                                             " of a 16 bits long positive integer. For example, the Blockiness VQI"
                                             " corresponds to the least significant bit of this integer. The ordering"
                                             " of the rest of VQIs is as follows (values in parentheses identify"
                                             " decimal values that correspond to the one particular bit being set in"
                                             " the 16-bit positive integer): Blockiness (1), SA (2), Letterbox (4),"
                                             " Pillarbox (8), Blockloss (16), Blur (32), TA (64), Blackout (128),"
                                             " Freezing (256), Exposure (512), Contrast (1024), Interlace (2048),"
                                             " Noise (4096), Slice (8192) and Flickering (16384)."
                                             " Please note that you can provide a value for the VQIS parameter"
                                             " in the form of a hexadecimal number."
                                             " For example, 0x7FFF means running all VQIs.")
    parser.add_argument("-e", "--exec", help="provide here the path to the binary file running 15 AGH VQIs. The "
                                             "default is to use the agh_vqis_binary_x86_mt binary contained in the "
                                             "repo.", type=Path)
    args = parser.parse_args()
    # Run 15 AGH VQIs if no VQIs were selected
    if cli and not args.vqis:
        logger.info("No IQIs were selected. Running 15 AGH VQIs only.")
        args.vqis = "0x7FFF"
    return args


def process_single_mm_file(in_path: Path, cli: bool = False, options: dict = {}, args=None):
    """
    Processes single multimedia file (image or video).

    :param in_path: path to an input file to process
    :param options: options for executable file
    :return: status, 0 if successful, 1 otherwise
    """

    if args is None:
        args = parse_user_input(cli, options)

    if not in_path.exists():
        logger.error(f'{str(in_path)} file does not exists')
        return -1

    mm_file_ext = in_path.suffix
    if mm_file_ext not in allowed_mm_file_extensions:
        logger.error(f'{mm_file_ext} file extension is not supported')
        return -1

    # Read properties of an input multimedia file
    in_mm_file_w, in_mm_file_h, nb_frames, frame_rate = get_mm_file_properties(in_path)
    is_input_video = True  # a flag making further processing logic easier to comprehend
    if nb_frames == 0:
        is_input_video = False

    # Prepare a dictionary in which to store objects with IQIs results
    results = {}

    # Run Blur Amount IQI on the input video or image (if requested)
    if (VQIs.blur_amount in options and options[VQIs.blur_amount]) or args.blur_amount:
        logger.info(f"Running the Blur Amount IQI on the input ({str(in_path.resolve())})")
        blur_amount_s = get_blur_amount_iqi(in_path, is_video=is_input_video)
        blur_amount_s.name = "Blur_amount"
        results.update({Results.BLUR_AMOUNT: blur_amount_s})

    # Run Colorfulness indicator on the input video or image (if requested)
    if args.colourfulness or (not cli and VQIs.colourfulness not in options) or (
            not cli and VQIs.colourfulness in options and options[VQIs.colourfulness]):
        logger.info(f"Running the Colourfulness IQI on the input ({str(in_path.resolve())})")
        # s --- series
        colourfulness_s = get_colourfulness_iqi(in_path, is_video=is_input_video)
        colourfulness_s.name = "Colourfulness"
        results.update({Results.COLOURFULNESS: colourfulness_s})

    run_UGC = False
    if is_input_video and (args.ugc or (not cli and VQIs.ugc not in options) or (
            not cli and VQIs.ugc in options and options[VQIs.ugc])):
        run_UGC = True
        options[VQIs.TA] = True  # UGC indicator requires TA
        options[VQIs.SA] = True  # and SA IQIs

    if cli and args.vqis:
        vqis_selected = int(args.vqis, base=0)  # parse optional hexadecimal input

    if not cli:
        vqis_selected = get_selected_vqis(options)

    vqis_res_df = None
    # Run the mitsu_single_file.sh script on the input video or image (if requested)
    if not cli or args.vqis:
        logger.info(f"Running requested AGH VQIs on the input ({str(in_path.resolve())})")
        agh_vqis_path = Path(options['exec']) if ('exec' in options and options['exec']) else args.exec
        vqis_res_df = _run_agh_viqs(in_path, agh_vqis_path, vqis_selected)
        if type(vqis_res_df) is not pd.DataFrame:  # Running the VQIs failed
            return -1

        if (len(vqis_res_df) != int(nb_frames)) and is_input_video:
            logger.warning(
                f"For some reason the number of frames read by ffmpeg-python does not match the number of frames read "
                f"by binary file. You may want to check whether the results are valid.")
            logger.warning(f"This is the difference in the number of frames as indicated by the two methods: "
                           f"{np.abs(len(vqis_res_df) - int(nb_frames))}")

    if run_UGC:
        logger.info(f"Running the UGC IQI on the input ({str(in_path.resolve())})")
        # s --- series
        # print(results)

        ugc_s = get_ugc_iqi(in_path, int(nb_frames), vqis_res_df)
        if ugc_s is None:
            logger.error(f"Error when running UGC IQI")
        else:
            ugc_s.name = "UGC"
            results.update({Results.UGC: ugc_s})

    if vqis_res_df is not None:
        results.update({Results.VQIS: vqis_res_df})

    # Store all results in a single CSV file
    store_results(results, in_path)

    return 0


def process_folder_w_mm_files(folder_path: Path, cli: bool = False, options: dict = {}, args=None):
    """
    Processes a folder with multimedia files.

    TODO Consider adding recursive directory search. In other words, allow to recursively process files in all
     subdirectories.

    :param folder_path: path to a folder with multimedia files to process
    :param args: user arguments namespace, as returned by argparse (after processing user input)
    :return: status, 0 if successful, 1 otherwise
    """
    # Iterate over files in the folder one-by-one
    for child in folder_path.iterdir():
        # Ignore subdirectories
        if child.is_dir():
            logger.info(f"Skipping a subdirectory ({str(child)})")
            continue
        # Ignore non-video and non-image files
        # TODO Add here any video or image extensions we want to support
        if (child.suffix not in allowed_mm_file_extensions):
            logger.info(f"Not a multimedia file ({str(child)}), skipping")
            continue
        # Process a single video file
        # TODO Consider adding functionality of keeping all results in a single CSV file (as done in the legacy BATCH
        #  file)
        mm_file_path = child  # mm = multimedia
        status = process_single_mm_file(mm_file_path, cli, options, args)
    return 0


def main():
    # TODO Implement user input processing interface that allows to choose individual VQIs from the 15 AGH VQIs in a
    #  user-friendly manner
    args = parse_user_input(True, options={})

    in_path = args.path
    in_path = in_path.absolute()
    if not in_path.exists():
        raise FileNotFoundError(f"The path you specified ({in_path}) does not exist. Exiting.")
    if args.exec:
        agh_vqis_path = args.exec
        assert agh_vqis_path.exists(), f"The binary file with 15 AGH VQIs you specified ({str(agh_vqis_path)}) " \
                                       f"doesn't seem to exist. Quitting."

    if in_path.is_dir():
        logger.info(f"Processing a folder ({str(in_path)}) potentially containing a set of multimedia materials")
        status = process_folder_w_mm_files(in_path, cli=True, options={}, args=args)
    else:
        in_mm_file_path = in_path  # mm = multimedia
        status = process_single_mm_file(in_mm_file_path, cli=True, options={}, args=args)

    return status


if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
