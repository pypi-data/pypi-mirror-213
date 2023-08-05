import numpy as np
import tensorflow as tf

class RNNModel:
    def __init__(self, input_shape, output_shape, num_units, num_layers):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.num_units = num_units
        self.num_layers = num_layers
        
        # Define the RNN architecture
        self.model = tf.keras.Sequential()
        for i in range(num_layers):
            if i == 0:
                # Add the first layer with input_shape
                self.model.add(tf.keras.layers.SimpleRNN(units=num_units, 
                                                         activation='tanh', 
                                                         return_sequences=True, 
                                                         input_shape=input_shape))
            elif i == num_layers - 1:
                # Add the last layer with output_shape
                self.model.add(tf.keras.layers.SimpleRNN(units=num_units, 
                                                         activation='tanh', 
                                                         return_sequences=False))
            else:
                # Add the intermediate layers
                self.model.add(tf.keras.layers.SimpleRNN(units=num_units, 
                                                         activation='tanh', 
                                                         return_sequences=True))
                
        # Add the output layer with output_shape and softmax activation
        self.model.add(tf.keras.layers.Dense(units=output_shape, activation='softmax'))
        
        # Compile the model with categorical crossentropy loss and adam optimizer
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    def fit(self, X_train, y_train, epochs, batch_size):
        # Convert y_train to one-hot encoding
        y_train = tf.keras.utils.to_categorical(y_train, num_classes=self.output_shape)
        
        # Fit the model to the training data
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
    
    def predict(self, X_test):
        # Make predictions on the test data
        y_pred = self.model.predict(X_test)
        
        # Convert predictions to class labels
        y_pred_labels = np.argmax(y_pred, axis=1)
        
        return y_pred_labels
