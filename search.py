
def binarySearch(arr, l, r, x):
    while l <= r:
        mid = l + (r - l) // 2;

        if arr[mid] == x:
            return True
 
        elif arr[mid] < x:
            l = mid + 1
 
        else:
            r = mid - 1
            
    return -1

def linearSearch(arr, value):
    if value in arr:
        return True
    return False   