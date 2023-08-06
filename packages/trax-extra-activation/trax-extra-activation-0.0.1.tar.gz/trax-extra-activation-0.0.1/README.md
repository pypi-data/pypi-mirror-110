# Trax Extra Activation Functions
Extra activation functions for [Trax](https://github.com/google/trax)

<code>pip install trax-extra-activation</code>

## How to use
You can use activation functions in the same way as that ones implemented in Trax.

```python
from trax_extra_activation import TanhExp
model = tl.Serial(
    tl.Embedding(vocab_size=8192, d_feature=256),
    tl.Mean(axis=1),
    tl.Dense(2),
    TanhExp()
)
```

## Activations
- HardShrink
  ```python
  HardShrink(lmbda: float = 0.5) -> PureLayer
  ```
  - [PyTorch Document](https://pytorch.org/docs/stable/generated/torch.nn.Hardshrink.html#torch.nn.Hardshrink)
- HardSwish
  ```python
  HardSwish() -> PureLayer
  ```
  - [PyTorch Document](https://pytorch.org/docs/stable/generated/torch.nn.Hardswish.html#torch.nn.Hardswish)
- LogSigmoid
  ```python
  LogSigmoid() -> PureLayer
  ```
  - [PyTorch Document](https://pytorch.org/docs/stable/generated/torch.nn.LogSigmoid.html#torch.nn.LogSigmoid)
- Relu6
  ```python
  Relu6() -> PureLayer
  ```
  - [PyTorch Doument](https://pytorch.org/docs/stable/generated/torch.nn.ReLU6.html#torch.nn.ReLU6)
- Celu
  ```python
  Celu(a: float = 1.0) -> PureLayer
  ```
  - [PyTorch Document](https://pytorch.org/docs/stable/generated/torch.nn.CELU.html#torch.nn.CELU)
- Silu
  ```python
  Silu() -> PureLayer
  ```
  - [PyTorch Document](https://pytorch.org/docs/stable/generated/torch.nn.SiLU.html#torch.nn.SiLU)
- Mish
  ```python
  Mish() -> PureLayer
  ```
  - [PyTorch Document](https://pytorch.org/docs/stable/generated/torch.nn.Mish.html#torch.nn.Mish)
- SoftShrink
  ```python
  SoftShrink(lmbda: float = 0.5) -> PureLayer
  ```
  - [PyTorch Document](https://pytorch.org/docs/stable/generated/torch.nn.Softshrink.html#torch.nn.Softshrink)
- SoftSign
  ```python
  SoftSign() -> PureLayer
  ```
  - [PyTorch Document](https://pytorch.org/docs/stable/generated/torch.nn.Softsign.html#torch.nn.Softsign)
- TanhShrink
  ```python
  TanhShrink() -> PureLayer
  ```
  - [PyTorch Document](https://pytorch.org/docs/stable/generated/torch.nn.Tanhshrink.html#torch.nn.Tanhshrink)
- TanhExp
  ```python
  TanhExp() -> PureLayer
  ```
  - [Paper](https://arxiv.org/abs/2003.09855)
