Analyze *in vivo* raw data
===

## How to launch the experiments
- Preparations:  
1. You should have the raw data then save them in the directory **/dataset/\<subject>/SDS[1 or 2]/\<date>/**
2. You should have phantom_simulated in the directory **/dataset/phantom_simulated** 
3. keep your pre-trained surrogate model in the directory **/surrogate_model/\<subject>/**
4. keep your pre-trained prediction model in the directory **/model_save/\<exp_name>/\<subject>/**
5. Make sure your **OPs_used** is synchronized as previous experiment (MCX simulation, training surrogate model, training prediction model)
6. Make sure your **ANN_models.py** is synchronized as previous experiment (training surrogate model, training prediction model) 
 
- Launch: 
    - **S1_preprocess_short.ipynb**: preprocess raw data of short channel.
    - **S1_preprocess_long.ipynb**: preprocess raw data of long channel.
    - **S2_predict_measured_data.ipynb**: use prediction model take processed data as input, get predicted blood oxygen change of IJV.



## Diagram of preprocessing of raw data
![image](https://hackmd.io/_uploads/Sk8z4zqNa.png)


