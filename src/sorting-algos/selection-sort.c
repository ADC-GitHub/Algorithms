int selectionSort(double * inputArray, int numElements) {
    double key;

    if (numElements <= 0)
        return -1;
int i ;
int j ;
    for (i = 0; i < numElements; ++i) {
        key = inputArray[i];
        for (j = i + 1; j < numElements; ++j) {
            if (inputArray[j] < key) {
                inputArray[i] = inputArray[j];
                inputArray[j] = key;
                key = inputArray[i];
            }
        }
    }
    return 0;
}
