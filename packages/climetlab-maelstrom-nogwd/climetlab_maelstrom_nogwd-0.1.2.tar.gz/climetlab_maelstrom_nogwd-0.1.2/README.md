## maelstrom-nogwd

A dataset plugin for climetlab for the dataset maelstrom-nogwd/nogwd.


Features
--------

In this README is a description of how to get the maelstrom-nogwd.

## Dataset description
Contains the input/output dataset for learning non-orographic 
gravity wave drag, as described in https://arxiv.org/abs/2101.08195
Data is group by forecast start date.

## Using climetlab to access the data
Data can be accessed either by forecast start-date or dataset type.
With neither argument provided, the first file is loaded, corresponding
to 2015-01-01. Incorrect dates will be flagged.
Dataset types are "training", "validation" & "testing" corresponding
to the date groups outlined in https://arxiv.org/abs/2101.08195


The climetlab python package allows easy access to the data with a few lines of code such as:
```

!pip install climetlab climetlab_maelstrom_nogwd
import climetlab as cml
ds = cml.load_dataset("maelstrom-nogwd", date='2015-01-01')
ds.to_xarray()
#or
ds = cml.load_dataset("maelstrom-nogwd", dataset='training')
ds.to_xarray()
```
