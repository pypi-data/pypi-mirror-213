"# microtinygrad" 

 Micro Tiny neural network library that allows training of simple neural networks through mini-batch gradient descent only using numpy and pandas. Currently only provides support for pandas dataframes. Useful if you want to train small neural networks and quick tuning of hyperaparameters. 
 # Motivation

 In order to learn what goes on under the hood of neural network's backpropagation, I decided to implement it myself. However, my algorithm provides a more analytical solution (Calculating closed form gradients), rather than the approaches used by other neural network libaries (Micrograds Value Tree). Thus, this only currently supports common neural network patterns Linear Activation/Regression amd SoftMax Cross Entropy.  
 

 # Simple Quick Start 

```javascript I'm tab B
nn = NeuralNetwork()
```


 