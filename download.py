import sys
import os
import os.path as osp
import argparse
import urllib.request
import pandas as pd
import multiprocessing
from multiprocessing import Pool
from tqdm import tqdm
import tarfile
import pytube


global video_output_dir
error_file = 'errors.log'
errors = 0


def download_video(youtube_id):
    global errors
    # TODO: do not download it video already exists
    try:
        youtube = pytube.YouTube('https://www.youtube.com/watch?v=' + youtube_id)
        video = youtube.streams.first()
        video.download(output_path=video_output_dir, filename=youtube_id)
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

    # Define dataset root directory name
    root_dir = 'Kinetics{}'.format(args.version)

    # Create directory for downloading URLs and annotation files
    anno_dir = osp.join(root_dir, "annotations")
    if not osp.exists(anno_dir):
        os.makedirs(anno_dir, exist_ok=True)

    print("#.Download URLs and annotations tar.gz file for Kinetics-{}...".format(args.version))
    anno_root_url = "https://storage.googleapis.com/deepmind-media/Datasets/kinetics"
    anno_tar_file = osp.join(anno_dir, "kinetics{}.tar.gz".format(args.version))
    try:
        urllib.request.urlretrieve(url="{}{}.tar.gz".format(anno_root_url, args.version),
                                   filename=anno_tar_file)
    except:
        raise ConnectionError("Could not download URLs and annotations file: {}".format(anno_tar_file))

    print("#.Extract URLs and annotations tar.gz file for Kinetics-{}...".format(args.version))
    tf = tarfile.open(anno_tar_file)
    tf.extractall(path=anno_dir, members=None)
    anno_dir = osp.join(anno_dir, 'kinetics{}'.format(args.version))

    # Create directory for downloading videos
    video_dir = osp.join(root_dir, "videos")
    if not osp.exists(video_dir):
        os.makedirs(video_dir)

    # TODO: add comment
    subsets = (args.subset, )
    if args.subset == 'all':
        subsets = ('train', 'test', 'validate')

    # TODO: add comment
    for subset in subsets:
        print("#.Process subset: {}".format(subset))
        global video_output_dir
        video_output_dir = osp.join(video_dir, subset)
        if not osp.exists(video_output_dir):
            os.makedirs(video_output_dir)

        print("  \\__Parse URLs csv file...")
        youtube_ids = pd.read_csv(osp.join(anno_dir, '{}.csv'.format(subset))).youtube_id.tolist()
        print("  \\__Download videos...")
        pool = Pool(args.workers)
        for _ in tqdm(pool.imap_unordered(download_video, youtube_ids), total=len(youtube_ids)):
            pass
        pool.close()


if __name__ == '__main__':
    main()
