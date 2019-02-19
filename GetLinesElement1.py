f = open("number.txt","r")

My_Lines = (f.readlines() )

def getLineElement(Lines):

    

#print(f.readlines()[1:])

    line_numbers=[]
    print("-------------------------")
    for line in Lines:
        line=line+" "
    

        numbers = []

        number = ""
        print(line)

        print("-------------------------")
        for s in line:


        
            if s == " " :
                if number!="":
                    numbers.append(number)
                number = ""


            if s != " " and s !="\n":
                number = number + s
                #print(number)

        line_numbers.append(numbers)    
        
                


    f.close()
    return line_numbers

#print( getLineElement(My_Lines) )

for line in getLineElement(My_Lines):
    print(line)
