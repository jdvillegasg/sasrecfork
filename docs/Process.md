# Sampling

The function `sample_function()` is responsible for sampling the preprocessed [Training Dataset](PreProcess.md#partitioning-for-training).

To do so, the function creates `U` (see [Definitions](PreProcess.md#definitions)) batches of 'ready to train data' (I will shortly explain what does that mean) for each single user.

The function executes endlessly (until the under-the-hood processes are stopped). When it has created `U` different batches for each user, it takes the [Training Dataset](PreProcess.md#partitioning-for-training) and shuffles it randomly, and start over. 

!!! success "Note"
    The pytorch implementation differs and improves on the original tensorflow implementation, since the original implementation creates each batch for a random user without guaranteeing that there won't be users picked up multiple times. This situation is *unlikely* to happend but *can* happen due to the random choice of users.

