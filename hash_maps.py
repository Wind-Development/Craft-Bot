# This is a class used to link data for mod-mail
class HashTable:

  # Original: https://www.geeksforgeeks.org/hash-map-in-python/

  # Constructs a hash table, this is much like a java hash map
  def __init__(self, size):
    self.size = size
    self.hash_table = self.create_buckets()

  def create_buckets(self):
    return [[] for _ in range(self.size)]

  def set_val(self, key, val):

    hashed_key = hash(key) % self.size

    bucket = self.hash_table[hashed_key]

    found_key = False
    for index, record in enumerate(bucket):
      record_key = record

      if record_key == key:
        found_key = True
        break

    if found_key:
      bucket[index] = (key, val)
    else:
      bucket.append((key, val))

  def get_val(self, key):

    hashed_key = hash(key) % self.size

    bucket = self.hash_table[hashed_key]

    found_key = False
    for record in enumerate(bucket):
      record_key = record

      if record_key == key:
          found_key = True
          break

    if found_key:
      return record_key
    else:
      return 'No record found'

  def delete_val(self, key):

    hashed_key = hash(key) % self.size

    bucket = self.hash_table[hashed_key]

    found_key = False
    for index, record in enumerate(bucket):
      record_key = record

      if record_key == key:
        found_key = True
        break
    if found_key:
      bucket.pop(index)
    return
