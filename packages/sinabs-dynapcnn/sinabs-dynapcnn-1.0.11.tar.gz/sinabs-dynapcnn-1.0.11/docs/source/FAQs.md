# FAQs

## 1. What network structure can I define?
A: Auto-converison from a sinabs model to `DynapcnnNetwork` model is only supported for the *nn.Sequential* model structure. The skip and recurrent structure between DYNAPCNN cores are supported through low level-api ie. manually updating the configuration object.

## 2. What kinds of neural network operation I can use in Speck/DYNAP-CNN?
A: Currently we only support Conv2d, Avgpool, Sumpool, Linear, Flatten, and the IAF activation

## 3. What execution order should I be aware of when I am implementing a sequential structure?
A: You should be aware with the internal layer order. DYNAP-CNN techonology defines serveral layers that can be communicates each other. In a layer, the Convolution and Neuron activation must be implemented with **Conv-->IAF order-->pool(optional)** order. The cascaded convolution and neuron activation in a DYNAPCNN layer is not allowed.

![dataflow](_static/Overview/dataflow_layers.png)

### Ex1. Bad Case: Cascaded convlution
```

network = nn.sequential([
                        nn.conv2d(),
                        nn.conv2d(),
                        IAFsqueeze(),
                        ])
                    
```
### Ex2. Bad Case: None sequential
```

class Network:
    
    def __init__(self):
        self.conv1 = nn.conv2d()
        self.iaf = IAFsqueeze()
    def forward(self, x):
        out = self.conv1(x)
        out = self.iaf(out)
        return out
                    
```

### Ex3. Bad Case: Use unsupport operation

```
network = nn.sequential([
                        nn.conv2d(),
                        nn.BatchNorm2d(), # unspport in speck/dynapcnn
                        IAFsqueeze(),
                        ])
```

### Ex3. Good Case: Use unsupport operation

```
network = nn.sequential([
                        nn.conv2d(),
                        IAFsqueeze(),
                        nn.pool(),
                        # up to here is using 1 dynapcnn layer
                        nn.conv2d(),
                        IAFsqueeze(),
                        nn.Flatten(),
                        nn.Linear(),
                        IAFsqueeze(),
                        # up to here is using 2 dynapcnn layer
                        ])
```


## 4. What is the limination for network sizing?
A: we introduced the neuron memory and kernel memory constraints in the design. Apart from these:
* maximumlly using **9** dynapcnn layer
* convolution channel number < **1024**
* convolution kernel size < **16**
* pool size = [1, 2, 4, 8]
* if you are using readout layer, the number of output class should< **15**

## 5. Known dev-kit bugs

A. Channel index mapping error between the output DYNAP-CNN layer and readout block(on Speck2e/2f), for details see [here](https://synsense.gitlab.io/sinabs-dynapcnn/notebooks/using_readout_layer.html)


## 6. How to use the leak-neuron

A: This [tutorial:](getting_started/notebooks/leak_neuron) explains the steps involved in using leak on the SCNN cores.


## 7. Is my network compatible with my dev-kit/chip?
A: Once you have a network you can follow the below steps to check if it is compatible with your device;

```
...
# If you are starting from an ANN definition
my_ann = nn.Sequential(...)
my_snn = sinabs.from_model(my_network, input_shape)

# Restructure your SNN into a Dynapcnncnn Core structure
my_dynapcnn_network = DynapcnnNetwork(my_snn, input_shape)

# Check if your netowrk is compatible with a given chip
assert my_dynapcnn_network.is_compatible_with("speck2fmodule")

...
```

## 8. How do I list all connected devices and their IDs?
A: Once your devices are connected, you can use the `get_device_map` method to inspect them.

```python
from sinabs.backend.dynapcnn.io import get_device_map

device_map: Dict[str, `DeviceInfo`] = get_device_map()

print(device_map)
```

This should produce an output that looks something like below:

```
>>> {'speck2edevkit:0': device::DeviceInfo(serial_number=, usb_bus_number=0, usb_device_address=5, logic_version=0, device_type_name=Speck2eDevKit)}
```