txt1 = "9000,4500,650,550,650,550,650,550,650,550,650,550,650,550,650,1600,650,550,650,550,650,550,650,1600,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,1600,650,550,650,1600,650,550,650,1600,650,550,650,1600,650,0"
txt2 = "9000,4500,650,550,650,550,650,550,650,550,650,550,650,550,650,1600,650,550,650,550,650,550,650,1600,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,550,650,1600,650,550,650,1600,650,550,650,1600,650,550,650,1600,650,0"
str1 = ""
str2 = ""
HDR_MARK = '9000'
HDR_SPACE = '4500'
BIT_SPACE = '650'
ONE_SPACE = '1600'
ZERO_SPACE = '550'

check = 0
txt1 = txt1.split(',')
txt2 = txt2.split(',')


for i in txt1:
    if i == HDR_MARK:
        check = 0
    elif i == HDR_SPACE:
        check = 0
    elif (i == BIT_SPACE) and (check == 0):
        check = 1
    elif (i == ONE_SPACE) and (check == 1):
        str1 += '1'
        check = 0
    elif (i == ZERO_SPACE) and (check == 1):
        str1 += '0'
        check = 0
    elif (i == '29500') and (check == 1):
        check = 0

for i in txt2:
    if i == HDR_MARK:
        check = 0
    elif i == HDR_SPACE:
        check = 0
    elif (i == BIT_SPACE) and (check == 0):
        check = 1
    elif (i == ONE_SPACE) and (check == 1):
        str2 += '1'
        check = 0
    elif (i == ZERO_SPACE) and (check == 1):
        str2 += '0'
        check = 0
    elif (i == '29500') and (check == 1):
        check = 0

print(str1)
print(str2)