import torch


def LoadModel():
    #model = torch.hub.load(r'./yolo', 'custom', path=r'./BeeWeights.pt', source='local')
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'./Data/FlyingMovies/BeeWeights.pt')
    return model