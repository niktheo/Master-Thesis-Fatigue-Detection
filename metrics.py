def precision (tp,fp) : 
    return tp/(tp+fp)

def recall (tp,fn) : 
    return tp/(tp+fn)

def f1_score (precision,recall) : 
    return 2 * precision * recall/ (precision + recall)

def accuracy(tp,tn,fp,fn):
    return (tp+tn)/(tp+tn+fp+fn)

# def average_prec():
