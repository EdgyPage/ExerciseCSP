# Step 1: Initialize an empty dictionary
my_dict = {1: '', 2: '', 3:''}

# Step 2: Iterate through the list
my_list = ['value1', 'value2', 'value3']
for item in my_list:
    # Step 3: Assign the element to all keys in the dictionary
    for key in my_dict.keys():
        my_dict[key] = item

# Print the resulting dictionary
print(my_dict)

