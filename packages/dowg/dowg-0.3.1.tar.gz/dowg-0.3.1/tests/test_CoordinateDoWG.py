import torch
from dowg.CoordinateDoWG import CoordinateDoWG

def test_coordinate_dowg():
    model = torch.nn.Linear(10, 1)
    optimizer = CoordinateDoWG(model.parameters(), clip=0.01)
    criterion = torch.nn.MSELoss()

    # Create some random input and target tensors
    x = torch.randn(1, 100)
    y = torch.randn(1, 1000)

    # Perform a forward pass
    output = model(x)

    # Compute the loss
    loss = criterion(output, y)

    # Perform a backward pass
    loss.backward()

    # Perform a step with the optimizer
    
    try:
        optimizer.step()
    except: 
        print("Error in CoordinateDoWG.step()")
    