def longest_sorted_part(text):
    if text == "":
        return "No substring found"

    longest = text[0]     
    current = text[0]     

    for i in range(1, len(text)):
        if text[i] >= text[i - 1]:
            current += text[i] 
        else:
            current = text[i]  

        if len(current) > len(longest):
            longest = current   

    return longest

user_input = input("enter text: ")
result = longest_sorted_part(user_input)
print("the longest sorted is :", result)