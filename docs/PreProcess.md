# Definitions

* User interaction:  has the items an user have interacted with, and the timestamp of the interaction

!!! success "Example of user interaction"
    ```py
    // The first entry is the timestamp and the second is the product id
    User[user_id] = [[15465464, 2], [15465469, 257], [15465499, 3457]]
    ```

# Data management 

## Data cleaning

The datasets are obtained from [Amazon Reviews](Datasets.md#amazon-reviews). The original structure of the datasets is `json` but they are preprocessed so that the output format is:

!!! success "Output dataset"
    [User ID]   [Product ID]
    1           354
    1           247

Each item listed for the given user appears in the order given by the timestamp.

## Data partition for training, validation and testing

For training, validation and testing the data is partitioned in the following manner:

* Given a [User Interaction](#definitions) of size `N` the trainining set is obtained from the first `N-2` samples
* Given a [User Interaction](#definitions) of size `N` the validation set is obtained from the sample before the last.
* Given a [User Interaction](#definitions) of size `N` the test set is obtained from the last sample.