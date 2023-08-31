import matplotlib.pyplot as plt
import numpy as np

def plot_ear_over_time(ear_values_over_time):
    plt.plot(np.arange(len(ear_values_over_time)), ear_values_over_time, marker='o')
    plt.xlabel('Frame Number')
    plt.ylabel('Eye Aspect Ratio (EAR)')
    plt.title('Eye Aspect Ratio (EAR) over Time')
    plt.grid(True)
    plt.show()

def plot_performance_metrics(thresholds, precision_values, recall_values, f1_scores):
    plt.bar(thresholds, precision_values, label='Precision')
    plt.bar(thresholds, recall_values, label='Recall', bottom=precision_values)
    plt.bar(thresholds, f1_scores, label='F1-Score', bottom=np.add(precision_values, recall_values))
    plt.xlabel('Thresholds')
    plt.ylabel('Metric Value')
    plt.title('Comparative Analysis of Performance Metrics')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_ear_and_mar_histograms(ear_values, mar_values):
    plt.hist(ear_values, bins=15, color='blue', alpha=0.7)
    plt.xlabel('Eye Aspect Ratio (EAR)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Eye Aspect Ratio (EAR)')
    plt.grid(True)
    plt.show()

    plt.hist(mar_values, bins=15, color='orange', alpha=0.7)
    plt.xlabel('Mouth Aspect Ratio (MAR)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Mouth Aspect Ratio (MAR)')
    plt.grid(True)
    plt.show()
