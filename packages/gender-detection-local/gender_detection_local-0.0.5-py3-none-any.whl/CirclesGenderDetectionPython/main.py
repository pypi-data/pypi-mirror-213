from gender_detection import *
model=GenderClassifier()
result=model.Predict(model_path="gender_detection")
print(result)
