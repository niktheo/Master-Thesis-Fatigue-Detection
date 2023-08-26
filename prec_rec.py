import matplotlib.pyplot as plt
import numpy as np

# Example precision-recall values
recall = [0.10, 0.20, 0.40, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95, 1.00]
precision = [0.94, 0.85, 0.70, 0.60, 0.55, 0.50, 0.45, 0.40, 0.35, 0.30]

# Plotting the precision-recall curve
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, marker='o')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.grid(True)
plt.show()



def calculate_average_precision(precision, recall):
    # Ensure precision and recall are numpy arrays
    precision = np.array(precision)
    recall = np.array(recall)

    # Calculate the area under the precision-recall curve using trapezoidal rule
    ap = np.trapz(precision, recall)

    return ap

# Example precision-recall value

# Calculate the average precision
ap = calculate_average_precision(precision, recall)
print(f"Average Precision: {ap:.4f}")