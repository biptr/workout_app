import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from collections import OrderedDict

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Database information                                    ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
load_dotenv()

password = os.getenv('MG_PWD')
mongodb_uri = os.getenv('MG_URI')
client = MongoClient(mongodb_uri)

db = client['workout_application']
exercises = db['exercises']
workouts = db['workouts'] 

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Add exercises to the exercises collection via file      ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def load_data_into_exercises_collection(input_file):
    '''
    Loads a JSON file into the exercises collection

    Parameters:
        input_file (str): The path to the JSON file containing exercise data.

    Returns:
        str: Prints messages indicating the number of successful and failed insertions, 
        and detailed error messages if any documents failed to insert.  
    '''    
    
    with open(input_file) as file:
        data = json.load(file)
        
        successful_insertions = 0
        failed_insertions = 0
        
        for document in data:
            if not exercises.find_one({'name': document['name']}):
                try:
                    exercises.insert_one(document)
                    successful_insertions += 1
                except Exception as e:
                    print(f"Failed to insert document {document['name']}: {e}")
                    failed_insertions += 1
            else:
                print(f"Document {document['name']} already exists in the collection, skipping...")
                failed_insertions +=1
            
    print(f"Successful insertions: {successful_insertions}")
    print(f"Failed insertions: {failed_insertions}")
    
    if failed_insertions == 0:
        print("All documents were loaded successfully.")
    else:
        print("Some documents failed to load. Please review the error messages.")

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Create an exercise                                      ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def create_exercise(name, category):
    '''
    Creates an exercise in the exercises collection

    Parameters:
        name (str): The exercise name
        category (str): The muscle category worked

    Returns:
        str: A message indicating if the exercise was successfully created or if it already exists
    '''
    
    exercise_query = exercises.find_one({'name': name})
    
    if exercise_query:
        print("Exercise already created.")
        
    else:
        exercises.insert_one({'name': name, 'muscleCategory': category})   
        exercise_inserted = exercises.find_one({'name': name})
        
        if exercise_inserted:
            print(f"Exercise name: {exercise_inserted['name']}, ID: {exercise_inserted['_id']}, was successfully created.")
        
        else:
            print("Error: Exercise was not successfully created.")   

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Update an exercise                                      ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def update_exercise(exercise, key, value):
    '''
    Updates the exercise's attributes in the exercises collection

    Parameters:
        exercise (str): The name of the exercise to be updated
        key (str): The attribute that will be updated
        value (str): The value of the new attribute
    Returns:
        str: A message indicating if the exercise was successfully updated or if it was not found
    '''
    
    if key not in ['name', 'muscleCategory']:
        print(f"Invalid attribute '{key}'. Only 'name' or 'category' can be updated.")
    
    else:
        exercise_to_update = exercises.find_one({'name': exercise})
        
        if exercise_to_update:
            result = exercises.update_one(exercise_to_update, {'$set': {key: value}})
            
            if result.acknowledged:
                print(f"Exercise '{exercise}' updated successfully.")
            
            else:
                print(f"Failed to update exercise '{exercise}'.")
                
        else:
            print(f"Exercise '{exercise}' not found in the database.")
        
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Delete an exercise                                      ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def delete_exercise(exercise):
    '''
    Removes an exercise from the exercises collection

    Parameters:
        exercise (str): The name of exercise that will be deleted

    Returns:
        str: A message indicating if the exercise was successfully deleted or if it was not found
    '''
    
    exercise_to_delete = exercises.find_one({'name': exercise})
    
    if exercise_to_delete:
        result = exercises.delete_many({'name': exercise})

        if result.deleted_count > 0:
            print(f"Exercise '{exercise}' deleted successfully.")
        
        else:
            print(f"Failed to delete exercise '{exercise}.'")
    
    else:
        print(f"Exercise '{exercise}' not found in the database.")
  
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Update entire exercise                                  ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛     
def update_entire_exercise(exercise_name, object):
    '''
    Updates an exercise in the exercises collection

    Parameters:
        exercise_name (str): The name of the exercise that will be updated
        object (dict): A dictionary containing the new data for the exercise, including the name and muscle category

    Returns:
        str: A message indicating if the exercise was successfully updated or if it was not found
    '''
    
    exercise_to_update = exercises.find_one({'name': exercise_name})

    if exercise_to_update:
        result = exercises.replace_one({'name': exercise_name}, object)
        
        if result.matched_count > 0:
            print(f"Exercise '{exercise_name}' was successfully updated.")
        
        else:
            print(f"Failed to update exercise '{exercise_name}'.")
            
    else:
        print(f"Exercise '{exercise_name}' not found in the database.")  
        
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Create a workout                                        ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  
def create_workout(name):
    '''
    Creates a workout in the workouts collection

    Parameters:
        name (str): The name of the workout
    Returns:
        str: A message indicating if the workout was successfully created or if it already exists.
    '''   
    workout_query = workouts.find_one({'name': name})
    
    if workout_query:
        print(f"Workout '{name}' already created.")
    
    else:
        result = workouts.insert_one({"name": name, "exercises": []})
    
        if result.acknowledged:
           print(f"Workout '{name}' created successfully.")
        
        else:
            print(f"Failed to create workout '{name}'.")   
                 
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Add and exercise to a workout                           ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ 
def insert_exercise_into_workout(workout, exercise):   
    '''
    Inserts an exercise into a selected workout

    Parameters:
        workout (str): The name of the workout where the exercise will be added
        exercise (str): The exercise name to be added

    Returns:
        str: A message indicating if the exercise was successfully added to a workout or if it already exists
    '''   
    
    workout_query = workouts.find_one({"name": workout})

    if not workout_query:
        print(f"Workout '{workout}' not found in the database.")

    else:
        exercise_query = exercises.find_one({"name": exercise})
    
        if not exercise_query:
            print(f"Exercise '{exercise}' not found in the database.")

        else:
            workout_query = workouts.find_one({"name": workout})
            
            if workout_query:               
                workout_id = workout_query['_id']       
                exercises_list = workouts.distinct("exercises.name", {"name": workout})
            
                if exercise in exercises_list:
                    print(f"{exercise} already exists in workout {workout}.")
                
                else:
                    workouts.update_one({'_id': workout_id} ,{"$push": {"exercises": exercise_query}})
                    print(f"{exercise} added to workout {workout}.")
        
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Remove an exercise from a workout                       ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ 
def delete_exercise_from_workout(workout, exercise):
    '''
    Removes an exercise from a selected workout

    Parameters:
        workout (str): The name of the workout from where the exercise will be removed
        exercise (str): The exercise name to be removed

    Returns:
        str: A message indicating if the exercise was successfully removed from a workout or not
    '''  
    
    workout_query = workouts.find_one({"name": workout})
    
    if not workout_query:
        print(f"Workout '{workout}' not found in the database.")
               
    else:
        workout_id = workout_query['_id']       
        exercises_list = workouts.distinct("exercises.name", {"name": workout})
    
        if exercise in exercises_list:
            result = workouts.update_one({'_id': workout_id}, {'$pull': {'exercises': {'name': exercise}}})
            
            if result.modified_count > 0:
                print(f"Exercise '{exercise}' removed from workout '{workout}'.")
            
            else:
                print(f"Failed to remove exercise '{exercise}' from workout '{workout}'.")
            
        else:
            print(f"Exercise '{exercise}' not found in workout '{workout}'.")
