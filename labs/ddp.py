import os, json
import torch
import torch.distributed as dist
from torch import nn
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import TensorDataset, DataLoader, DistributedSampler
def main():
    if not torch.cuda.is_available(): raise RuntimeError('Requires Linux and CUDA GPUs')
    rank=int(os.environ['RANK']);local=int(os.environ['LOCAL_RANK'])
    torch.cuda.set_device(local)
    dist.init_process_group('nccl')
    try:
        torch.manual_seed(19)
        x=torch.randn(128,8);y=x[:,:2]*.5
        dataset=TensorDataset(x,y)
        sampler=DistributedSampler(dataset,shuffle=True,drop_last=True)
        loader=DataLoader(dataset,batch_size=8,sampler=sampler)
        model=DDP(nn.Linear(8,2).cuda(local),device_ids=[local])
        opt=torch.optim.SGD(model.parameters(),lr=.05)
        for epoch in range(3):
            sampler.set_epoch(epoch)
            total=torch.zeros(2,device=local)
            for bx,by in loader:
                bx=bx.cuda(local);by=by.cuda(local)
                opt.zero_grad(set_to_none=True)
                loss=(model(bx)-by).square().mean()
                loss.backward();opt.step()
                total[0]+=loss.detach()*len(bx);total[1]+=len(bx)
            dist.all_reduce(total)
            if rank==0: print(json.dumps({'epoch':epoch,'global_mean_loss':(total[0]/total[1]).item(),
             'effective_batch':8*dist.get_world_size()}))
        flat=torch.cat([p.detach().flatten() for p in model.parameters()])
        reference=flat.clone()
        dist.broadcast(reference,src=0)
        torch.testing.assert_close(flat,reference)
    finally:
        dist.destroy_process_group()
if __name__=='__main__': main()
