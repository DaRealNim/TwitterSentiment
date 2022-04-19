def getNegAndPosWords():
    with open("dicts/frlsd.cat") as dictFile:
        lines = iter(dictFile.readlines())
        negativeWords = []
        positiveWords = []

        next(lines)
        while ((neg := next(lines).strip()) != "POSITIVE"):
            neg = neg.split("(")
            neg[0] = neg[0].strip()
            neg[1] = neg[1].replace(")", "")
            neg[1] = int(neg[1])
            negativeWords.append(neg)
    
        while True:
            try:
                pos = next(lines).strip()
                pos = pos.split("(")
                pos[0] = pos[0].strip() 
                pos[1] = pos[1].replace(")","")
                pos[1] = int(pos[1])           
                positiveWords.append(pos)
                print(pos)
            except StopIteration:
                break
    return (positiveWords, negativeWords)
