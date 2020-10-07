# File name: app.py
# Author: Jesse Malinen
# Description: Main app script

# imports
from flask import Flask, jsonify, request
from http import HTTPStatus

# app definition
app = Flask(__name__)

# instructions list
instructions = [
    {
        'id': 1,
        'name': 'Paint a wall',
        'description': 'Instructions how to paint a wall',
        'steps': ['Clean the wall', 'Tape the trim',
                  'Roll the primer onto the wall',
                  'Paint the trim', 'Remove the tape'],
        'tools': ['tape', 'primer', 'paint', 'paint roller',
                  'paint tray', 'paintbrush'],
        'cost': 100,
        'duration': 8
    },
    {
        'id': 2,
        'name': 'Throw a ball',
        'description': 'Instructions how to throw a ball',
        'steps': ['get a ball', 'grab the ball',
                  'pull your hand back', 'throw the ball'],
        'tools': ['ball', 'hand'],
        'cost': 50,
        'duration': 4
    }
]

# get all instructions
@app.route('/instructions', methods=['GET'])
def get_instructions():
    return jsonify({'data': instructions})

# get a specific instruction
@app.route('/instructions/<int:instruction_id>', methods=['GET'])
def get_instruction(instruction_id):
    instruction = next((instruction for instruction in instructions if instruction['id'] == instruction_id), None)

    if instruction:
        return jsonify(instruction)

    return jsonify({'message': 'instruction not found'}), HTTPStatus.NOT_FOUND

# add a new instruction
@app.route('/instructions', methods=['POST'])
def create_instruction():
    data = request.get_json() # requesting input from user

    name = data.get('name')
    description = data.get('description')
    steps = data.get('steps')
    tools = data.get('tools')
    cost = data.get('cost')
    duration = data.get('duration')

    instruction = {
        'id': len(instructions) + 1, # id number depends on list length
        'name': name,
        'description': description,
        'steps': steps,
        'tools': tools,
        'cost': cost,
        'duration': duration
    }

    instructions.append(instruction) # adding entry to list

    return jsonify(instruction), HTTPStatus.CREATED

# updating an instruction
@app.route('/instructions/<int:instruction_id>', methods=['PUT'])
def update_instruction(instruction_id):
    instruction = next((instruction for instruction in instructions if instruction['id'] == instruction_id), None)
    # if instruction not found
    if not instruction:
        return jsonify({'message': 'instruction not found'}), HTTPStatus.NOT_FOUND
    # otherwise asking for input
    data = request.get_json()

    instruction.update(
        {
            'name': data.get('name'),
            'description': data.get('description'),
            'steps': data.get('steps'),
            'tools': data.get('tools'),
            'cost': data.get('cost'),
            'duration': data.get('duration')
        }
    )

    return jsonify(instruction)

# deleting an instruction
@app.route('/instructions/<int:instruction_id>', methods=['DELETE'])
def delete_instruction(instruction_id):
    instruction = next((instruction for instruction in instructions if instruction['id'] == instruction_id), None)
    # if instruction not found
    if not instruction:
        return jsonify({'message': 'instruction not found'}), HTTPStatus.NOT_FOUND
    # otherwise delete
    instructions.remove(instruction)

    return '', HTTPStatus.NO_CONTENT

# run script
if __name__ == '__main__':
    app.run()
