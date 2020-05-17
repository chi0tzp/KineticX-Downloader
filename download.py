import os
import os.path as osp
import argparse
import urllib.request
import pandas as pd
from multiprocessing import Pool
from tqdm import tqdm
import tarfile
import pytube


global video_output_dir, error_file
errors = 0


def download_video(youtube_id):
    """Download video from YouTube using PyTube.

    Args:
        youtube_id (str): Youtube id (https://www.youtube.com/watch?v=<youtube_id>)

    """
    global error_file, errors
    try:
        youtube = pytube.YouTube('https://www.youtube.com/watch?v=' + youtube_id)
        video = youtube.streams.first()
        video_filename = osp.join(video_output_dir, youtube_id + '.' + video.subtype)
        if (not osp.isfile(video_filename)) or (os.stat(video_filename).st_size == 0):
            try:
                video.download(output_path=video_output_dir, filename=youtube_id)
            except:
                with open(error_file, "a") as f:
                    f.write("{}\n".format(youtube_id))
                    errors += 1
    except:
        with open(error_file, "a") as f:
            f.write("{}\n".format(youtube_id))
            errors += 1


def main():
    parser = argparse.ArgumentParser("Kinetics dataset downloader")
    parser.add_argument('-v', '--version', type=str, default='400', choices=('400', '600', '700'),
                        help="choose dataset version ('400', '600', '700')")
    parser.add_argument('-s', '--subset', type=str, default='val', choices=('train', 'test', 'validate', 'all'),
                        help="choose dataset subset ('train', 'test', 'validate', or 'all')")
    parser.add_argument('-w', '--workers', type=int, default=None, help="Set number of multiprocessing workers")
    args = parser.parse_args()

    print("#.Download Kinetics{} dataset...".format(args.version))

    # Define dataset root directory name
    root_dir = 'Kinetics{}'.format(args.version)

    # Create directory for downloading URLs and annotation files
    anno_dir = osp.join(root_dir, "annotations")
    if not osp.exists(anno_dir):
        os.makedirs(anno_dir, exist_ok=True)

    print("#.Download URLs and annotations tar.gz file for Kinetics{}...".format(args.version))
    anno_root_url = "https://storage.googleapis.com/deepmind-media/Datasets/kinetics"
    anno_tar_file = osp.join(anno_dir, "kinetics{}.tar.gz".format(args.version))
    try:
        urllib.request.urlretrieve(url="{}{}.tar.gz".format(anno_root_url, args.version),
                                   filename=anno_tar_file)
    except:
        raise ConnectionError("Could not download URLs and annotations file: {}".format(anno_tar_file))

    print("#.Extract URLs and annotations tar.gz file for Kinetics{}...".format(args.version))
    tf = tarfile.open(anno_tar_file)
    tf.extractall(path=anno_dir, members=None)
    anno_dir = osp.join(anno_dir, 'kinetics{}'.format(args.version))

    # Create directory for downloading videos
    video_dir = osp.join(root_dir, "videos")
    if not osp.exists(video_dir):
        os.makedirs(video_dir)

    # Get dataset subset(s) for downloading
    subsets = (args.subset, )
    if args.subset == 'all':
        subsets = ('train', 'test', 'validate')

    # Download dataset subset
    for subset in subsets:
        print("#.Process subset: {}".format(subset))
        global video_output_dir, error_file

        # Create dir for dataset subset
        video_output_dir = osp.join(video_dir, subset)
        if not osp.exists(video_output_dir):
            os.makedirs(video_output_dir)

        # Define error log file
        error_file = 'Kinetics{}_{}_errors.log'.format(args.version, subset)
        if osp.exists(error_file):
            os.remove(error_file)

        # Parse URLs csv file and get a list of YouTube IDs to download
        print("  \\__Parse URLs csv file...")
        youtube_ids = pd.read_csv(osp.join(anno_dir, '{}.csv'.format(subset))).youtube_id.tolist()

        # Download YouTube videos for given IDs
        print("  \\__Download videos...")
        pool = Pool(args.workers)
        for _ in tqdm(pool.imap_unordered(download_video, youtube_ids), total=len(youtube_ids)):
            pass
        pool.close()


if __name__ == '__main__':
    main()
