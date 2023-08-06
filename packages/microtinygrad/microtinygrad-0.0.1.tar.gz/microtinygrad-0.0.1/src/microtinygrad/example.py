import numpy as np
import pandas as pd

def relu(x):
    return np.where(x > 0, x, 0)
def drelu(x):
    return np.where(x > 0, 1,0)
def mse(t,p):
    """
    Returns mean sqaured error given two arrays of the same length
    """
    return sum((t-p)**2)/len(t)

def softmax(x):
    # assumes x is a vector

    return np.exp(x) / np.sum(np.exp(x))


class NeuralNetwork:
    def __init__(self,hidden = []) -> None:
        self.sizes = hidden
        self.biases = None
        self.weights = None
        self.type = None
        self.map = {}
    # detects what type of model we want and constructs our bias,weights,type and map dependent on the dataframe and series given
    def construct(self,X,Y):
        inputsize = X.shape[1]
        self.sizes.insert(0,inputsize)
        unique_values = len(Y.unique())
        self.sizes.append(unique_values)
        self.type = 'classification'
        self.map = {index: value for index, value in enumerate(Y.unique())}
        self.biases = [np.zeros((y, 1)) for y in self.sizes[1:]]
        self.weights = [np.random.randn(y, x) * np.sqrt(2/x) for x, y in zip(self.sizes[:-1],self.sizes[1:])]

    # Helper for train function
    # Feeds our input into our neural network and determines the loss 
    def forward(self,input,answers):
        ## Input is supposed to be the training matrix
        input = input.T
        for b, w in zip(self.biases, self.weights):
            dot = np.dot(w, input)+b
            if np.array_equal(self.biases[len(self.biases) - 1] ,b):
                if self.type == 'classification':
                    input = softmax(dot.T)
            else:
                input = relu(dot)
        # input is now the output activation
        # If the type is regression, then the length of the output activation should be 1. 
        if self.type == 'classification':
            ## Accuracy instead of loss 
            currentsum = 0
            for row,index in zip(input,answers):
                if np.argmax(row) == index:
                    currentsum += 1
            loss = currentsum
        return  loss
    
    # Returns a tuple of dw,db, which are layer by layer arrays that represent partials
    def backprop(self,inputx,inputy):
        # input x is a 1d vector ,input y is a scalar
        partialb = [np.zeros(b.shape) for b in self.biases]
        partialw = [np.zeros(w.shape) for w in self.weights]
        storedsums = []
        input = inputx.reshape(inputx.size,1)
        storedactivations = [input.T]
        # Forward propagation, storing the su
        for b, w in zip(self.biases, self.weights):
            dot = np.dot(w, input)+b
            storedsums.append(dot)
            ## If we are on the last iteration, then our activation function is linear if its regression, or softmax if its classification
            if np.array_equal(self.biases[len(self.biases) - 1] ,b):
                if self.type == 'classification':
                    ## Ensure no overflow
                    input = softmax(dot.T)
            else:
                input = relu(dot)
            storedactivations.append(input.T)
        ## Actual backpropagation
        #First Layer
        ## Regression case. Thus, the activation for our output for our output layer is linear. Our loss function is mean square error, thus delta (dL/dz) is -2(y-z).
        ## Classification case. Delta of the output layer is dependent on the output layer. Credit to https://towardsdatascience.com/derivative-of-the-softmax-function-and-the-categorical-cross-entropy-loss-ffceefc081d1 for doing the dirty work
        if self.type == 'classification':
            dz = storedactivations[-1]
            dz[inputy] = dz[inputy] - 1
            assert dz.shape == partialb[-1].shape
            partialb[-1] = dz
            dw = np.dot(dz, storedactivations[-2])
            assert dw.shape == partialw[-1].shape
            partialw[-1]= dw
        
        # Finding partials for the rest of the layers
        for i in range(2,len(self.sizes)): 
            dz = drelu(storedsums[-i])

            delta = np.dot(self.weights[-i + 1].T,partialb[-i + 1]) * dz
            assert delta.shape == partialb[-i].shape
            partialb[-i] = delta   
            weight = np.dot(delta, storedactivations[-i - 1])
            assert weight.shape == partialw[-i].shape
            partialw[-i] = weight
        return (partialw,partialb)

    # Updates our weights and biases with a given batch
    def updatebatch(self,batchx,batchy,learningrate = 0.01):
        ## Assumptions these are numpy arrays

        currentsumb = [np.zeros(b.shape) for b in self.biases]
        currentsumw = [np.zeros(w.shape) for w in self.weights]
        batchx = batchx.values

        for x,y in zip(batchx,batchy):
            gradientw,gradientb = self.backprop(x,y)
            for i in range(len(currentsumb)):
                currentsumb[i] = (gradientb[i] + currentsumb[i])
                currentsumw[i] = (gradientw[i] + currentsumw[i])
        
        for i in range(len(currentsumb)):
            self.weights[i] = self.weights[i] - (learningrate/len(batchy)) * currentsumw[i]
            self.biases[i] = self.biases[i] - (learningrate/len(batchy)) * currentsumb[i]
    

            
    def train(self,X,Y,batchsize = 32,epoch = 10,testx = None,testy = None):
        assert isinstance(X, pd.DataFrame) 
        assert isinstance(Y,pd.Series)
        # Constructs the array for training and test error
        self.construct(X,Y)
        if testx and testy:
            testloss = [self.forward(testx,testy)]
        trainingloss = [self.forward(X,Y)]
        print(trainingloss)
        if self.type == 'classification':
            Y = pd.factorize(Y)[0]
        minibatchesX = np.array_split(X, len(X) // batchsize)
        minibatchesY = np.array_split(Y, len(Y) // batchsize)
        #split dataframe into batches of size batchsize
        for i in range(epoch):
            for x,y in zip(minibatchesX,minibatchesY):
                self.updatebatch(x,y)
            
            if self.type == 'classification':
                print('Your training accuracy after epoch ' + str(i + 1) + ' is ' + str(self.forward(X,Y)))
                if testx and testy:
                    print('Your test accuracy after epoch ' + str(i + 1) + ' is ' + str(self.forward(testx,testy)))

                


            