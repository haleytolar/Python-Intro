class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def __sub__(self, other):
        # Convert both heights to inches for easy subtraction
        total_inches_self = self.feet * 12 + self.inches
        total_inches_other = other.feet * 12 + other.inches
        
       
        total_inches_result = total_inches_self - total_inches_other
        
        # If the result is negative, handle the borrowing
        if total_inches_result < 0:
            result_feet = 0  
            result_inches = total_inches_result
        else:
            result_feet = total_inches_result // 12  # Get the number of feet
            result_inches = total_inches_result % 12  # Get the remaining inches
        
        
        return Height(result_feet, result_inches)

    def __str__(self):
        # String representation of the Height object
        return f"{self.feet} feet {self.inches} inches"
        

height1 = Height(5, 10)  
height2 = Height(3, 9)   


result = height1 - height2

print(f"Result: {result}")  # Should output the height difference
