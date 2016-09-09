import json
import os
import numpy

dataset = "C:\\Users\\Kateryna\\testnow\\"
success_apis=[]
fail_apis=[]
return_codes=[]
sample_num=0

for sample in os.listdir(dataset):
    print "Reading file "+sample
    sample_num+=1
    with open(dataset+sample, 'rb') as fp:
        parsed_json=json.loads(fp.read())

    for n in parsed_json["behavior"]["processes"]:
        for k in n["calls"]:
            if k["status"] == 1:
                if k["api"] not in success_apis:
                    success_apis.append(k["api"])
            else:
                if k["api"] not in fail_apis:
                    fail_apis.append(k["api"])
            if k["return_value"] not in return_codes:
                return_codes.append(k["return_value"])
                
print len(success_apis)
print len(fail_apis)
print len(return_codes)
                    

matrix=numpy.zeros((sample_num,len(success_apis)+len(fail_apis)+len(return_codes)))
print (len(success_apis)+len(fail_apis)+len(return_codes))
ids=0

for sample in os.listdir(dataset):
    print sample
    with open(dataset+sample, 'rb') as fp:
        parsed_json=json.loads(fp.read())
    q=0
    for suc_api in success_apis:
        for n in parsed_json["behavior"]["processes"]:
            for k in n["calls"]:
                if suc_api in k["api"]:
                    matrix[ids][q]=matrix[ids][q]+1
                else:
                    matrix[ids][q]+=0
        q+=1
    for fail_api in fail_apis:
        for n in parsed_json["behavior"]["processes"]:
            for k in n["calls"]:
                if fail_api in k["api"]:
                    matrix[ids][q]=matrix[ids][q]+1
                else:
                    matrix[ids][q]+=0
        q+=1
    for code in return_codes:
        for n in parsed_json["behavior"]["processes"]:
            for k in n["calls"]:
                if code == k["return_value"]:
                    matrix[ids][q]=matrix[ids][q]+1
                else:
                    matrix[ids][q]+=0
        q+=1
    ids+=1
numpy.save('C:\\Users\\Kateryna\\data.npy', matrix)
print matrix
print q
##    
