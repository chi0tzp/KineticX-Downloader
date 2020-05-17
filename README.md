# KinetiX-Downloader

*A Python3 script for downloading the **Kinetics 400, 600, and 700** datasets using [PyTube3](https://pypi.org/project/pytube3/).*

[Kinetics](https://deepmind.com/research/open-source/kinetics) is a large-scale, high-quality dataset of URL links to approximately 650,000 video clips that covers 700 human action classes, including  human-object interactions such as playing instruments, as well as  human-human interactions such as shaking hands and hugging. Each action class has at least 600 video clips. Each clip is human annotated with a single action class and lasts around 10s.

Available versions of Kinetics:

- Kinetics 400: [[paper](https://arxiv.org/abs/1705.06950) | [URLs and Annotations](https://storage.googleapis.com/deepmind-media/Datasets/kinetics400.tar.gz)]
- Kinetics 600: [[paper](https://arxiv.org/abs/1808.01340) | [URLs and Annotations](https://storage.googleapis.com/deepmind-media/Datasets/kinetics600.tar.gz)]
- Kinetics 700: [[paper](https://arxiv.org/abs/1907.06987) | [URLs and Annotations](https://storage.googleapis.com/deepmind-media/Datasets/kinetics700.tar.gz)]



## Prerequisites

- pytube3
- pandas
- tqdm



## Download dataset

Script `download.py`  can be used for downloading videos for the Kinetics dataset of given `version` (i.e., `400`, `600`, or `700`) and for given dataset subset (i.e., `train`, `test`, `validate`, or `all` of them):

~~~
usage: Kinetics dataset downloader [-h] [-v {400,600,700}] [-s {train,test,validate,all}] [-w WORKERS]

optional arguments:
  -h, --help            show this help message and exit
  -v {400,600,700}, --version {400,600,700}
                        choose dataset version ('400', '600', '700')
  -s {train,test,validate,all}, --subset {train,test,validate,all}
                        choose dataset subset ('train', 'test', 'validate', or 'all')
  -w WORKERS, --workers WORKERS
                        Set number of multiprocessing workers
~~~

Dataset videos will be saved under the directory `Kinetics<version>/`. It is expected that some videos will not be available for downloading. This may happen for various reasons (e.g., due to an unexpected error of PyTube or due to unavailability of the YouTube video). A error log file will be created as soon as a video download error occurs, and will store all YouTube IDs of the videos that have not been downloaded (`Kinetics<version>_<subset>_errors.log`).  After download process is complete, you may re-run it for attempting to download the videos that have failed (if a video has been downloaded successfully will be omitted).



## TODO

- [ ] Add script for extracting frames from downloaded video. In the meantime, you may take a look at [here](https://github.com/chi0tzp/PyVideoFramesExtractor).
