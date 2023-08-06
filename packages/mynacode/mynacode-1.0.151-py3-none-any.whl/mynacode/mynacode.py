import numpy as np
import os, sys
import json, requests, ast
import pkg_resources
import GPUtil, platform, psutil
from datetime import datetime
from sklearn import metrics
import matplotlib.pyplot as plt
import dill
import urllib.request
import torch, itertools

#protocol = 'http'
protocol = 'https'

#IP = '127.0.0.1:8000'
IP = 'mynacode.com'

username = ""
key = ""
  

def login(uname, ky):
  global username
  global key
  
  print("Logging in...")
  credentials = {'username':uname, 'key':ky, 'task':'login'}
  response = requests.post(protocol+'://'+IP+'/api/python_login', data=credentials)
  
  if response.text == '1':
    username = uname
    key = ky
    print("Successfully connected to mynacode!")
  else:
    print("Credentials could not be verified.")


def metadata(run_id):

  installed_packages = pkg_resources.working_set #Save all installed packages for that project
  installed_packages_list = sorted(["%s = %s" % (i.key, i.version) for i in installed_packages])

  system_info_list = ['Codebase Python ' + platform.python_version()]
  
  system_info_list.append("    GPU    ")
  try:
      gpus = GPUtil.getGPUs()
      if len(gpus) == 0:
          system_info_list.append("No NVIDIA GPU found")
      else:
          for gpu in gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_memory = gpu.memoryTotal
            system_info_list.append("GPU ID " + str(gpu_id))
            system_info_list.append(gpu_name)
            system_info_list.append(str(gpu_memory) + " MB")
  except:
      system_info_list.append("No NVIDIA Driver found")

  system_info_list.append("    CPU    ")
  system_info_list.append(platform.processor())
  system_info_list.append(platform.platform())
  system_info_list.append(platform.machine())
  system_info_list.append("    MEMORY    ")
  system_info_list.append("RAM " + str(round(psutil.virtual_memory().total / (1024.0 **3))) + " GB")

  data = {'run_id' : run_id, 'installed_packages': str(installed_packages_list), 'username': username, 'key': key, 'system_information': str(system_info_list)}
  
  response = requests.post(protocol+'://'+IP+'/api/add_metadata', data=data)
  
  if response.text == '0':
    print("Authentication failed")
  else:
    print("Metadata saved")
  

def csv(run_id, dataframe):
    columns_list = dataframe.columns.values.tolist()
    isnull_list = dataframe.isnull().sum().values.tolist()
    isunique_list = dataframe.nunique().values.tolist()
    size = sys.getsizeof(dataframe)/1024
    shape = dataframe.shape
    dtypes_list = []

    for d in dataframe.dtypes:
        dtypes_list.append(str(d))

    data = {'run_id': run_id, 'columns_list': str(columns_list), 'isnull_list': str(isnull_list),
            'isunique_list': str(isunique_list), 'dtypes_list': str(dtypes_list),
            'username': username, 'size': int(size), 'shape': str(shape), 'key': key}

    response = requests.post(protocol+'://'+IP+'/api/add_csv', data=data)

    if response.text == '0':
      print("Authentication failed")
    else:
      print("CSV Information saved.")  

    

def specificity(y_true, y_pred):
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_truth = np.count_nonzero(y_true == 0)
   
    return float(y_correct/y_truth)

def npv(y_true, y_pred): #Negative Predicted Value
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_predicted = np.count_nonzero(y_pred == 0)
   
    return float(y_correct/y_predicted)

def get_roc_auc(y_true, y_pred):
    fpr, tpr, threshold = metrics.roc_curve(y_true, y_pred)
    roc_auc = metrics.auc(fpr, tpr)
    gmeans = np.sqrt(tpr * (1 - fpr)) #sensitivity * specificity (element-wise)
    index = np.argmax(gmeans) #Returns index of max value
    best_threshold = threshold[index]
   
    return fpr, tpr, roc_auc, gmeans, best_threshold, index

