
def get_weight():
    while True:
        try:
            weight = float(input("Enter your weight (kg): "))
            if weight <= 0 or weight > 300:
                print(" Please enter a realistic weight (1–300 kg).")
            else:
                return weight
        except ValueError:
            print(" Invalid input. Enter a number.")

def get_height():
    while True:
        try:
            height = float(input("Enter your height (meters): "))
            if height <= 0 or height > 2.5:
                print(" Please enter a realistic height (0.5–2.5 meters).")
            else:
                return height
        except ValueError:
            print("Invalid input. Enter a number.")

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal weight"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def main():
    print(" BMI Calculator\n")

    weight = get_weight()
    height = get_height()

    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)

    print("\n BMI Result")
    print("--------------------")
    print(f"BMI Value : {bmi:.2f}")
    print(f"Category  : {category}")

# Run the program
main()
