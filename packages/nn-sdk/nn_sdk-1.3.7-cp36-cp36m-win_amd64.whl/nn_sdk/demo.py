# -*- coding: utf-8 -*-
from nn_sdk.py_engine_csdk import csdk_object
'''
    前言: 
        当前支持开发语言c/c++,python,java
        当前支持推理引擎tensorflow(v1,v2) onnxruntime
        当前支持多子图,支持图多输入多输出，支持tensorflow 1 pb , tensorflow 2 pb , tensorflow ckpt
        python (demo.py) , c包 (nn_sdk.h) , java包 (nn_sdk.java)
'''


'''
    python 推理demo
    config 字段介绍:
        engine: 推理引擎 0: tensorflow , 1: onnx
        log_level: 日志类型 0 fatal , 2 error , 4 info , 8 debug
        model_type: tensorflow时有效, 0 pb format   if 1 ckpt format
        ConfigProto: tensorflow时有效
        graph_inf_version: tensorflow version [0,1] or onnxruntime 1
        graph: 多子图配置 
            node: 例子: tensorflow 1 input_ids:0 ,  tensorflow 2: input_ids , onnx: input_ids
            data_type: 节点的类型根据模型配置，支持 int int64 long longlong float 
            shape: 节点尺寸
            python 接口可以忽视 data_type,shape字段 ,如 {"node":"input_ids:0"}
            java 和 c 包不可缺少 data_type,shape字段
    
'''
config = {
    "model_dir": r'E:/algo_text/nn_csdk/nn_csdk/py_test_ckpt/model.ckpt',
    "log_level": 4,
    'engine':1,
    "model_type": 1,
    "ConfigProto": {
        "log_device_placement": False,
        "allow_soft_placement": True,
        "gpu_options": {
            "allow_growth": True
        },
    },
    "graph_inf_version": 1,
    "graph": [
        {
            "input": [
                {"node":"input_ids:0", "data_type":"float", "shape":[1, 256]},
                {"node":"input_mask:0", "data_type":"float", "shape":[1, 256]}
            ],
            "output": [
                {"node":"input_ids:0", "data_type":"float", "shape":[1, 256]},
            ],
        }
    ]}

seq_length = 256
input_ids = [[1.] * seq_length]
input_mask = [[1] * seq_length]
sdk_inf = csdk_object(config)
if sdk_inf.valid():
    net_stage = 0
    ret, out = sdk_inf.process(net_stage, input_ids,input_mask)
    print(ret)
    print(out)
    sdk_inf.close()