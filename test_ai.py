from transformers import pipeline


classifer= pipeline("text-classification")
result = classifer("I love this product! It works great and exceeded my expectations.")
print(result)