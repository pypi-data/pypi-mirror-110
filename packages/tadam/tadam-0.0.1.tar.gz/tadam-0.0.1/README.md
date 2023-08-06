## TAdam

The Pytorch implementation of TAdam algorithm in：'A decreasing scaling transition scheme from Adam to SGD'
[https://arxiv.org/abs/2106.06749](https://arxiv.org/abs/2106.06749)

### Usage

```python
from tadam import TAdam

...

optimizer = TAdam(model.parameters(), iters=required, lr=1e-3, moment=1/4, up_lr=0.3, low_lr=0.01)


#iters(int, required): iterations
#	iters = (testSampleSize / batchSize) * epoch
#
#moment(float, optional): transition moment
#       moment = transition_iters / iters

#set default value: moment=1/4, up_lr=0.3, low_lr=0.01
```





The code will be uploaded as soon as possible

