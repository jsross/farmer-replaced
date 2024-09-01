def create_matrix(num_cols, num_dims):		
	matrix = []
	
	for index in range(num_cols):
		if num_dims <= 1:
			matrix.append(None)
		else:
			matrix.append(create_matrix(num_cols, num_dims - 1))
	
	return matrix
	

		
	