import numpy as np
#from scipy.optimize import linear_sum_assignment

class Hungarian_algorithm:

    # This method take in input a numpy square matrix nxn where each cells i,j represents the weight   
    # of the edge joining node i with node j.
    # This method returns a matrix nxn repesenting the assignement that maximize the weight.
    # Each cell i,j contains 1 if the edge joining i and j belong to the assignement, 0 otherwise.
    def get_maximum_weight_assignment(self, matrix):
        m = self.__copy(matrix) #matrix.copy()
        maximum_value = m.max()
        m = m * - 1
        m = m + maximum_value
        return self.__compute(m)
    
    # This method take in input a numpy square matrix nxn where each cells i,j represents the weight   
    # of the edge joining node i with node j.
    # This method returns a matrix nxn repesenting the assignement that minimize the weight.
    # Each cell i,j contains 1 if the edge joining i and j belong to the assignement, 0 otherwise.
    def get_minimum_weight_assignment(self, matrix):
        return self.__compute(matrix)

    def __copy(self, matrix):
        copy_matrix = np.empty(matrix.shape, dtype = int) 
        for i in range(0,matrix.shape[0]):
            for j in range(0,matrix.shape[1]):
                copy_matrix[i,j] = matrix[i,j]
        return copy_matrix

    def __compute(self, initial_matrix):
        matrix = self.__copy(initial_matrix) #matrix = initial_matrix.copy()
        matrix = self.__pad_matrix(matrix,0)
        self.__step1(matrix)
        self.__step2(matrix)
        n_lines = 0
        max_length = np.maximum(matrix.shape[0], matrix.shape[1])
        while n_lines != max_length:
            lines = self.__step3(matrix)
            n_lines = len(lines[0]) + len(lines[1])
            if (n_lines != max_length):
                self.__step5(matrix, lines[0], lines[1])
        return self.__final_assignement(initial_matrix, matrix)

    def __pad_matrix(self, matrix,val):
        (a,b)=matrix.shape
        if a>b:
            padding=((0,0),(0,a-b))
        else:
            padding=((0,b-a),(0,0))
        return np.pad(matrix,padding,mode='constant',constant_values=val)

    # Remove the dummy rows/columns
    def __restore_initial_shape(self, initial_matrix, assignement):
        dif = initial_matrix.shape[0] - initial_matrix.shape[1]
        if(dif > 0):
            return assignement[:,0:-abs(dif)]
        elif(dif != 0):
            return assignement[0:-abs(dif),:]
        return assignement

    def __final_assignement(self,initial_matrix, m):
        assignement = np.zeros(m.shape, dtype = int)
        assignement = self.__assignement_single_zero_lines(m, assignement)
        while(np.sum(m==0)>0):
            i,j = self.__first_zero(m)
            assignement[i,j] = 1
            m[i,:] += 1
            m[:,j] += 1
            assignement = self.__assignement_single_zero_lines(m,assignement)

        assignement = self.__restore_initial_shape(initial_matrix, assignement)
        return assignement
    
    def __first_zero(self,m):
        return np.argwhere(m==0)[0][0], np.argwhere(m==0)[0][1]

    def __assignement_single_zero_lines(self, m, assignement):
        val = self.__find_rows_single_zero(m)
        while (val):
            i, j = val[0], val[1]
            m[i, j] += 1
            m[:, j] += 1
            assignement[i, j] = 1
            val = self.__find_rows_single_zero(m)

        val = self.__find_cols_single_zero(m)
        while (val):
            i, j = val[0], val[1]
            m[i, :] += 1
            m[i, j] += 1
            assignement[i, j] = 1
            val = self.__find_cols_single_zero(m)
        return assignement

    def __find_cols_single_zero(self, matrix):
        for i in range(0, matrix.shape[1]):
            if (np.sum(matrix[:, i] == 0) == 1):
                j = np.argwhere(matrix[:, i] == 0).reshape(-1)[0]
                return j, i
        return False

    def __find_rows_single_zero(self, matrix):
        for i in range(0, matrix.shape[0]):
            if(np.sum(matrix[i, :] == 0) == 1):
                j = np.argwhere(matrix[i, :] == 0).reshape(-1)[0] 
                return i, j
        return False

    def __step1(self, matrix):
        for i in range(matrix.shape[0]):
            matrix[i, :] = matrix[i, :] - np.min(matrix[i, :])

    def __step2(self, matrix):
        for i in range(matrix.shape[1]):
            matrix[:, i] = matrix[:, i] - np.min(matrix[:, i])

    def __step3(self, m):
        dim = m.shape[0]
        assigned = np.array([])
        assignments = np.zeros(m.shape, dtype=int)

        for i in range(0, m.shape[0]):  # NOTE!!: changed dim into m.shape[0] (by Tommy)
            for j in range(0, m.shape[1]):  # NOTE!!: changed dim into m.shape[1] (by Tommy)
                if (m[i, j] == 0 and np.sum(assignments[:, j]) == 0 and np.sum(assignments[i, :]) == 0):
                    assignments[i, j] = 1
                    assigned = np.append(assigned, i)

        rows = np.linspace(0, dim - 1, dim).astype(int)
        marked_rows = np.setdiff1d(rows, assigned)
        new_marked_rows = marked_rows.copy()
        marked_cols = np.array([])

        while (len(new_marked_rows) > 0):
            new_marked_cols = np.array([], dtype=int)
            for nr in new_marked_rows:
                zeros_cols = np.argwhere(m[nr, :] == 0).reshape(-1)
                new_marked_cols = np.append(new_marked_cols, np.setdiff1d(zeros_cols, marked_cols))
            marked_cols = np.append(marked_cols, new_marked_cols)
            new_marked_rows = np.array([], dtype=int)

            for nc in new_marked_cols:
                new_marked_rows = np.append(new_marked_rows, np.argwhere(assignments[:, nc] == 1).reshape(-1))
            marked_rows = np.unique(np.append(marked_rows, new_marked_rows))
        return np.setdiff1d(rows, marked_rows), np.unique(marked_cols)

    def __step5(self, m, covered_rows, covered_cols):
        uncovered_rows = np.setdiff1d(np.linspace(0, m.shape[0] - 1, m.shape[0]), covered_rows).astype(int)
        uncovered_cols = np.setdiff1d(np.linspace(0, m.shape[1] - 1, m.shape[1]), covered_cols).astype(int)
        min_val = np.max(m)

        for i in uncovered_rows.astype(int):
            for j in uncovered_cols.astype(int):
                if (m[i, j] < min_val):
                    min_val = m[i, j]

        for i in uncovered_rows.astype(int):
            m[i, :] -= min_val

        for j in covered_cols.astype(int):
            m[:, j] += min_val
        return m



# Test
#a = np.random.randint(100, size=(3,3))
#a = np.matrix([[72, 23, 61], [35, 29, 13], [67, 2, 93]])
#a = np.matrix([[102, 120, 152], [152, 139, 174], [118, 146, 260]]) #esercitazione
#a = np.matrix([[17, 86, 46, 90], [79, 52, 62, 30], [37, 20, 36, 40]])
#a = np.matrix([[73, 84, 4], [97, 75, 43], [66, 42, 96]])
#a = np.matrix([[76, 31, 21, 58, 40], [50, 58, 57,94,70], [47, 69, 94,8,21], [13, 94, 81, 3, 50], [19, 46, 57, 84, 51]])

print (a)
res1 = Hungarian_algorithm().get_minimum_weight_assignment(a)
print("\n Optimal Matchin for minimizing cost:\n", res1)

res2 = Hungarian_algorithm().get_maximum_weight_assignment(a)
print("\n Optimal Matchin for maximizing cost:\n", res2)
