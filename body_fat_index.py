import math

def calculate_body_fat(gender, height, neck, waist, hip=None):
    if gender.lower() == 'male':
        body_fat = 86.010 * math.log10(waist - neck) - 70.041 * math.log10(height) + 36.76
    elif gender.lower() == 'female':
        body_fat = 163.205 * math.log10(waist + hip - neck) - 97.684 * math.log10(height) - 78.387
    else:
        raise ValueError("Invalid gender. Use 'male' or 'female'.")
    return round(body_fat, 2)

# Example usage
gender = 'male'
height = 175  # in cm
neck = 40     # in cm
waist = 90    # in cm
body_fat = calculate_body_fat(gender, height, neck, waist)
print(f"Body Fat Percentage: {body_fat}%")