def create_array(length, default):
	array = []

	for _ in range(length):
		array.append(default)
	
	return array


def new_array(src_array):
	dest_array = []

	for item in src_array:
		dest_array.append(item)
	
	return dest_array

def copy_array(src_array, dest_array):
	count = len(src_array)

	for index in range(count):
		dest_array[index] = src_array[index]

def find_in_array(array, test_func):
	items = []

	for index in range(len(array)):
		item = array[index]

		if test_func(item, index):
			items.append(item)
	
	return items

def remove_range(array, to_remove):
	for item in to_remove:
		if item in array:
			array.remove(item)

	return array

def select_object_from_array(array, properties):
	def test_func(item, _):
		for key in properties:
			if key not in item:
				return False
			if item[key] != properties[key]:
				return False
			
			continue

		return True
	
	return find_in_array(array, test_func)

def merge(target, source):
	for key in source:
		target[key] = source[key]

def wait_till(timestamp):
	while True:
		current_timestamp = get_time()

		if current_timestamp > timestamp:
			break
