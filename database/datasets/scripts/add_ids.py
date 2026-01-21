import json

input_file = "final_quiz_dataset.json"

try:
    with open(input_file, 'r') as f:
        data = json.load(f)

    print(f"Read {len(data)} questions.")

    # Add unique IDs
    for index, item in enumerate(data, start=1):
        # Create a new dictionary with 'id' at the top
        new_item = {"id": index}
        new_item.update(item)
        data[index-1] = new_item

    with open(input_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Successfully added IDs to {len(data)} questions in {input_file}")

except FileNotFoundError:
    print(f"Error: {input_file} not found.")
except Exception as e:
    print(f"Error: {e}")
