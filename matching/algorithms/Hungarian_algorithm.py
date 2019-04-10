import numpy as np
#from scipy.optimize import linear_sum_assignment

class Hungarian_algorithm:

    def compute(self, matrix):
        m = matrix.copy()
        self.__step1(m)
        self.__step2(m)
        n_lines = 0
        max_length = np.maximum(m.shape[0], m.shape[1])
        while n_lines != max_length:
            lines = self.__step3(m)
            n_lines = len(lines[0]) + len(lines[1])
            if (n_lines != max_length):
                self.__step5(m, lines[0], lines[1])
        return self.__final_assignement(matrix, m)

    def __final_assignement(self,initial_matrix, m):
        assignement = np.zeros(m.shape, dtype = int)
        assignement = self.__assignement_single_zero_lines(m, assignement)
        while(np.sum(m==0)>0):
            i,j = self.__first_zero(m)
            assignement[i,j] = i
            m[i,:] += 1
            m[:,j] += 1
            assignement = self.__assignement_single_zero_lines(m,assignement)

        return assignement* initial_matrix, assignement
    
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
                return i, j
        return False

    def __find_rows_single_zero(self, matrix):
        for i in range(0, matrix.shape[0]):
            if (np.sum(matrix[i, :] == 0) == 1):
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

        for i in range(0, dim):
            for j in range(0, dim):
                if (m[i, j] == 0 and np.sum(assignments[:, j]) == 0 and np.sum(assignments[i, :]) == 0):
                    assignments[i, j] = i
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
                new_marked_rows = np.append(new_marked_rows, np.argwhere(assignments[:, nc] == i).reshape(-1))
            marked_rows = np.unique(np.append(marked_rows, new_marked_rows))
        return np.setdiff1d(rows, marked_rows), np.unique(marked_cols)

    def __step5(self, m, covered_rows, covered_cols):
        uncovered_rows = np.setdiff1d(np.linspace(0, m.shape[0] - 1, m.shape[0]), covered_rows).astype(int)
        uncovered_cols = np.setdiff1d(np.linspace(0, m.shape[1] - 1, m.shape[1]), covered_rows).astype(int)
        min_val = np.max(m)

        for i in uncovered_cols.astype(int):
            for j in uncovered_cols.astype(int):
                if (m[i, j] < min_val):
                    min_val = m[i, j]

        for i in uncovered_rows.astype(int):
            m[i, :] -= min_val

        for j in covered_cols.astype(int):
            m[:, j] += min_val
        return m


def compute(matrix):
    hungarian = Hungarian_algorithm()
    return hungarian.compute(matrix)

# Test
# a = np.random.randint(100, size=(3,3))
# print (a)
# res1 = compute(a)
# print("\n Optimal Matchin:\n", res1[1], "\n Value: ", np.sum(res1[0]))
