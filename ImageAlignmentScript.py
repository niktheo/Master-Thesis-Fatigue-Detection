def imgAlig ():
    f = open("./Annotations_Images/list_98pt_rect_attr_train.txt", "r")

    newArr=[]
    arr= []
    count = 0
    bBoxGroundTruth=[]
    imgName=[]
    for item in f:
        arr.append(item.split(' '))
        imgName = arr[count][-1].split('/')
        imgName[1]= imgName[1].split("\n")
        a =[imgName[1][0]]
        bBoxGroundTruth = arr[count][196:200]
        res = [[eval(i) for i in bBoxGroundTruth]]
        infoArray= a + res
        newArr.append(infoArray)
        count +=1
    
    return newArr

imgAlig ()

