import torch


def clip_gradient(grad:torch.tensor, k: float = 1.0):
    """Clips the gradients based on the kth percentile of their absolute values.
    
    Args:
        grad (torch.Tensor): The gradients to be clipped.
        k (float): The percentile of gradients to keep.

    Returns:
        torch.Tensor: The clipped gradients.
    """
    assert k >= 0 and k <= 1, "k must be between 0 and 1. Got {}".format(k)

    grad = grad.flatten()
    kth = int(k * len(grad))
    threshold = torch.topk(torch.abs(grad), kth)[0][-1]
    clipped_grad = torch.clamp(grad, -threshold, threshold)
    return clipped_grad.reshape(grad.shape)    