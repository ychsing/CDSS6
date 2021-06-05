# CDSS6

### 程式列表架構清單
```
| README.md
| use_module.ipynb
| module
├── MatchClinTrial.py
├── MatchResult.py
├── models.py
├── __init__.py
├── h5
│   ├── ALK_II_model.h5
│   ├── KRAS_II_model.h5
│   ├── ROS1_II_model.h5
│   ├── PDL1_model.h5
│   ├── Stage_model.h5
│   ├── gene_EGFR_model.h5
│   ├── gene_EGFR_18_model.h5
│   ├── gene_EGFR_19_model.h5
│   ├── gene_EGFR_20_model.h5
│   ├── gene_EGFR_21_model.h5
│   ├── Histology_model.h5
│   └── Operation_model.h5
├── pickle
│   ├── clinicalDB_report_tokenizer.pickle
└── └── clinicalDB_soap_tokenizer.pickle
```

### 環境
```python
import tensorflow as tf
print(tf.__version__)
```
> 2.1.0-rc1
```python
import keras
print(keras.__version__)
```
> 2.3.1

## **使用範例**
import module
```python
from module import MatchResult
```
進行匹配
```python
MatchResult.get_result(patient_json, criterias)
```
```
["criteria_A's match prob : 60.0 %",
 "criteria_B's match prob : 11.11 %",
 "criteria_C's match prob : 25.0 %",
 "criteria_D's match prob : 33.33 %",
 "criteria_E's match prob : 33.33 %",
 "criteria_F's match prob : 66.67 %"]
 ```

### - *Preparation parameters*
- [x] patient_json 
```python
patient_json = {
    "pathology_report":{
        "soap":"pathology soap content",
        "report":"pathology report content"
    },
    'manual_input':{"BRAF":'U',
                    "RET":'U',
                    "NTRK":'U',
                    "MET":'U',
                    "P53":'U',
                    'age': '45',
                    (略),
                     'ECOG': '0'}
    }
 ```
 - [X] criterias (Clinical Trials criterias)
 ```python
criterias = {
    "criteria_A":['1', 'NSCLC', [1,3], '', '18,19', '', '', '', '','', '', '','','',[18,75],'1','','','0','1','','','','','','','','','1','','','','',[4,5]],
    "criteria_B" : ["1",'SCLC',"","IIIB,IIIC,IVA,IVB",'N','N','N',"","","","","","","",[18,75],"","","","","","","","","","","","",'1',"","","","","progressed",""],
    "criteria_C" : ["1",'',"","IIIB,IIIC,IVA,IVB",'20','','',"","","","","","","","","","","","","0","0","","P","","","","","","","","","1","progressed",""],
    "criteria_D" : ["1",'NSCLC',"","IIIB,IIIC,IVA,IVB",'','P','',"","","","","","","","","","","","","0","","","","","","","0","","","","","","",""],
    "criteria_E" : ["1",'NSCLC',"","IIIA,IIIB,IIIC,IVA,IVB",'','P','',"","","","","","P","",[18,99],"","","","","","","","","","","","","","","","","","",""],
    "criteria_F" : ["0",'NSCLC',"","",'N','N','',"","","","","","","",[18,75],"","","","","1","","","","","","","","","","","","","",""]
}
```
* criteria order
```
["operation","histology","Tumor_size","stage","EGFR","ALK","ROS1","KRAS","PDL1", 
'BRAF', 'RET', 'NTRK', 'MET', 'P53', 'age', 'gender', 'smoking', 'Nodal_meta', 
 'distant_meta', 'cns_mata', 'bone_mata', 'wild_type', 'her2', 'anti_ang', 
 'platinum',  'EGFR_TKIs', 'ALK_inh', 'PDL1_inh', 'CTLA4_inh', 'Radiotherapy', 
 'Chemotherapy', 'systemic_therapy', 'disease_status', 'ECOG']
```

* manual input 共25項內容，出現型態如下

| id      | Phenotype     | Type     |
| :-----: | :-------------| :------: |
| 1     | BRAF     | U/N/P     |
|2|RET|U/N/P|
|3|NTRAK|U/N/P|
|4|MET|U/N/P|
|5|P53|U/N/P|
|6|Age|integer|
|7|Gender|0/1|
|8|smoking|0/1|
|9|Nodal  metastases|0/1|
|10|Distant metastases|0/1|
|11|CNS metastases|0/1|
|12|bone metastases|0/1|
|13|wild type|U/N/P|
|14|Her2|U/N/P|
|15|Anti-angiogenesis|0/1|
|16|Platinum |0/1|
|17|EGFR TKIs |0/1|
|18|ALK inhibitors |0/1|
|19|PD-1/PD-L1 inhibitors |0/1|
|20|CTLA-4 inhibitor |0/1|
|21|Raidotherapy|0/1|
|22|Chemotherapy|0/1|
|23|systemic therapy|0/1|
|24|Disease status |0/1|
|25|ECOG PS |0/1/2/3/4/5|
