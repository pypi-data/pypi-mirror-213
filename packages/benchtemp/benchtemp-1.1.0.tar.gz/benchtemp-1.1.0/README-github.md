# BenchTeMP: A General Benchmark Library for Evaluating Temporal Graph Models

## Overview
**BenchTeMP** is a general Benchmark Python Library for users to create and evaluate Temporal Graph models quickly and efficiently. 
**BenchTeMP** provides users with the unified **original dataset preprocess function, Data Class, DataLoader, EdgeSampler, and Evaluator** for creating and evaluating your Temporal Graph model.

- The original datasets are [Here]() and the datasets preprocessed by BenchTeMP are [Here]().
- The GitHub of BenchTeMP project is [Here]().
- The source codes for evaluating existing Temporal Graph models based on BenchTeMP are [Here](). 
- The leaderboards website created by our team for Temporal Graph models is [Here]().

## Installation
### Requirements
Please ensure that you have installed the following dependencies:

- numpy >= 1.18.0
- pandas >= 1.2.0
- sklearn >= 0.20.0

### PyPI install
```bash
pip3 install benchtemp 
```

## Package Usage
### Datasets
The datasets that have been preprocessed by BenchTeMP are [Here]().
You can directly download the datasets and then put them into the directory './data'.

In addition, BenchTeMP provides data processing functions. you can download the original datasets [Here]() and then 
use the functions provided by BenchTeMP for data preprocessing.

Function:
**benchtemp.preprocessing.data.data_preprocess(data_name <font color='lightblue'>: str</font>, bipartite <font color='lightblue'>: bool</font>=True)**

Parameters:
- **data_name <font color='lightblue'>: str</font>** - the name of the dataset.
- **bipartite <font color='lightblue'>: bool</font>** - Whether the Temporal Graph is bipartite graph.

Returns:
- **ml_{data_name}.csv** - the csv file of the Temporal Graph.
- **ml_{data_name}.npy** - the edge features of the Temporal Graph.
- **ml_{data_name}_node.npy** - the node features of the Temporal Graph.

Example:

```python
from benchtemp.data.preprocessing import data_preprocess

# If the dataset is bipartite graph, i.e. the user (source nodes) and the item (destination nodes) are of the same type.
data_preprocess("data_name", bipartite=True)

# non-bipartite graph.
data_preprocess("data_name", bipartite=False)
```

Notes:

For bipartite graph, BenchTeMP will factorize the source node index and 
the destination node index, respectively. 
```python
import pandas as pd

assert len(sources) == len(destinations)

# bipartite graph
sources, _ = pd.factorize(sources)
destinations, _ = pd.factorize(destinations)

upper_u = sources.max + 1
destinations = destinations + upper_u
```
For bipartite graph, BenchTeMP will factorize the concatenation of source node array and 
the destination node array. 

```python
import pandas as pd
import numpy as np

assert len(sources) == len(destinations)
interaction_num = len(sources)

# non-bipartite graph
node_index, _ = pd.factorize(np.concatenate((sources, destinations), axis=0))

sources = node_index[[0:interaction_num]]
destinations = node_index[[interaction_num:interaction_num + interaction_num]]
```


### TemporalData Class
Class:

**Data(sources <font color='lightblue'>: numpy.ndarray</font>,
destinations <font color='lightblue'>: numpy.ndarray</font>,
timestamps <font color='lightblue'>: numpy.ndarray</font>,
edge_idxs <font color='lightblue'>: numpy.ndarray</font>,
labels <font color='lightblue'>: numpy.ndarray</font>)**

Parameters:
- **sources <font color='lightblue'>: numpy.ndarray</font>** - Array of sources of Temporal Graph edges.
- **destinations <font color='lightblue'>: numpy.ndarray</font>** - Array of destinations of Temporal Graph edges.
- **timestamps <font color='lightblue'>: numpy.ndarray</font>** - Array of timestamps of Temporal Graph edges.
- **edge_idxs <font color='lightblue'>: numpy.ndarray</font>** - Array of edge IDs of Temporal Graph edges.
- **labels <font color='lightblue'>: numpy.ndarray</font>** - Array of labels of Temporal Graphe dges.

