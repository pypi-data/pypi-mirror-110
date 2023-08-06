## ACTICO ML Python

With this package, a user is able to export a trained H2O ML model 
to ACTICO Model Hub.

Parameters
----------
api_key : string.
    Generated within Model Hub and required for a connection.

machine_learning_server_url : string.
    The link to the machine learning server, e.g. "http://localhost:8080".

model_name : string. 
    The name of the model to be released, e.g. "credit-rf-model".

training_frame_name : string. 
    The name of the frame used for the training, e.g. "credit-train.hex".

module_id : string.
    The module id is used to group related model projects into one logical unit, e.g. "actico.credit".

project_id : string.
    The model project id is used to refer to the released machine learning model, e.g. "gm-model".

version : string, optional.
    The version is used to distinguish between different iterations of a model. If left blank, an automatically generated version is used.

    

