class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        if matrixFilePath:
            self.matrix = {}
            self.numRows, self.numCols = self.reading_file(matrixFilePath)
        else:
            self.numRows = numRows
            self.numCols = numCols
            self.matrix = {}

    def reading_file(self, matrixFilePath):
        with open(matrixFilePath, 'r') as file:
            lines = file.readlines()

        try:
            numRows = int(lines[0].strip().split('=')[1])
            numCols = int(lines[1].strip().split('=')[1])

            for line in lines[2:]:
                line = line.strip()
                if line and line.startswith('(') and line.endswith(')'):
                    row, col, value = map(int, line[1:-1].split(','))
                    self.matrix[(row, col)] = value
                elif line:
                    raise ValueError("Input file has wrong format")

            return numRows, numCols

        except Exception as e:
            raise ValueError("Input file has wrong format") from e

    def getvalue(self, currRow, currCol):
        return self.matrix.get((currRow, currCol), 0)

    def setvalue(self, currRow, currCol, value):
        if value != 0:
            self.matrix[(currRow, currCol)] = value
        elif (currRow, currCol) in self.matrix:
            del self.matrix[(currRow, currCol)]

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for addition")

        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for (row, col), value in self.matrix.items():
            result.setvalue(row, col, value + other.getvalue(row, col))

        for (row, col), value in other.matrix.items():
            if (row, col) not in self.matrix:
                result.setvalue(row, col, value)

        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for subtraction")

        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for (row, col), value in self.matrix.items():
            result.setvalue(row, col, value - other.getvalue(row, col))

        for (row, col), value in other.matrix.items():
            if (row, col) not in self.matrix:
                result.setvalue(row, col, -value)

        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Number of columns in the first matrix must equal the number of rows in the second matrix")

        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)

        for (i, j), val in self.matrix.items():
            for k in range(other.numCols):
                result.setvalue(i, k, result.getvalue(i, k) + val * other.getvalue(j, k))

        return result

    def print_matrix(self):
        for row in range(self.numRows):
            for col in range(self.numCols):
                # Print each element with a tab separating columns
                print(self.getvalue(row, col), end="\t")
            print()  # Move to the next line after each row

    def print_sparse_matrix(self):
        for (row, col), value in self.matrix.items():
            print(f"({row}, {col}, {value})")


# Example usage:
if __name__ == "__main__":
    
    matrix1 = SparseMatrix("../../sample_inputs/easy_sample_02_2.txt")
    matrix2 = SparseMatrix("../../sample_inputs/easy_sample_02_1.txt")

    operation = input("Select operation: add, subtract, multiply: ")

    if operation == "add":
        result = matrix1.add(matrix2)
        print(result)
    elif operation == "subtract":
        result = matrix1.subtract(matrix2)
    elif operation == "multiply":
        result = matrix1.multiply(matrix2)
    else:
        print("Invalid operation selected")
        exit()

    # Print the resulting matrix
    print("Resulting Matrix:")
    result.print_sparse_matrix()  # Prints the full matrix (including zeros)