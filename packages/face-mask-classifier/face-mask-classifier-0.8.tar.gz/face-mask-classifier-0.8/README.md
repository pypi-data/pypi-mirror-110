SVM facemask classifier

Pretrained Model used:
   Keras-facenet model ()
     This model is used to detect the faces in a image and create a embedding vector of the faces which would be passed to a SVM classifier. 
     The embedding vector is of dimension 512.


Download the SVM pretrained model https://github.com/Baskar-t/face-mask-classifier/tree/main/models

Class mask_predictor
#### image - path of the image file to predict the mask
#### pretrained path of the SVM model
def pred_mask(image,svm_model_path)
     ......
	return img, box_list, label_list, proba_list
	
#### img - image vector
#### box list - list of image box of faces
#### label_list - list of labels for the predicted face images (Mask , No Mask)
#### proba_list - list of probability of predicted labels


Usage:

## mask_predictor.pred_mask(image path, path_svm_model)