# Mining Italian Short Argumentative Texts

## About

This repository contains the code related to the paper "Mining Italian Short Argumentative Texts" (I. Namor, P.Totis, S. Garda, M.Stede). It is a fork of the project [Evidence graphs for parsing argumentation structure](https://github.com/peldszus/evidencegraph) by A.Peldszus. 

We extend the original work to run on an Italian corpus of argumentative texts. 

## Prerequisites

This code runs in Python 3.6. It is recommended to install it in a separate virtual environment. Here are installation instructions for an Ubuntu 18.04 linux:

```
# basics
sudo apt install virtualenv python3.6-dev
# for lxml
sudo apt install libxml2-dev libxslt1-dev
# for matplotlib
sudo apt install libpng-dev libfreetype6-dev
# for graph plotting
sudo apt install graphviz
```

## Setup environment

Install all required python libaries in the environment and download the language models required by the spacy library.

```
make install-requirements
make download-spacy-data-de
make download-spacy-data-en
make download-spacy-data-it
```

After that you need to download all the models needed for `matetools` and place them in `mateparser/models`:
1) parser,tagger and morphology [(here)](https://drive.google.com/file/d/0B-qbj-8rtoUMLUg5NGpBVW9JNkE/edit)
2) lemmatizer [(here)](https://drive.google.com/file/d/0B-qbj-8rtoUMaUVsWUFuOE81ZW8/edit)

## Test

Make sure all the tests pass.

```
make test
```

## Run a minimal experiment

Run a (shortened and simplified) minimal experiment, to see that everything is working:

```
make run-minimal-en
```

You should (see last lines of the output) get an average macro F1 of the *base classifiers* similar to: (cc ~= 0.846, ro ~= 0.758, fu ~= 0.745, at ~= 0.705).

Evaluate the results, which have been written to `data/`:

```
env/bin/python src/experiments/eval_minimal.py --lang en
```

You should (see first lines of the output) get an average macro F1 for the *decoded results* similar to: (cc ~= 0.861, ro ~= 0.771, fu ~= 0.754, at ~= 0.712).

## Replicate published results

Run one of the following:

```
make run-complete-en
make run-complete-de
make run-complete-it
```

# Additions

## 1) Situation Entity types 

It is possible to add the [(SE annotations)](http://www.cl.uni-heidelberg.de/english/research/downloads/resource_pages/GER_SET/GER_SET_data.shtml) to the [(micro-texts)](http://angcl.ling.uni-potsdam.de/resources/argmicro.html) corpus.

In order to to so it is needed to first parse the annotations to match the actual ADUs found in the `micro-texts` corpus.

```
env/bin/python src/my_scripts/parse_set.py ./resources/adu2setypes.pkl
```

This will created a compressed dictionary containing all `micro-texts` ADUs with their corresponding SE types. In order to avoid mismatching with the ADUs representation in the `features_text.py` module, all the ADUs are in one line with no space.

Then it is possible to use 
    

```
env/bin/python src/my_scripts/run_minimal_with_se_feat.py --lang de
```

to asses the impact of such features.

## 2) Visualiazing Argumentation Graphs 

### 2.1) Micro-text originl ADUs

In this setting the `micro-text` corpus is the one provided by Andreas found in the folder `argmin/data/corpus/german/arg`. Therefore, you do not need to pass any specific path to the corpus.

```
env/bin/python src/my_scripts/files_to_pred_and_viz.py --out <folder> --model <path to pre-trained model>
```

where `--out` specify the path to a folder (if it does not exist it will creat it) and for `--model` I suggest to use model the last model produced with `run_minimal.py`, so it should be `data/models/m112de-test-adu-full-noop__<hash>__4`.

If you have in mind some interasting cases that you wish to check directly, instead of going through the all corpus you can pass them with `--text-ids` (comma separated list).
So, for instance, if you want to see what happens only for `micro_b001` and `micro_b002` you can call:
    

```
env/bin/python src/my_scripts/files_to_pred_and_viz.py --out <folder> --model <path to pre-trained model> --text-ids micro_b001,micro_b002
```

In the output folder you will find 2 files for each text: one containing the predictions, and one being the graph image.

### 2.2) Micro-text customly segmented ADUs

You can also use the segmentation obtained with the DiscourseSegmenter. Since getting such segmentations for `micro-texts` takes a while (mate tools are quite slow) I include here in `data/corpus/german_mate_segmented` all the texts already segmented. Same as before you can get predictions for these texts and visualize their graphs, with:

```
env/bin/python src/my_scripts/files_to_pred_and_viz.py --dir <input dir> --suffix <segmented> --out <folder> --model <path to pre-trained model> --text-ids micro_b001,micro_b002
```

The only difference is that you have to pass a folder containing all the segmented texts, in this case `data/corpus/german_mate_segmented` and the a suffix argument `segmented` (which is the default) to retrieve the ADUs created with the mechanism we taksed about.

### 2.3) From custom files

It is possible to create visualization of argumentation structure of any texts. In order to do so it is needed first to obtain ADUs from a text. To do so [(DiscourseSegmenter)](https://github.com/WladimirSidorenko/DiscourseSegmenter) will be used.

Please make sure you install `DiscourseSegmenter` in a different virtualenvironment. A __quick__ way to do so is to use the script in `shortcuts` named `create_dseg_venv`. This will create a new virtual enviroment with discourse segmenter installed. Moreover, in order to use this segmentation tool you need to install as well the `Mate tools` models to provide the input in the requested format. To do so, please follow the instruction in `mateparser/models` dir.

With the scripy `matepar_parser.sh` (always in `shortcuts`) you can process all files inside a folder to get directly the output of `DiscourseSegmenter`. Finally by calling:
    

```
env/bin/python src/my_scripts/files_to_pred_and_viz.py --dir <dir with dseg files> --suffix <e.g. .seg> --model <trained evidencegraph model path> --out <out dir>
```

you can save the predictions on your texts and their visualization in a png file.

In order to provide a __quick__ way to do this, on a **single file** it is possible to use:

```
user@machine:argumentation_minig ./shortcuts/text2arg.sh -i <input file> -o <out folder>
```

to directly go from a simple text to its argumentation structure visualization.

## References

1) [Joint prediction in MST-style discourse parsing for argumentation mining](https://aclweb.org/anthology/D/D15/D15-1110.pdf)  
   Andreas Peldszus, Manfred Stede.  
   In: Proceedings of the 2015 Conference on Empirical Methods in Natural Language  Processing (EMNLP), Portugal, Lisbon, September 2015.

2) Mining Italian Short Argumentative Texts
	Ivan Namor, Pietro Totis, Samuele Garda, Manfred Stede.
	In: CLIC 2019