def get_metrics(y_true, y_pred, threshold):
    y_pred_binary = (y_pred > threshold).astype('float')
   
    prec = metrics.precision_score(y_true, y_pred_binary)
    rec = metrics.recall_score(y_true, y_pred_binary)
    spec = specificity(y_true, y_pred_binary)
    f1 = metrics.f1_score(y_true, y_pred_binary)
    acc = metrics.accuracy_score(y_true, y_pred_binary)
    npv_val = npv(y_true, y_pred_binary)
   
    c_matrix = metrics.confusion_matrix(y_true, y_pred_binary, labels=[0,1])
   
    return prec, rec, spec, f1, acc, npv_val, c_matrix


def save_torch_results(run_id, test_dataloader=None, test_dataloader_name='test', model=None, weights=None, threshold = 0.5, problem_type = 'binary classification', hist_bins=20):

    print("Using threshold = 0.5.")
    

    y_pred_list = []
    y_label_list = []
    
    net = load_torch_model(run_id)
    
    if test_dataloader==None:
      try:
        print("Using dataloader_name = 'test'")
        test_dataloader = load_torch_dataloader(run_id, test_dataloader_name)
      except:
        print("Please pass the test set dataloader object as a parameter or save the test set in a dedicated directory by running save_torch_dataloader(run_id, dataloader, dataloader_name)")
      
    net.eval()
    with torch.no_grad():
      for X_batch, y_batch in test_dataloader:
        y_test_pred = net(X_batch)
        y_pred_list.append(y_test_pred.detach().cpu().numpy())
        y_label_list.append(y_batch.detach().cpu().numpy())
      
    y_predicted = np.array(y_pred_list).flatten()
    y_true = np.array(y_label_list).flatten()
    
    prec, rec, spec, f1, acc, npv_val, c_matrix = get_metrics(y_true, y_predicted, threshold)
    fpr, tpr, roc_auc, gmeans, best_threshold, index = get_roc_auc(y_true, y_predicted)


    pred_hist = plt.hist(y_predicted, bins=hist_bins)
    freq = pred_hist[0]
    bins = pred_hist[1]

    data = {'run_id' : run_id, 'precision': round(prec, 4), 'recall': round(rec, 4), 'specificity': round(spec, 4),
            'f1': round(f1, 4), 'accuracy': round(acc, 4), 'npv': round(npv_val, 4), 'c_matrix': c_matrix,
            'username': username, 'key': key, 'test_auc': roc_auc, 'freq': freq, 'bins': hist_bins,
            'fpr': fpr, 'tpr': tpr}   

    print(data)
    
    response = requests.post(protocol+'://'+IP+'/api/add_results', data=data)
  
    if response.text == '0':
      print("Authentication failed")
    else:
      print("Results saved")


def save_torch_model(run_id, model):
    if not os.path.exists('mynacode'):
      os.mkdir('mynacode')
      
    with open('mynacode/'+str(run_id)+'/saved_network.pkl', 'wb') as f:
        dill.dump(model, f)

    torch.save(model.state_dict(), 'mynacode/'+str(run_id)+'/saved_state_dict.pt')
        
    files = {'network': open('mynacode/'+str(run_id)+'/saved_network.pkl','rb'), 'state_dict': open('mynacode/'+str(run_id)+'/saved_state_dict.pt','rb')}
    
    response = requests.post(protocol+'://'+IP+'/api/upload_pytorch_weights', files=files, data={'run_id':run_id, 'username': username, 'key': key})


