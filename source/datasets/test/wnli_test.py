from typing import Tuple
from autogoal.kb import *
from autogoal.ml import AutoML
from dataset import Dataset
from functions_load import *
import utils
from sklearn.metrics import f1_score
import numpy as np 

a = Dataset("wnli-es", "https://github.com/amyGB99/automl_benchmark/releases/download/paws-x/paws-x-es.zip", load_wnli )
utils.save_dataset_definition(a)
c = utils.load_dataset_definition("wnli-es")
Xtr,ytr,Xde,yde,Xte,yte = c.loader_func(a)
ytr1= np.asarray(ytr)
yte1= np.asarray(yte)
yde1= np.asarray(yde)
print(len(Xtr))
print(len(ytr1))
print(ytr1)
print("kaka")
print(Xtr[0:3])
print(Xte[0:3])
automl = AutoML(
    input=(Seq[Seq[Sentence]], Supervised[VectorCategorical]),
    output= VectorCategorical)
#automl.fit(Xtr[0:100],ytr1[0:100])
#print(automl.best_score_)
# print(len(ytr1))
# automl.fit(Xtr,ytr1)
# print(yte1)

# print("aqui")
#y = automl.predict(Xte)

# #for i in y:  
#print(y)
# print(automl.best_score_)

# #score = automl.score(Xte,yte1)


