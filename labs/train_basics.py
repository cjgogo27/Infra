import torch
from torch import nn
torch.manual_seed(7)
torch.set_num_threads(1)
x = torch.randn(8, 3)                         # 8 samples, 3 features
target = x[:, :1] * 2 - x[:, 1:2]            # [8, 1] synthetic targets
model = nn.Linear(3, 1)                      # weight [1, 3], bias [1]
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
before = model.weight.detach().clone()
optimizer.zero_grad(set_to_none=True)
prediction = model(x)                        # forward: [8, 1]
loss = (prediction - target).square().mean()
loss.backward()                             # computes gradients, not an update
assert torch.equal(before, model.weight)
print('shapes:', x.shape, prediction.shape, model.weight.shape)
print('gradient:', model.weight.grad.tolist())
optimizer.step()                            # updates the parameters
assert not torch.equal(before, model.weight)
print('weight_before:', before.tolist())
print('weight_after:', model.weight.detach().tolist())
initial = loss.item()
for _ in range(29):
    optimizer.zero_grad(set_to_none=True)     # omit this to accumulate gradients
    loss = (model(x) - target).square().mean()
    loss.backward()
    optimizer.step()
final = (model(x) - target).square().mean().item()
assert final < initial
print({'initial_loss': initial, 'final_loss': final, 'updates': 30})