def load_torch_model(run_id):

    response = requests.post(protocol+'://'+IP+'/api/get_pytorch_weights', data={'run_id':run_id, 'username': username, 'key': key})
    response = response.json()

    if not os.path.exists('mynacode'):
      os.mkdir('mynacode')

    if not os.path.exists('mynacode/'+str(run_id)):
      os.mkdir('mynacode/'+str(run_id))

    urllib.request.urlretrieve(response['weights'], 'mynacode/'+str(run_id)+'/'+response['weights'].split('/')[-1])
    urllib.request.urlretrieve(response['network'], 'mynacode/'+str(run_id)+'/'+response['network'].split('/')[-1])

    with open('mynacode/'+str(run_id)+'/saved_network.pkl', 'rb') as f:
        net = dill.load(f)


    net.load_state_dict(torch.load('mynacode/'+str(run_id)+'/saved_state_dict.pt'))

    return net

def save_torch_dataloader(run_id, dataloader, dataloader_name):
  mean_sum = 0
  batch_count = 0
  labels_count_zero = labels_count_one = 0
  _min = _max = 0
  sample_count = 0

  if not os.path.exists('mynacode'):
    os.mkdir('mynacode')

  if not os.path.exists('mynacode/'+str(run_id)):
    os.mkdir('mynacode/'+str(run_id))

  with open('mynacode/'+str(run_id)+'/'+dataloader_name+'.pkl', 'wb') as f:
      dill.dump(dataloader, f)

  for X_batch, y_batch in dataloader:
    mean_sum += np.mean(X_batch.detach().cpu().numpy())
    batch_count += 1
    labels_count_zero += np.count_nonzero(y_batch.detach().cpu().numpy() == 1)
    labels_count_one += np.count_nonzero(y_batch.detach().cpu().numpy() == 0)
    sample_count += len(X_batch)

    batch_shape = X_batch.detach().cpu().numpy().shape[1:]

    if np.min(X_batch.detach().cpu().numpy()) < _min:
      _min = np.min(X_batch.detach().cpu().numpy())

    if np.max(X_batch.detach().cpu().numpy()) > _max:
      _max = np.max(X_batch.detach().cpu().numpy())


  dataset_dict = {str(dataloader_name)+'_shape' : str((sample_count,) + batch_shape), str(dataloader_name)+'_mean': mean_sum/batch_count,
                str(dataloader_name)+'_min': _min, str(dataloader_name)+'_max': _max, str(dataloader_name)+'_zeros': labels_count_zero,
                str(dataloader_name)+'_ones': labels_count_one}

  post_data = {'run_id': run_id, 'dataset': str(dataset_dict), 'name': dataloader_name, 'username': username, 'key': key}

  response = requests.post(protocol+'://'+IP+'/api/add_dataset', data=post_data)
  
  if response.text == '0':
    print("Authentication failed")


def load_torch_dataloader(run_id, dataloader_name):
  print('Finding '+dataloader_name+' in directory '+ 'mynacode/'+str(run_id)+'/'+dataloader_name+'.pkl')
  with open('mynacode/'+str(run_id)+'/'+dataloader_name+'.pkl', 'rb') as f:
      dataloader = dill.load(f)

  return dataloader


def recreate_torch_results(run_id, test_dataloader=None, threshold=0.5):
  
  print("This function will use a default threshold of 0.5. Please change the parameter value if a different threshold is required.")

  y_pred_list = []
  y_label_list = []
  
  net = load_torch_model(run_id)
  
  if test_dataloader==None:
    test_dataloader = load_torch_dataloader(run_id, 'test')
    
  net.eval()
  with torch.no_grad():
    for X_batch, y_batch in test_dataloader:
      y_test_pred = net(X_batch)
      y_pred_list.append(y_test_pred.detach().cpu().numpy())
      y_label_list.append(y_batch.detach().cpu().numpy())
    
  y_predicted = np.array(y_pred_list).flatten()
  y_true = np.array(y_label_list).flatten()
  
  prec, rec, spec, f1, acc, npv_val, c_matrix = get_metrics(y_true, y_predicted, threshold)
  fpr, tpr, roc_auc, gmeans, best_threshold, index = get_roc_auc(y_true, y_predicted)
  print(prec, rec, spec, f1, acc, npv_val, c_matrix)
 



