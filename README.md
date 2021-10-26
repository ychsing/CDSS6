# PatientLikeMe_MatchingScore
## **使用範例**
import module
```python
import pandas as pd
from PatientLikeMe_MatchingScore import *
```
### - *DemoData*
```python
PLM_DemoData = pd.read_csv("PLM_DemoData.csv",encoding = 'big5')
```
```python
# raw data
Demo_soap_input = PLM_DemoData.loc[1][1]
Demo_report_input = PLM_DemoData.loc[1][2]

# raw data to structured
DemoData = PLM_DemoData.loc[1][4:].tolist()

weighted = [int(i) for i in PLM_DemoData.loc[0][4:-1].tolist()]
DB = PLM_DemoData.iloc[2:,:]
```
```python
score_sort = matching_score_df(DemoData, DB, weighted)
rec_drug, rec_sy, rec_score, candidate_patient_dict = recommends_drug(score_sort)
print('recommends drug:{}\nscore:{}\nsurvival_y:{}'.format(rec_drug, rec_score,rec_sy))
```
> recommends drug : Pemetrexed,Erlotinib,Vinorelbine,Gefitinib,Docetaxel <\br>
>score : 85.18 <\br>
>survival_y : >7.44 
