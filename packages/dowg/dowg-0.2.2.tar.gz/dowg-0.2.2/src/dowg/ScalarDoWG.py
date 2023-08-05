import torch

from .clip import clip_gradient


class ScalarDoWG(torch.optim.Optimizer):
    def __init__(self, params, eps=1e-4, clip=0.01, *args, **kwargs):
        defaults = dict(epsilon=1-eps, lr=1, clip=clip)
        self.epsilon = 1-eps
        super(ScalarDoWG, self).__init__(params, defaults)

    def step(self, closure=None):
        
        state = self.state
        loss = None
        if closure is not None:
            loss = closure()
    
            if "rt2" not in state:
                state["rt2"] = torch.Tensor([self.epsilon])
            if "vt" not in state:
                state["vt"] = torch.Tensor([0])
    
            grad_sq_norm = torch.Tensor([0])
            curr_d2 = torch.Tensor([0])
    
            with torch.no_grad():
                for idx, group in enumerate(self.param_groups):
                    group_state = state[str(idx)]  # convert idx to a string
                    if "x0" not in group_state:
                        group_state["x0"] = [torch.clone(p) for p in group["params"]]
        
                    grad_sq_norm += torch.stack(
                        [(p.grad**2).sum() for p in group["params"]]
                    ).sum()
                    curr_d2 += torch.stack(
                        [
                            ((p - p0) ** 2).sum()
                            for p, p0 in zip(group["params"], group_state["x0"])
                        ]
                    ).sum()
        
                state["rt2"] = torch.max(state["rt2"], curr_d2)
                state["vt"] += state["rt2"] * grad_sq_norm
                rt2, vt = state["rt2"], state["vt"]
    
            for group in self.param_groups:
                for p in group["params"]:
                    gt_hat = rt2 * clip_gradient(p.grad.data.clone(), group["clip"])
                    denom = torch.sqrt(vt).add_(group["epsilon"])
                    p.addcdiv_(gt_hat, denom, value=-1.0)
        return loss