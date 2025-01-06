
file=open("Ref2.py","r")

lines=[]
nums=[]

for x in file.readlines():
    if len(x)>2:
        lines.append(x)

for x in lines:
    if "#mod" in x:
        nums.append(int(lines.index(x)))

for x in nums:


    #print(lines[x-3])
    #print(lines[x-2])
    print(lines[x-1])
    print(lines[x])

    #cont=input("")
    print("-----------------------------------------")

