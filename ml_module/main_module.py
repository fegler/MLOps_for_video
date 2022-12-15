import pytorch_lightning as pl 
import torch.nn as nn 
import torch.nn.functional as F
import torchvision.models as models 
import torch 

### ML part sample code 
# ResNet model code 

class ResnetModule(pl.LightningModule):
    def __init__(self, n_layer:int = 34, n_class:int = 10):
        super().__init__()
        fc_in_channel = 512
        if n_layer == 34: 
            self.model = models.resnet34(pretrained=True)
        elif n_layer == 50:
            self.model = models.resnet50(pretrained=True)
            fc_in_channel = 2048
        elif n_layer == 18:
            self.model = models.resnet18(pretrained=True)
        
        ## remove original fc layer
        self.model = nn.Sequential(*list(self.model.children())[:-1])
        self.fc = nn.Linear(fc_in_channel, n_class, bias=True)
    
    def forward(self, x):
        return self.fc(self.model(x).squeeze())
    
    def training_step(self, batch, batch_idx):
        x, y = batch 
        pred = self.fc(self.model(x).squeeze(2).squeeze(2))
        pred = F.softmax(pred, dim=1)
        loss = F.cross_entropy(pred, y)
        return loss 

    def predict_step(self, batch, batch_idx):
        x, y = batch 
        pred = self.fc(self.model(x).squeeze(2).squeeze(2))
        pred = F.softmax(pred, dim=1)
        return pred.numpy()
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-4)