def saveToHDF(f,path,data):

  try:
    f.create_dataset(path,data=data)
  except ValueError:
    try:
      f[path][()] = data
    except TypeError:
      del f[path]
      f.create_dataset(path,data=data)
      
      
def isbinary(vector):
  return np.array_equal(vector, vector.astype(bool))



def arebinary(dictionary):

  for key in dictionary:
    if not isbinary(dictionary[key]['values']):
      return False
      break
  else:
    return True         




def contains(name, strings):
  answer = True
  for string in strings:
    if string not in name:
      answer = False
  return answer


def find_files(folder,strings):

    file_list = os.listdir(folder)
    files = []
    
    for file_name in file_list:
      if contains(file_name,strings):
        files.append(file_name)
    
    return files




def create_folder(new_folder):
  if not os.path.exists(new_folder):
    os.mkdir(new_folder)
      