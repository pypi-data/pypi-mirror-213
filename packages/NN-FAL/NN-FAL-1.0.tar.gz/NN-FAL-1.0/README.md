# NNFal

A neural network-based falsification framework for falsifying several CPS models such as hybrid automata and Simulink models. The algorithm accepts two inputs: a safety property and a neural network model that acts as an approximation model of the CPS models. It includes the DNNF and DNNV as neural network falsifier frameworks for obtaining counterexample. XSpeed is used for validating the counterexample for hybrid automata models and the counterexample of the Simulink model is verified using MATLAB. The following safety violating trajectory is generated from an instance of Navigation benchmarks by NNFal.

<img src="./figs/NAV_30_P1.png" width = "256" height = "256"/>


# Prerequisites
NNFal requires the following packages...

- [XSpeed-plan](https://gitlab.com/Atanukundu/XSpeed-plan) for simulating and validating the hybrid automata models.

- [MATLAB](https://in.mathworks.com/products/simulink.html) for simulating and validating the state-flow/Simulink models.

- [MATLAB engine](https://in.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html) for Python. From a Python script, we can call Simulink model through MATLAB Engine API.
 	 
- [DNNF](https://github.com/dlshriver/dnnf) for obtaining counterexample input from the deep neural networks .
  	 
- [DNNV](https://github.com/dlshriver/DNNV) for obtaining counterexample input for the reachability property falsifier.
    	 
   	 
# Installation
    
- Allow default installation of the library header files into the directory /usr/local/include and the .a/.so files into the directory /usr/local/lib.

- Assume MATLAB is installed in your machine.

- Clone the [XSpeed-plan](https://gitlab.com/Atanukundu/XSpeed-plan) repository into the validation directory of NNFal and build it from the source (Instructions are given in the XSpeed repo).

- Install DNNF using the following command or install from source [DNNF](https://github.com/dlshriver/dnnf).

```bash
$ pip3 install dnnf
```

- Install DNNV using the following command or install from source [DNNV](https://github.com/dlshriver/DNNV).
```bash
$ pip3 install dnnv
```
- INstall NNENUM using the command, for more details see [NNENUM installation](https://github.com/dlshriver/DNNV) in DNNV framework.
```bash
$ dnnv_manage install nnenum
```

- Install matlab engine for python using the command:
```bash
$ pip3 install matlabengine==9.13.7
```

# Run

usage: NNFal.py [-h] --property PROPERTY --network NETWORK --CPS_type CPS_TYPE
                [--model MODEL] [--config CONFIG] [--initial INITIAL]
                --scaling SCALING --falsifier FALSIFIER

optional arguments:
```bash
  -h, --help            	show this help message and exit
  
  --property PROPERTY   	Safety property in DNNP.
  
  --network NETWORK     	Neural network in ONNX.
  
  --CPS_type CPS_TYPE   	CPS type i.e HA or MATLAB.
   
  --model MODEL         	Model file (XML) of the HA model required for validation.
  
  --config CONFIG       	Config file (cfg) of the HA model required for validation.
  
  --initial INITIAL     	Initial config file (py) for the matlab model required for validation.
  
  --scaling SCALING     	Mention the dataset/model for inv_scalling(CE).
  
  --falsifier FALSIFIER		Falsifier should be in lower case latter: pgd, nnenum
```

- An example for running an instance of NAV benchmark (HA) using the following command:

```bash
$ python3 NNFal.py --property ../property/NAV/NAV_30/property_11.py --network ../network/NAV/NAV_30/NAV_30_NN-1.onnx --falsifier pgd --scaling NAV_30_NN --CPS_type HA --model ../validation/XSpeed-plan/benchmarks/NNFal/30.xml --config ../validation/XSpeed-plan/benchmarks/NNFal/30_1.cfg
```
	
- An example for running an instance of Chasing cars benchmark (Simulink model) using the following command:
```bash
$ python3 NNFal.py --property ../property/Chasing_cars/property_111.py --network ../network/Chasing_cars/CC_v1.onnx --falsifier nnenum --scaling CC --CPS_type MATLAB --initial ../validation/matlab/CC/initial_CC.py
```

- Run the following Python scripts in the NNFal/source directory. It automatically stores the result in a .csv file in the same directory.
```bash
$ python3 run_instancePGD.py
or,
$ python3 run_instanceNNENUM.py
```

- Additional Python libraries and runlim are required to run the aforementioned scripts.
    
    
# Author and Contact

    Atanu Kundu
    E-mail: mcsak2346@iacs.res.in




