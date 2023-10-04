# import matplotlib.pyplot as plt
# import numpy as np

# # Example precision-recall values
# recall = [0.10, 0.20, 0.40, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95, 1.00]
# precision = [0.94, 0.85, 0.70, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30]

# # Plotting the precision-recall curve
# plt.figure(figsize=(8, 6))
# plt.plot(recall, precision, marker='o')
# plt.xlabel('Recall')
# plt.ylabel('Precision')
# plt.title('Precision-Recall Curve')
# plt.grid(True)
# plt.show()



# def calculate_average_precision(precision, recall):
#     # Ensure precision and recall are numpy arrays
#     precision = np.array(precision)
#     recall = np.array(recall)
#     print('prec', precision)
#     print('rec', recall)
#     # Calculate the area under the precision-recall curve using trapezoidal rule
#     ap = np.trapz(precision, recall)

#     return ap

# # Example precision-recall value

# # Calculate the average precision
# ap = calculate_average_precision(precision, recall)
# print(f"Average Precision: {ap:.4f}")

import matplotlib.pyplot as plt
import numpy as np

# Improved precision-recall values
recall = [0.10, 0.30, 0.45, 0.55, 0.65, 0.75, 0.85, 0.90, 0.95, 1.00]
precision = [0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50]

# Calculate F1 score
def calculate_f1_score(precision, recall):
    f1_scores = 2 * (precision * recall) / (precision + recall)
    return f1_scores

f1_scores = calculate_f1_score(np.array(precision), np.array(recall))

# Calculate average precision, recall, and F1 score
avg_precision = np.mean(precision)
avg_recall = np.mean(recall)
avg_f1_score = np.mean(f1_scores)

# Plotting the Precision-Recall curve
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, marker='o', label='Precision-Recall Curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.grid(True)
plt.legend()
plt.show()

# Plotting the F1 score curve
plt.figure(figsize=(8, 6))
plt.plot(recall, f1_scores, marker='o', color='green', label='F1 Score Curve')
plt.xlabel('Recall')
plt.ylabel('F1 Score')
plt.title('F1 Score Curve')
plt.grid(True)
plt.legend()

# Print average precision, recall, and F1 score
print(f'Average Precision: {avg_precision:.2f}')
print(f'Average Recall: {avg_recall:.2f}')
print(f'Average F1 Score: {avg_f1_score:.2f}')

plt.show()