Returns: 
- **<font color='lightblue'> benchtemp.Data</font>**. A Temporal Graph.




Example:
```python
import pandas as pd
import numpy as np
from benchtemp.utils import Data

graph_df = pd.read_csv("dataset_path")

sources = graph_df.u.values
destinations = graph_df.i.values
edge_idxs = graph_df.idx.values
labels = graph_df.label.values
timestamps = graph_df.ts.values

# For example, the full Temporal Graph of the dataset is full_data.
full_data = Data(sources, destinations, timestamps, edge_idxs, labels)
```


### DataLoader
### (1) Link Prediction task
Function:

**benchtemp.lp.readers.get_data(dataset_name <font color='lightblue'>: str</font>, different_new_nodes_between_val_and_test=False, randomize_features=False)**
 
Parameters:
- **dataset_name <font color='lightblue'>: str</font>** - The name of the dataset. The dataset file (.csv file of the Temporal Graph, .npy file of the node features and .npy file of the edge features) should be in "./data" directory.
- **different_new_nodes_between_val_and_test <font color='lightblue'>: bool</font>** - Different new nodes between  the validation and test dataset.
- **randomize_features <font color='lightblue'>: bool</font>** - Random initialization of node Features. 

Returns:
- **node_features <font color='lightblue'>: numpy.ndarray</font>** - Array of the Node Features of the Temporal Graph. 
- **edge_features <font color='lightblue'>: numpy.ndarray</font>** - Array of the Edge Features of the Temporal Graph.
- **full_data <font color='lightblue'>: benchtemp.Data</font>** - Full Temporal Graph dataset. 
- **train_data <font color='lightblue'>: benchtemp.Data</font>** - The training Temporal Graph dataset. 
- **val_data <font color='lightblue'>: benchtemp.Data</font>** - The validation Temporal Graph dataset.
- **test_data <font color='lightblue'>: benchtemp.Data</font>**  - The **transductive** test Temporal Graph dataset.
- **new_node_val_data <font color='lightblue'>: benchtemp.Data</font>** - The **inductive [new-]** setting validation Temporal Graph dataset.
- **new_node_test_data <font color='lightblue'>: benchtemp.Data</font>** - The **inductive [new-]** setting test Temporal Graph dataset.
- **new_old_node_val_data <font color='lightblue'>: benchtemp.Data</font>** - The **inductive [new-old]** setting validation Temporal Graph dataset.
- **new_old_node_test_data <font color='lightblue'>: benchtemp.Data</font>** - The **inductive [new-old]** setting test Temporal Graph dataset.
- **new_new_node_val_data <font color='lightblue'>: benchtemp.Data</font>** - The **inductive [new-new]** setting validation Temporal Graph dataset.
- **new_new_node_test_data <font color='lightblue'>: benchtemp.Data</font>** - The **inductive [new-new]** setting test Temporal Graph dataset.
- **unseen_nodes_num <font color='lightblue'>: int</font>** - The number of unseen nodes of inductive setting.

Example:

```python
from benchtemp.lp.dataloader import get_data

node_features, edge_features, full_data, train_data, val_data, test_data, new_node_val_data, new_node_test_data, new_old_node_val_data, new_old_node_test_data, new_new_node_val_data, new_new_node_test_data, unseen_nodes_num = get_data(
    dataset_name, different_new_nodes_between_val_and_test=False, randomize_features=False)
```

### EdgeSampler
BenchTeMP provides the unified
negative edge sampler with **seed** for Link Prediction task to  sample an equal amount of negatives to the positive interactions.

Class:

**RandEdgeSampler(src_list <font color='lightblue'>: numpy.ndarray</font>, dst_list <font color='lightblue'>: numpy.ndarray</font>, seed <font color='lightblue'>: int</font> =None)**

Parameters:
- **src_list <font color='lightblue'>: numpy.ndarray</font>** - the list of source nodes.
- **dst_list <font color='lightblue'>: numpy.ndarray</font>** - the list of destination nodes.
- **seed <font color='lightblue'>: numpy.ndarray</font>** - seed of random.

