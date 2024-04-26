from sklearn.metrics import precision_score, recall_score, f1_score

# Dự đoán của model và nhãn thực tế trong tập dữ liệu test
predicted_labels = [...]  # Dự đoán của model
actual_labels = [...]     # Nhãn thực tế

# Tính toán các thông số đánh giá
precision = precision_score(actual_labels, predicted_labels, average='weighted')
recall = recall_score(actual_labels, predicted_labels, average='weighted')
f1 = f1_score(actual_labels, predicted_labels, average='weighted')

# In các thông số đánh giá
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
