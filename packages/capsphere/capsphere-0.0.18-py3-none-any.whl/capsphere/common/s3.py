def get_total_objects(bucket) -> int:
    count = 0
    for i in bucket.objects.all():
        count = count + 1

    return count