Returns: 

- **<font color='lightblue'> benchtemp.RandEdgeSampler</font>**

Example:

```python
from benchtemp.lp.edgesampler import RandEdgeSampler

# For example, if you are training , you should create a training  RandEdgeSampler based on the training dataset.
train_rand_sampler = RandEdgeSampler(train_data.sources, train_data.destinations)

...
for epoch in range(args.epochs):
    ...
    # sample an equal amount of negatives to the positive interactions.
    _, negatives_batch = train_rand_sampler.sample(size)
    ...
...
```
### (2) Node Classification task
Function:



**benchtemp.nc.readers.get_data_node_classification((dataset_name <font color='lightblue'>: str</font>, use_validation <font color='lightblue'>: bool</font>=False))** 

Parameters:
- dataset_name <font color='lightblue'>: str</font> - The name of the dataset. The dataset file (.csv file of the Temporal Graph, .npy file of the node features and .npy file of the edge features) should be in "./data" directory.
- use_validation <font color='lightblue'>: bool</font> - Whether use validation dataset or not.

Returns:
- **node_features <font color='lightblue'>: numpy.ndarray</font>** - Array of the Node Features of the Temporal Graph. 
- **edge_features <font color='lightblue'>: numpy.ndarray</font>** - Array of the Edge Features of the Temporal Graph.
- **full_data <font color='lightblue'>: benchtemp.Data</font>** - Full Temporal Graph dataset for Node Classification task. 
- **train_data <font color='lightblue'>: benchtemp.Data</font>** - The training Temporal Graph dataset for Node Classification task. 
- **val_data <font color='lightblue'>: benchtemp.Data</font>** - The validation Temporal Graph dataset for Node Classification task.
- **test_data <font color='lightblue'>: benchtemp.Data</font>**  - The test Temporal Graph dataset for Node Classification task.



### EarlyStopMonitor
Class:

**EarlyStopMonitor(max_round=3, higher_better=True, tolerance=1e-10)**

Parameters:
- **max_round <font color='lightblue'>: int </font>** - the maximum number of rounds of EarlyStopMonitor.
- **higher_better <font color='lightblue'>: bool </font>** - better the performance.
- **tolerance <font color='lightblue'>: float </font>** - the tolerance of the EarlyStopMonitor.

Returns:
- **<font color='lightblue'> benchtemp.EarlyStopMonitor</font>**

Example:
```python
from benchtemp.utils import EarlyStopMonitor

...
early_stopper = EarlyStopMonitor(max_round=args.patience)
for epoch in range(args.epochs):
    ...
    val_ap = model(val_datasets)
    if early_stopper.early_stop_check(val_ap):
        break
    ...
...
```

### Evaluator

**Link Prediction** Evaluation Metrics  are **Area Under the Receiver Operating Characteristic Curve (ROC AUC)** and **average precision (AP)**

**Node Classification** Evaluation Metric is **Area Under the Receiver Operating Characteristic Curve (ROC AUC)**

Class: 

**Evaluator(task_name: str = "LP")**

Parameters:
- task_name <font color='lightblue'>: str </font> - the name of the task, choice in **["LP", "NC"]**.

Returns:
- **<font color='lightblue'> benchtemp.Evaluator</font>**

Example:

```python
from benchtemp.utils import Evaluator

# For example, Link prediction task. Evaluation Metrics: AUC, AP.
evaluator = Evaluator("LP")

...
# test data
pred_score = model(test_data)
test_auc, test_ap = Evaluator.eval(pred_score, true_label)
...
```

```python
from benchtemp.utils import Evaluator

# For example, Node Classification task. Evaluation Metrics: AUC.
evaluator = Evaluator("NC")

...
# test data
pred_score = model(test_data)
test_auc = Evaluator.eval(pred_score, true_label)
...
```

## Call for Contributions

**BenchTeMP** project is looking for contributors with 
expertise and enthusiasm! If you have a desire to contribute to **BenchTeMP**, 
please contact [BenchTeMP team](mailto:jonnyhuanghnu@gmail.com).