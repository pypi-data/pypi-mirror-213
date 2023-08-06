import torch
"""    Specification:
    
    Adaptively sets the thresholds for each coordinate: ACClip ( τ k , m k ) = min { τ k | m k | + ϵ , 1 } m k , τ α k = β 2 τ α k − 1 + ( 1 − β 2 ) | g k | α , (ACClip) where operations are element-wise, ϵ is a small number for numerical stability, and we set α = 1 by default. The use of a coordinate-wise α -moment (as opposed to the traditional second moment) is motivated by our theory and estimates B = E [ | g α k | ] 1 / α in Assumption 2. Since E [ | g α k | ] 1 / α is increasing in α ≥ 1 , using α = 1 is a conservative bound on B when the true α is unknown.    
"""

def clip_gradient(grad, k=0.5):
    return grad.clamp(-k, k)
def ac_clip_gradient(grad, params, clip_factor):
    param_norm = torch.norm(torch.cat([param.view(-1) for param in params]))
    
    # Compute the maximum allowed gradient norm
    max_grad_norm = clip_factor * param_norm
    
    # Compute the norm of the gradients
    grad_norm = torch.norm(grad.view(-1))
    
    if grad_norm > max_grad_norm:
        # If gradient norm is greater than the maximum allowed norm, clip the gradient
        grad = grad * (max_grad_norm / (grad_norm + 1e-6))
    
    return grad