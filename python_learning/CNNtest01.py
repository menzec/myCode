# -*- coding: utf-8 -*-
# @Date    : 2018-07-13 14:07:43
# @Author  : Menzecheng (Menzc@outlook.com)
# @Link    : NULL
# @Version : $Id$

import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import torch.nn as nn
import torch.nn.functional as F


path = 'D:\\data'

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = torchvision.datasets.CIFAR10(path, train=True,
                                        download=False, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(path, train=False,
                                       download=False, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4,
                                         shuffle=False, num_workers=2)
classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# functions to show an image

def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))



# get some random training images
if __name__ == '__main__':
  dataiter = iter(trainloader)
  images, labels = dataiter.next()


# show images
if __name__ == '__main__':
  imshow(torchvision.utils.make_grid(images))
  # print labels
  print(' '.join('%5s' % classes[labels[j]] for j in range(4)))


# 2. Define a Convolution Neural Network
class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()  #b,3,32,32
        layer1 = nn.Sequential()
        layer1.add_module('conv1',nn.Conv2d(3,32,3,1,padding=1))#b,32,32,32
        layer1.add_module('relu1',nn.ReLU(True))
        layer1.add_module('pool1',nn.MaxPool2d(2,2)) #b,32,16,16
        self.layer1 = layer1

        layer2 = nn.Sequential()
        layer2.add_module('conv2',nn.Conv2d(32,64,3,1,padding=1))#b,64,16,16
        layer2.add_module('relu2',nn.ReLU(True))
        layer2.add_module('pool2',nn.MaxPool2d(2,2)) #b,64,8,8
        self.layer2=layer2

        layer3 = nn.Sequential()
        layer3.add_module('conv3',nn.Conv2d(64,128,3,1,padding=1))#b,128,8,8
        layer3.add_module('relu3',nn.ReLU(True))
        layer3.add_module('pool3',nn.MaxPool2d(2,2)) #b,128,4,4
        self.layer3 = layer3

        layer4=nn.Sequential()
        layer4.add_module('fc1',nn.Linear(2048,512))
        layer4.add_module('fc_relu1',nn.ReLU(True))
        layer4.add_module('fc2',nn.Linear(512,64))
        layer4.add_module('fc_relu2',nn.ReLU(True))
        layer4.add_module('fc3',nn.Linear(64,10))
        self.layer4 = layer4
    def forward(self,x):
        conv1 = self.layer1(x)        
        conv2 = self.layer2(conv1)
        #print('conv2',conv2.size())
        conv3 = self.layer3(conv2)
        #print('conv3',conv3.size())
        fc_input = conv3.view(conv3.size(0),-1)
        fc_out = self.layer4(fc_input)
        #print('x.size(),conv1.size(),conv2.size(),conv3.size(),fc_input.size(),fc_out.size()\n',x.size(),conv1.size(),conv2.size(),conv3.size(),fc_input.size(),fc_out.size())
        return fc_out


net = Net()

print(net)
########################################################################
# 3. Define a Loss function and optimizer
import torch.optim as optim

#criterion = nn.CrossEntropyLoss()
#optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

optimizer = torch.optim.Adam(net.parameters())
criterion = torch.nn.CrossEntropyLoss()
########################################################################
# 4. Train the network
if __name__ =='__main__':
  for epoch in range(2):  # loop over the dataset multiple times

      running_loss = 0.0
      for i, data in enumerate(trainloader, 0):
          # get the inputs
          inputs, labels = data

          # zero the parameter gradients
          optimizer.zero_grad()
          
          # forward + backward + optimize
          outputs = net(inputs)
          loss = criterion(outputs, labels)
          loss.backward()
          optimizer.step()

          # print statistics
          running_loss += loss.item()
          if i % 2000 == 1999:    # print every 2000 mini-batches
              print('[%d, %5d] loss: %.3f' %
              (epoch + 1, i + 1, running_loss / 2000))
              running_loss = 0.0


print('Finished Training')

########################################################################
# 5. Test the network on the test data

if __name__ == '__main__':
  dataiter = iter(testloader)
  images, labels = dataiter.next()

  # print images
  imshow(torchvision.utils.make_grid(images))
  print('GroundTruth: ', ' '.join('%5s' % classes[labels[j]] for j in range(4)))

  outputs = net(images)
  _, predicted = torch.max(outputs, 1)

  print('Predicted: ', ' '.join('%5s' % classes[predicted[j]]
                              for j in range(4)))
  # The results seem pretty good.
  correct = 0
  total = 0
  with torch.no_grad():
      for data in testloader:
          images, labels = data
          outputs = net(images)
          _, predicted = torch.max(outputs.data, 1)
          total += labels.size(0)
          correct += (predicted == labels).sum().item()

  print('Accuracy of the network on the 10000 test images: %d %%' % (
      100 * correct / total))

class_correct = list(0. for i in range(10))
class_total = list(0. for i in range(10))
if __name__ == '__main__':
  with torch.no_grad():
      for data in testloader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs, 1)
        c = (predicted == labels).squeeze()
        for i in range(4):
          label = labels[i]
          class_correct[label] += c[i].item()
          class_total[label] += 1

  for i in range(10):
    print('Accuracy of %5s : %2d %%' % (
      classes[i], 100 * class_correct[i] / class_total[i]))
