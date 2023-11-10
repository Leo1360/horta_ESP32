def filtroDesvPad(arr, num_std_dev=1):
    if len(arr) == 0:
        return 0
    
    # Calculate the mean of the input array
    arr_mean = sum(arr) / len(arr)

    # Calculate the standard deviation of the input array
    arr_std = (sum((x - arr_mean) ** 2 for x in arr) / len(arr)) ** 0.5

    # Calculate the threshold for filtering
    threshold = arr_std * num_std_dev

    # Filter out values more than 'num_std_dev' standard deviations away from the mean
    filtered_arr = [x for x in arr if abs(x - arr_mean) <= threshold]

    return filtered_arr

def mediaArray(arr):
    if len(arr) == 0:
        return 0  # Avoid division by zero if all values are filtered out
    media = sum(arr) / len(arr)
    return media
