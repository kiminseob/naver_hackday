def partition(alist,blist, start, end):
    pivot = alist[start]
    left = start+1
    right = end
    done = False
    while not done:
            while left <= right and alist[left] <= pivot:
                left += 1
            while alist[right] >= pivot and right >= left:
                right -= 1
            if right < left:
                        done = True
            else:
                tmp = alist[left]
                tmp2 = blist[left]
                alist[left] = alist[right]
                blist[left] = blist[right]
                alist[right] = tmp
                blist[right] = tmp2

    tmp = alist[start]
    tmp2 = blist[start]
    alist[start] = alist[right]
    blist[start] = blist[right]
    alist[right] = tmp
    blist[right] = tmp2
    return right

def quickSort(alist,blist, start, end):

    if start < end:
        pivot = partition(alist,blist, start, end)
        quickSort(alist,blist, start, pivot-1)
        quickSort(alist,blist, pivot+1, end)

    return alist
