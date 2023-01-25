import os
from keras.preprocessing import image
from keras.models import load_model
from operator import itemgetter
from helper_db import HelperDB
from helper import image_path

class CNN:

    classes = ['Login', 'SignIn', 'SignUp']

    @classmethod
    def predict(cls, id):
        
        label = HelperDB().get_label(id)

        auth_model_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "cnn", "auth_model.h5"
        )
        
        model = load_model(auth_model_path)
        im_width = 64
        im_height = 48

        local_img = os.path.join(image_path(), label['image_name'])

        img = image.image_utils.load_img(local_img, target_size=(im_height, im_width))
        img = image.image_utils.img_to_array(img)
        img = img.reshape((1,) + img.shape)
        img = img/255.

        y_prob = model.predict(img)

        potentials = []
        for idx, result in enumerate(y_prob[0]):
                    
            print(f"Prediction higher than 80 {result} class {cls.classes[idx]}")
            # Compare
            # ld = label.replace(" ", "").lower()
            predicted_class = cls.classes[idx].replace(" ", "").lower()
            potentials.append({
                "score": result * 100,
                "label": predicted_class
            })            
                    
        return sorted(potentials, key=itemgetter('score'), reverse=True)[0]
 
        
