def crawler(baseUrl,key="null"):
    url = baseUrl

def makeArr(name):
    mFile = open(name, "r")
    lines = mFile.readlines()
    mFile.close()
    arr = []
    for line in lines:
        line = line.strip("\n")
        temps = line.split(",")
        tempArr = []
        for i in range(len(temps)):
            tempArr.append(temps[i])
        arr.append(tempArr)
    return arr

def taxiByArea():
    mFile = open("taxicompany.csv", "r")
    lines = mFile.readlines()
    mFile.close()

    result = {}
    for line in lines:
        line = line.strip("\n")
        arr = line.split(",")

        if arr[0] in result.keys():
            # 이미 딕셔너리에 있는 경우
            result[arr[0]] += 1
        else:
            result[arr[0]] = 1

    resFile = open("taxiByArea.csv", "w")
    for k, v in result.items():
        resFile.write(k + "," + str(v) + "," + "\n")
    resFile.close()

def locationChange():
     # 행정구역 행렬 변환
     lArr = makeArr("DistinctArea.csv")
     # 좌표 행렬 변환
     tArr = makeArr("locations.csv")

     # 이름 같은 거 같은 이름으로 넣어버리기
     result = open("resLoc.csv", "w")
     for l in lArr:
         for t in tArr:
             print(l[1],t[2], t[1]==t[2])
             if l[1] == t[2]:
                 result.write(l[0] +","+ l[1] +","+ t[4] +","+ t[5])
     result.close()


def taxiAddLocation():
    # 좌표 행렬 변환
    locationArr = makeArr("resultOfTaxi.csv")
    # 택시 행렬 변환
    taxiArr = makeArr("taxiByArea.csv")

    # print(taxiArr, locationArr)
    # 택시 행렬 기준으로 좌표 값 찾기
    result = open("resultOfTaxi.csv", "w")

    for t in taxiArr:
        for l in locationArr:
            if t[0] == l[0]:
                print(t[0])
                result.write(t[0] + "," + l[1] + "," + t[1] + "\n" )
    result.close()


# taxiAddLocation()
