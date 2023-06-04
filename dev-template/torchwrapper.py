from sklearn.base import BaseEstimator

import torch
from torch.nn import functional as F

# 
class TorchWrapper(BaseEstimator):
    def __init__(self, net, X_size, device):
        super().__init__()
        self.net = net
        self.X_size = X_size
        self.device = device

    def fit(self, X, y, **kwargs):
        # the estimator is already fitted
        return self
    
    def get_params(self, deep: bool = True) -> dict:
        params = dict()
        params["net"] = self.net
        params["X_size"] = self.X_size
        params["device"] = self.device 
        return params

    def set_params(self, **params):
        self.net = params["net"]
        self.X_size = params["X_size"]
        self.device = params["device"]
        
    def predict(self, x):
        if torch.is_tensor(x) == False:
            return torch.argmax(self.predict_proba(torch.tensor(x)), dim = 1).numpy()
        else:
            return torch.argmax(self.predict_proba(x), dim = 1)
    
    def predict_proba(self, x):
        if torch.is_tensor(x) == False:
            x = torch.tensor(x)
            x = self(x)
            x = F.softmax(x, dim = 1).numpy()
        else:
            x = self(x)
            x = F.softmax(x, dim = 1)
        return x

    def forward(self, x):
        no_tensor = False
        if torch.is_tensor(x) == False:
            x = torch.tensor(x)
            no_tensor = True

        x = torch.reshape(x, self.X_size )
        
        preds = torch.zeros( x.size(0), self.net.output_size)
        step = 128

        for i in range(0, x.size(0), step):
            if i + step > x.size(0):
                step = x.size(0) - i 
            
            preds[i:i+step] = self.net( x[i:i+step].to(self.device) ).detach().cpu()

        if no_tensor == True:        
            return preds.numpy()

        return preds
    
    def __call__(self, x): 
        return self.forward(x)

    def score(self, X, y):
        y_preds = self.predict(X)
        
        if torch.is_tensor(y) == False:    
            y = torch.tensor(y)

        if torch.is_tensor(y_preds) == False:    
            y_preds = torch.tensor(y_preds)
        
        acc = (y_preds == y).float().sum()
        acc = acc / len(y)

        return float(acc.item())
