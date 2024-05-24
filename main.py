from modules.exercises import create_exercise, update_exercise, delete_exercise, create_workout, insert_exercise_into_workout, delete_exercise_from_workout

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Defining the interaction menu                           ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def display_menu():
      print('Welcome, user. What task would you like to run?\n'
            '1. Create an exercise\n'
            '2. Update an exercise\n'
            '3. Delete an exercise\n'
            '4. Create a workout\n'
            '5. Add exercises to a workout\n'
            '6. Delete exercises from a workout\n')

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Asking the user for details based on selected task      ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def main():
    while True:
        display_menu()
        
        # Asking the user to select an option 
        user_input = input("Select an option... ")

        try:
            user_input = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")
            input("Press any number to continue...")
            continue
        
        match user_input:
            case 1:
                # Creating a new exercise
                
                name = input("Enter the exercise name: ")
                muscleCategory = input("Enter the muscle category: ")
                result = create_exercise(name, muscleCategory)
                # print(result)
                eval(input('Press any number to continue... '))
                
            case 2:
                # Updating an existing exercise
                
                name = input("Enter the name of the exercise to update: ")
                attribute = input("Enter the attribute to update (e.g., name, category): ")
                new_value = input("Enter the new value: ")
                update_exercise(name, attribute, new_value)
                eval(input('Press any number to continue... '))
                
            case 3:
                # Deleting an existing exercise
                
                name = input("Enter the name of the exercise to delete: ")
                delete_exercise(name)
                eval(input('Press any number to continue... '))
                
            case 4:
                # Creating a new workout
                
                name = input("Enter the name of the workout: ")
                create_workout(name)
                eval(input('Press any number to continue... '))
                
            case 5:
                # Inserting an exercise into a workout
                
                workout = input("Enter the name of the workout:")
                exercise = input("Enter the name of the exercise to be create:")
                insert_exercise_into_workout(workout, exercise)
                eval(input('Press any number to continue... '))
                
            case 6:
                #Deleting an exercise from a workout
                
                workout = input("Enter the name of the workout:")
                exercise = input("Enter the name of the exercise to be deleted:")
                delete_exercise_from_workout(workout, exercise)
                eval(input('Press any number to continue... '))
                
            case _:
                # Handling invalid options
                
                print("Invalid option. Please select a number between 1 and 11.")

if __name__ == "__main__":
    main()