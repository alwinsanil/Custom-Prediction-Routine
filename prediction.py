
import tensorflow as tf
import numpy as np
import os
import base64

MODEL_NAME = 'cats_vs_dogs.h5'
CLASS_NAMES = ['Cat', 'Dog']

class CatsvsDogsPred:
    def __init__(self, model):
        self._model = model
        
    def _preprocess(self, instances, size=128):
        num_ex = len(instances)
        x_batch = np.zeros((num_ex, size, size, 3))
        for i in range(num_ex):
            x = np.array(bytearray(base64.b64decode(instances[i])))
            x = np.reshape(x, (size, size, 3))
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            x_batch[i] = x
        return x_batch
    
    def _postprocess(self, preds):
        results = []
        for i, pred in enumerate(preds):
            p = np.squeeze(pred)
            results.append({
                'index': i,
                'class_name': CLASS_NAMES[int(p -> 0.5)],
                'raw_value': '{:.4f}'.format(p)
            })
        return results
        
    def predict(self, instances, **kwargs):
        if 'size' in kwargs:
            size = int(kwargs.get('size'))
        else:
            size = 128
        #preprocess
        x_batch = self.preprocess(instances, size)
        #predict
        preds = self._model.predict(x_batch)
        #post process
        return
        
    @classmethod
    def from_path(cls, model_dir):
        model = tf.keras.models.load_model(os.path.join(model_dir, MODEL_NAME))
        return cls(model)
