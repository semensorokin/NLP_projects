

```python
!ls
```

    cloze_task_average_accuracy.xlsx  Compare_data.md	 Tag_cloze_task.ipynb
    cloze_task_raw_data.xlsx	  LSTM_probability.xlsx
    Compare_data.ipynb		  output.xlsx



```python
import pandas as pd
data = pd.read_excel('LSTM_probability.xlsx')
data_cloze = pd.read_excel('cloze_task_raw_data.xlsx')
```


```python
data.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>item.id</th>
      <th>word.serial.no</th>
      <th>shown</th>
      <th>answer</th>
      <th>prob</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>Введите первое слово</td>
      <td>на</td>
      <td>0.016503</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>2</td>
      <td>На</td>
      <td>болотах</td>
      <td>0.000006</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>3</td>
      <td>На болотах</td>
      <td>оставался</td>
      <td>0.000138</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>4</td>
      <td>На болотах оставался</td>
      <td>еще</td>
      <td>0.124899</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>5</td>
      <td>На болотах оставался ещё</td>
      <td>лед</td>
      <td>0.002193</td>
    </tr>
  </tbody>
</table>
</div>




```python
data_cloze.shape
```




    (64645, 16)




```python
#for each sentence replace 'Введите первое слово'  with 'Start_X' according to sentence id
data_cloze.shown.replace('Введите первое слово', 'Start', inplace=True)
data_cloze[data_cloze.shown=='Start']
d_c_start = data_cloze[['shown', 'item.id']]
d_c_start['item.id'] = d_c_start['item.id'].astype(str)
d_c_start.loc[d_c_start.shown == 'Start', 'XXX'] = d_c_start.shown+'_'+d_c_start['item.id']
```

    /home/semen/anaconda3/lib/python3.7/site-packages/ipykernel_launcher.py:5: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      """
    /home/semen/anaconda3/lib/python3.7/site-packages/pandas/core/indexing.py:362: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self.obj[key] = _infer_fill_value(value)
    /home/semen/anaconda3/lib/python3.7/site-packages/pandas/core/indexing.py:543: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self.obj[item] = s



```python
data_cloze['app'] = d_c_start.XXX
import numpy as np
data_cloze['shown'] = np.where(data_cloze['shown']=='Start', data_cloze.app , data_cloze.shown)
data_cloze = data_cloze.drop('app', axis=1)
```


```python
data_cloze.shape, len(data_cloze.shown.unique())
```




    ((64645, 16), 1309)




```python
gb = data_cloze.groupby(['shown', 'answer', 'accuracy']).size()
gb = pd.DataFrame(gb,columns = ['fr'])
gb = gb.reset_index(level=['shown', 'answer', 'accuracy'])
gb.shape
```




    (25528, 4)




```python
gg= data_cloze.groupby(['shown', 'accuracy']).size()
gg = gg.reset_index(level=['shown', 'accuracy']) 
gg.columns = ['shown', 'accuracy', 'all_fr']
part0 = gg[gg.all_fr.max() == gg.all_fr]
max_value = gg[gg.shown == 'В'].all_fr.sum()
print(max_value)
gg.head(), gg.shape
```

    701





    (       shown  accuracy  all_fr
     0    Start_1       0.0     138
     1   Start_10       0.0      70
     2   Start_10       1.0       1
     3  Start_100       0.0      16
     4  Start_101       0.0      16, (1978, 3))




```python
gk= gg[['shown', 'all_fr', 'accuracy']].groupby(['shown']).sum()
gk = gk.reset_index(level=['shown'])
gk.columns = ['shown', 'sum_fr', 'accuracy']
gk.head(), gk.shape
gk[gk.accuracy==1.].shape
```




    (679, 3)




```python
gg = gg.merge(gk, left_on='shown', right_on='shown', how='outer')

```


```python
gg.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>shown</th>
      <th>accuracy_x</th>
      <th>all_fr</th>
      <th>sum_fr</th>
      <th>accuracy_y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Start_1</td>
      <td>0.0</td>
      <td>138</td>
      <td>138</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Start_10</td>
      <td>0.0</td>
      <td>70</td>
      <td>71</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Start_10</td>
      <td>1.0</td>
      <td>1</td>
      <td>71</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Start_100</td>
      <td>0.0</td>
      <td>16</td>
      <td>16</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Start_101</td>
      <td>0.0</td>
      <td>16</td>
      <td>16</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
print(gg.head())
def normal(x):
    return max_value/x
gg['index_norm'] = gg.sum_fr
gg.index_norm = gg.index_norm.apply(normal)
print(gg.head())
gg['prob'] = np.where(gg.accuracy_x==1., (gg.all_fr*gg.index_norm)/(gg.index_norm*gg.sum_fr), 0.0000000000000000001)
res = gg[['shown', 'accuracy_x','sum_fr','prob']]
res = res[res.prob!=0.]
print(res.shape)
print(res.head())
```

           shown  accuracy_x  all_fr  sum_fr  accuracy_y
    0    Start_1         0.0     138     138         0.0
    1   Start_10         0.0      70      71         1.0
    2   Start_10         1.0       1      71         1.0
    3  Start_100         0.0      16      16         0.0
    4  Start_101         0.0      16      16         0.0
           shown  accuracy_x  all_fr  sum_fr  accuracy_y  index_norm
    0    Start_1         0.0     138     138         0.0    5.079710
    1   Start_10         0.0      70      71         1.0    9.873239
    2   Start_10         1.0       1      71         1.0    9.873239
    3  Start_100         0.0      16      16         0.0   43.812500
    4  Start_101         0.0      16      16         0.0   43.812500
    (1978, 4)
           shown  accuracy_x  sum_fr          prob
    0    Start_1         0.0     138  1.000000e-19
    1   Start_10         0.0      71  1.000000e-19
    2   Start_10         1.0      71  1.408451e-02
    3  Start_100         0.0      16  1.000000e-19
    4  Start_101         0.0      16  1.000000e-19



```python
r = res[['shown','accuracy_x', 'prob']].groupby(['shown']).sum()
r = r.reset_index(level=['shown'])
print(r.shape)
#r.sum_fr = np.where(r.shown==res.shown, res.sum_fr, 0)
r.head()
```

    (1309, 3)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>shown</th>
      <th>accuracy_x</th>
      <th>prob</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Start_1</td>
      <td>0.0</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Start_10</td>
      <td>1.0</td>
      <td>1.408451e-02</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Start_100</td>
      <td>0.0</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Start_101</td>
      <td>0.0</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Start_102</td>
      <td>0.0</td>
      <td>1.000000e-19</td>
    </tr>
  </tbody>
</table>
</div>




```python
r[r.prob>=1.]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>shown</th>
      <th>accuracy_x</th>
      <th>prob</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>233</th>
      <td>В современном обществе семья и школа оказывают...</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>305</th>
      <td>Во избежание ожогов надо нанести на лицо небол...</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>307</th>
      <td>Во избежание ожогов надо нанести на лицо небол...</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>389</th>
      <td>Дрозды и скворцы начали вить семейные гнёзда н...</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>511</th>
      <td>Зачем ему звонить‚ если откликается спокойный ...</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>550</th>
      <td>Ирине досталась отдельная комната в двухкомнатной</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>565</th>
      <td>Какие главные лекарства должны входить</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>802</th>
      <td>Олень бродил среди берёз‚ жевал талый снег</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1022</th>
      <td>С нескрываемой едкой иронией отзываются они др...</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1040</th>
      <td>Собаку‚ виновницу случившегося‚ приказали сечь...</td>
      <td>1.0</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
data.shown.unique().shape
```




    (1170,)




```python
data.shown.replace('Введите первое слово', 'Start', inplace=True)
#data[data.shown=='Start']
d_start = data[['shown', 'item.id']]
d_start['item.id'] = d_start['item.id'].astype(str)
d_start.loc[d_start.shown == 'Start', 'XXX'] = d_start.shown+'_'+d_c_start['item.id']
data['app'] = d_start.XXX
data['shown'] = np.where(data['shown']=='Start', data.app , data.shown)
data = data.drop('app', axis=1)
data.shown.unique().shape

```

    /home/semen/anaconda3/lib/python3.7/site-packages/ipykernel_launcher.py:4: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      after removing the cwd from sys.path.
    /home/semen/anaconda3/lib/python3.7/site-packages/pandas/core/indexing.py:362: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self.obj[key] = _infer_fill_value(value)
    /home/semen/anaconda3/lib/python3.7/site-packages/pandas/core/indexing.py:543: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self.obj[item] = s





    (1185,)




```python
data_m = data.merge(r, left_on='shown', right_on='shown', how='outer')
```


```python
data_m.shown.unique().shape
```




    (1310,)




```python
#data_m = data_m.dropna()
result = data_m[['shown', 'answer', 'prob_x', 'prob_y']]
result[result.prob_y<0.0001]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>shown</th>
      <th>answer</th>
      <th>prob_x</th>
      <th>prob_y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Start_102</td>
      <td>на</td>
      <td>1.650273e-02</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Start_102</td>
      <td>он</td>
      <td>1.442693e-02</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Start_102</td>
      <td>ваня</td>
      <td>3.091045e-05</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Start_102</td>
      <td>сделав</td>
      <td>3.943548e-05</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Start_102</td>
      <td>я</td>
      <td>1.338693e-02</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Start_102</td>
      <td>дорога</td>
      <td>6.815995e-05</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Start_102</td>
      <td>не</td>
      <td>7.830556e-03</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Start_102</td>
      <td>выходя</td>
      <td>3.651174e-05</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Start_102</td>
      <td>и</td>
      <td>3.465874e-02</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Start_102</td>
      <td>у</td>
      <td>5.279777e-03</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Start_102</td>
      <td>очень</td>
      <td>7.828477e-04</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Start_102</td>
      <td>на</td>
      <td>1.650273e-02</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Start_102</td>
      <td>наживка</td>
      <td>6.170017e-07</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Start_102</td>
      <td>мне</td>
      <td>1.859887e-03</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Start_102</td>
      <td>город</td>
      <td>1.382068e-04</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Start_102</td>
      <td>в</td>
      <td>6.357282e-02</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Start_102</td>
      <td>здесь</td>
      <td>1.354696e-03</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Start_102</td>
      <td>у</td>
      <td>5.279777e-03</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>18</th>
      <td>На</td>
      <td>болотах</td>
      <td>6.423551e-06</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>19</th>
      <td>На</td>
      <td>привале</td>
      <td>4.040287e-05</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>20</th>
      <td>На</td>
      <td>газовой</td>
      <td>2.183123e-05</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>21</th>
      <td>На</td>
      <td>узкой</td>
      <td>4.291669e-05</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>22</th>
      <td>На</td>
      <td>ольгу</td>
      <td>1.001641e-05</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>23</th>
      <td>На</td>
      <td>массаже</td>
      <td>1.357266e-06</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>24</th>
      <td>На</td>
      <td>запись</td>
      <td>2.346074e-05</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>25</th>
      <td>На</td>
      <td>вторичном</td>
      <td>2.160513e-05</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>26</th>
      <td>На болотах</td>
      <td>оставался</td>
      <td>1.375087e-04</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>28</th>
      <td>На болотах оставался ещё</td>
      <td>лед</td>
      <td>2.192784e-03</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>33</th>
      <td>На болотах оставался ещё лёд‚ но на берегах реки</td>
      <td>появилась</td>
      <td>6.698859e-04</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>41</th>
      <td>Он ловко</td>
      <td>поддел</td>
      <td>4.475961e-03</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1453</th>
      <td>Start_63</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1454</th>
      <td>Start_64</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1455</th>
      <td>Start_65</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1456</th>
      <td>Start_66</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1458</th>
      <td>Start_68</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1459</th>
      <td>Start_69</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1460</th>
      <td>Start_7</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1461</th>
      <td>Start_70</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1462</th>
      <td>Start_71</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1463</th>
      <td>Start_73</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1464</th>
      <td>Start_74</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1466</th>
      <td>Start_76</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1468</th>
      <td>Start_8</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1469</th>
      <td>Start_81</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1470</th>
      <td>Start_82</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1471</th>
      <td>Start_83</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1472</th>
      <td>Start_84</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1474</th>
      <td>Start_86</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1475</th>
      <td>Start_87</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1476</th>
      <td>Start_88</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1477</th>
      <td>Start_89</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1478</th>
      <td>Start_9</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1479</th>
      <td>Start_90</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1480</th>
      <td>Start_91</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1482</th>
      <td>Start_94</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1483</th>
      <td>Start_95</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1484</th>
      <td>Start_96</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1485</th>
      <td>Start_97</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1486</th>
      <td>Start_98</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
    <tr>
      <th>1487</th>
      <td>Start_99</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.000000e-19</td>
    </tr>
  </tbody>
</table>
<p>724 rows × 4 columns</p>
</div>




```python
#print(check.shape)
check = data_cloze[['shown', 'answer']]
check = check.drop_duplicates()
data_result =  result.merge(check, left_on='shown', right_on='shown', how='outer')
data_result.shape
```




    (38346, 5)




```python
data_result = data_result[data_result.answer_x == data_result.answer_y]
data_result = data_result[['shown','answer_x','prob_x','prob_y']]
```


```python
data_result.columns = ['shown', 'answer', 'prob_by_model', 'prob_by_human']
data_result['$R^2$'] = (data_result.prob_by_human-data_result.prob_by_model)**2
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>item.id</th>
      <th>word.serial.no</th>
      <th>shown</th>
      <th>answer</th>
      <th>prob</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>Start_102</td>
      <td>на</td>
      <td>0.016503</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>2</td>
      <td>На</td>
      <td>болотах</td>
      <td>0.000006</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>3</td>
      <td>На болотах</td>
      <td>оставался</td>
      <td>0.000138</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>4</td>
      <td>На болотах оставался</td>
      <td>еще</td>
      <td>0.124899</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>5</td>
      <td>На болотах оставался ещё</td>
      <td>лед</td>
      <td>0.002193</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1</td>
      <td>6</td>
      <td>На болотах оставался ещё лёд‚</td>
      <td>но</td>
      <td>0.039917</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1</td>
      <td>7</td>
      <td>На болотах оставался ещё лёд‚ но</td>
      <td>на</td>
      <td>0.031502</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1</td>
      <td>8</td>
      <td>На болотах оставался ещё лёд‚ но на</td>
      <td>берегах</td>
      <td>0.003701</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1</td>
      <td>9</td>
      <td>На болотах оставался ещё лёд‚ но на берегах</td>
      <td>реки</td>
      <td>0.014212</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1</td>
      <td>10</td>
      <td>На болотах оставался ещё лёд‚ но на берегах реки</td>
      <td>появилась</td>
      <td>0.000670</td>
    </tr>
    <tr>
      <th>10</th>
      <td>1</td>
      <td>11</td>
      <td>На болотах оставался ещё лёд‚ но на берегах ре...</td>
      <td>трава</td>
      <td>0.003874</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2</td>
      <td>1</td>
      <td>Start_102</td>
      <td>он</td>
      <td>0.014427</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2</td>
      <td>2</td>
      <td>Он</td>
      <td>ловко</td>
      <td>0.000068</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2</td>
      <td>3</td>
      <td>Он ловко</td>
      <td>поддел</td>
      <td>0.004476</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2</td>
      <td>4</td>
      <td>Он ловко поддел</td>
      <td>концом</td>
      <td>0.000468</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2</td>
      <td>5</td>
      <td>Он ловко поддел концом</td>
      <td>ножа</td>
      <td>0.045508</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2</td>
      <td>6</td>
      <td>Он ловко поддел концом ножа</td>
      <td>замочки</td>
      <td>0.000002</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2</td>
      <td>7</td>
      <td>Он ловко поддел концом ножа замочки‚</td>
      <td>и</td>
      <td>0.051944</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2</td>
      <td>8</td>
      <td>Он ловко поддел концом ножа замочки‚ и</td>
      <td>они</td>
      <td>0.072151</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2</td>
      <td>9</td>
      <td>Он ловко поддел концом ножа замочки‚ и они</td>
      <td>отскочили</td>
      <td>0.002742</td>
    </tr>
    <tr>
      <th>20</th>
      <td>3</td>
      <td>1</td>
      <td>Start_102</td>
      <td>ваня</td>
      <td>0.000031</td>
    </tr>
    <tr>
      <th>21</th>
      <td>3</td>
      <td>2</td>
      <td>Ваня</td>
      <td>раскрыл</td>
      <td>0.000194</td>
    </tr>
    <tr>
      <th>22</th>
      <td>3</td>
      <td>3</td>
      <td>Ваня раскрыл</td>
      <td>было</td>
      <td>0.004079</td>
    </tr>
    <tr>
      <th>23</th>
      <td>3</td>
      <td>4</td>
      <td>Ваня раскрыл было</td>
      <td>рот</td>
      <td>0.467625</td>
    </tr>
    <tr>
      <th>24</th>
      <td>3</td>
      <td>5</td>
      <td>Ваня раскрыл было рот‚</td>
      <td>но</td>
      <td>0.661029</td>
    </tr>
    <tr>
      <th>25</th>
      <td>3</td>
      <td>6</td>
      <td>Ваня раскрыл было рот‚ но</td>
      <td>понял</td>
      <td>0.004546</td>
    </tr>
    <tr>
      <th>26</th>
      <td>3</td>
      <td>7</td>
      <td>Ваня раскрыл было рот‚ но понял‚</td>
      <td>что</td>
      <td>0.958914</td>
    </tr>
    <tr>
      <th>27</th>
      <td>3</td>
      <td>8</td>
      <td>Ваня раскрыл было рот‚ но понял‚ что</td>
      <td>что-то</td>
      <td>0.001715</td>
    </tr>
    <tr>
      <th>28</th>
      <td>3</td>
      <td>9</td>
      <td>Ваня раскрыл было рот‚ но понял‚ что что-то</td>
      <td>не</td>
      <td>0.241922</td>
    </tr>
    <tr>
      <th>29</th>
      <td>3</td>
      <td>10</td>
      <td>Ваня раскрыл было рот‚ но понял‚ что что-то не</td>
      <td>так</td>
      <td>0.575578</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1333</th>
      <td>142</td>
      <td>1</td>
      <td>Start_56</td>
      <td>ненужный</td>
      <td>0.000001</td>
    </tr>
    <tr>
      <th>1334</th>
      <td>142</td>
      <td>2</td>
      <td>Ненужный</td>
      <td>коврик</td>
      <td>0.000038</td>
    </tr>
    <tr>
      <th>1335</th>
      <td>142</td>
      <td>3</td>
      <td>Ненужный коврик</td>
      <td>из</td>
      <td>0.012761</td>
    </tr>
    <tr>
      <th>1336</th>
      <td>142</td>
      <td>4</td>
      <td>Ненужный коврик из</td>
      <td>твердой</td>
      <td>0.000035</td>
    </tr>
    <tr>
      <th>1337</th>
      <td>142</td>
      <td>5</td>
      <td>Ненужный коврик из твёрдой</td>
      <td>пластмассы</td>
      <td>0.010510</td>
    </tr>
    <tr>
      <th>1338</th>
      <td>142</td>
      <td>6</td>
      <td>Ненужный коврик из твёрдой пластмассы</td>
      <td>пригодится</td>
      <td>0.000660</td>
    </tr>
    <tr>
      <th>1339</th>
      <td>142</td>
      <td>7</td>
      <td>Ненужный коврик из твёрдой пластмассы пригодится</td>
      <td>как</td>
      <td>0.021249</td>
    </tr>
    <tr>
      <th>1340</th>
      <td>142</td>
      <td>8</td>
      <td>Ненужный коврик из твёрдой пластмассы пригодит...</td>
      <td>подставка</td>
      <td>0.000019</td>
    </tr>
    <tr>
      <th>1341</th>
      <td>142</td>
      <td>9</td>
      <td>Ненужный коврик из твёрдой пластмассы пригодит...</td>
      <td>для</td>
      <td>0.512068</td>
    </tr>
    <tr>
      <th>1342</th>
      <td>142</td>
      <td>10</td>
      <td>Ненужный коврик из твёрдой пластмассы пригодит...</td>
      <td>посуды</td>
      <td>0.008749</td>
    </tr>
    <tr>
      <th>1343</th>
      <td>143</td>
      <td>1</td>
      <td>Start_78</td>
      <td>когда</td>
      <td>0.004141</td>
    </tr>
    <tr>
      <th>1344</th>
      <td>143</td>
      <td>2</td>
      <td>Когда</td>
      <td>родители</td>
      <td>0.000715</td>
    </tr>
    <tr>
      <th>1345</th>
      <td>143</td>
      <td>3</td>
      <td>Когда родители</td>
      <td>пригрозили</td>
      <td>0.000205</td>
    </tr>
    <tr>
      <th>1346</th>
      <td>143</td>
      <td>4</td>
      <td>Когда родители пригрозили</td>
      <td>не</td>
      <td>0.003967</td>
    </tr>
    <tr>
      <th>1347</th>
      <td>143</td>
      <td>5</td>
      <td>Когда родители пригрозили не</td>
      <td>взять</td>
      <td>0.000895</td>
    </tr>
    <tr>
      <th>1348</th>
      <td>143</td>
      <td>6</td>
      <td>Когда родители пригрозили не взять</td>
      <td>ее</td>
      <td>0.013125</td>
    </tr>
    <tr>
      <th>1349</th>
      <td>143</td>
      <td>7</td>
      <td>Когда родители пригрозили не взять её</td>
      <td>с</td>
      <td>0.098012</td>
    </tr>
    <tr>
      <th>1350</th>
      <td>143</td>
      <td>8</td>
      <td>Когда родители пригрозили не взять её с</td>
      <td>собой</td>
      <td>0.859795</td>
    </tr>
    <tr>
      <th>1351</th>
      <td>143</td>
      <td>9</td>
      <td>Когда родители пригрозили не взять её с собой‚</td>
      <td>маша</td>
      <td>0.000831</td>
    </tr>
    <tr>
      <th>1352</th>
      <td>143</td>
      <td>10</td>
      <td>Когда родители пригрозили не взять её с собой‚...</td>
      <td>очень</td>
      <td>0.002211</td>
    </tr>
    <tr>
      <th>1353</th>
      <td>143</td>
      <td>11</td>
      <td>Когда родители пригрозили не взять её с собой‚...</td>
      <td>расстроилась</td>
      <td>0.051342</td>
    </tr>
    <tr>
      <th>1354</th>
      <td>144</td>
      <td>1</td>
      <td>Первое слово</td>
      <td>от</td>
      <td>0.001596</td>
    </tr>
    <tr>
      <th>1355</th>
      <td>144</td>
      <td>2</td>
      <td>От</td>
      <td>внимания</td>
      <td>0.000231</td>
    </tr>
    <tr>
      <th>1356</th>
      <td>144</td>
      <td>3</td>
      <td>От внимания</td>
      <td>наблюдателя</td>
      <td>0.000024</td>
    </tr>
    <tr>
      <th>1357</th>
      <td>144</td>
      <td>4</td>
      <td>От внимания наблюдателя</td>
      <td>не</td>
      <td>0.042131</td>
    </tr>
    <tr>
      <th>1358</th>
      <td>144</td>
      <td>5</td>
      <td>От внимания наблюдателя не</td>
      <td>должна</td>
      <td>0.000957</td>
    </tr>
    <tr>
      <th>1359</th>
      <td>144</td>
      <td>6</td>
      <td>От внимания наблюдателя не должна</td>
      <td>ускользать</td>
      <td>0.000054</td>
    </tr>
    <tr>
      <th>1360</th>
      <td>144</td>
      <td>7</td>
      <td>От внимания наблюдателя не должна ускользать</td>
      <td>даже</td>
      <td>0.009129</td>
    </tr>
    <tr>
      <th>1361</th>
      <td>144</td>
      <td>8</td>
      <td>От внимания наблюдателя не должна ускользать даже</td>
      <td>малейшая</td>
      <td>0.005202</td>
    </tr>
    <tr>
      <th>1362</th>
      <td>144</td>
      <td>9</td>
      <td>От внимания наблюдателя не должна ускользать д...</td>
      <td>деталь</td>
      <td>0.148185</td>
    </tr>
  </tbody>
</table>
<p>1363 rows × 5 columns</p>
</div>




```python
data_result[data_result.prob_by_human<0.0001]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>shown</th>
      <th>answer</th>
      <th>prob_by_model</th>
      <th>prob_by_human</th>
      <th>$R^2$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>24</th>
      <td>Start_102</td>
      <td>он</td>
      <td>0.014427</td>
      <td>1.000000e-19</td>
      <td>2.081363e-04</td>
    </tr>
    <tr>
      <th>79</th>
      <td>Start_102</td>
      <td>я</td>
      <td>0.013387</td>
      <td>1.000000e-19</td>
      <td>1.792099e-04</td>
    </tr>
    <tr>
      <th>101</th>
      <td>Start_102</td>
      <td>не</td>
      <td>0.007831</td>
      <td>1.000000e-19</td>
      <td>6.131761e-05</td>
    </tr>
    <tr>
      <th>226</th>
      <td>Start_102</td>
      <td>город</td>
      <td>0.000138</td>
      <td>1.000000e-19</td>
      <td>1.910112e-08</td>
    </tr>
    <tr>
      <th>241</th>
      <td>Start_102</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
    </tr>
    <tr>
      <th>10456</th>
      <td>Start_50</td>
      <td>однако</td>
      <td>0.006184</td>
      <td>1.000000e-19</td>
      <td>3.823848e-05</td>
    </tr>
    <tr>
      <th>10573</th>
      <td>Start_50</td>
      <td>он</td>
      <td>0.014427</td>
      <td>1.000000e-19</td>
      <td>2.081363e-04</td>
    </tr>
    <tr>
      <th>11037</th>
      <td>Start_50</td>
      <td>он</td>
      <td>0.014427</td>
      <td>1.000000e-19</td>
      <td>2.081363e-04</td>
    </tr>
    <tr>
      <th>11165</th>
      <td>Start_50</td>
      <td>у</td>
      <td>0.005280</td>
      <td>1.000000e-19</td>
      <td>2.787604e-05</td>
    </tr>
    <tr>
      <th>11629</th>
      <td>Start_50</td>
      <td>у</td>
      <td>0.005280</td>
      <td>1.000000e-19</td>
      <td>2.787604e-05</td>
    </tr>
    <tr>
      <th>11715</th>
      <td>Start_50</td>
      <td>за</td>
      <td>0.004480</td>
      <td>1.000000e-19</td>
      <td>2.006795e-05</td>
    </tr>
    <tr>
      <th>11959</th>
      <td>Start_50</td>
      <td>на</td>
      <td>0.016503</td>
      <td>1.000000e-19</td>
      <td>2.723400e-04</td>
    </tr>
    <tr>
      <th>12075</th>
      <td>Start_50</td>
      <td>на</td>
      <td>0.016503</td>
      <td>1.000000e-19</td>
      <td>2.723400e-04</td>
    </tr>
    <tr>
      <th>12163</th>
      <td>Start_50</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
    </tr>
    <tr>
      <th>12221</th>
      <td>Start_50</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
    </tr>
    <tr>
      <th>12337</th>
      <td>Start_50</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
    </tr>
    <tr>
      <th>12511</th>
      <td>Start_50</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
    </tr>
    <tr>
      <th>12713</th>
      <td>Start_50</td>
      <td>на</td>
      <td>0.016503</td>
      <td>1.000000e-19</td>
      <td>2.723400e-04</td>
    </tr>
    <tr>
      <th>12832</th>
      <td>Start_50</td>
      <td>но</td>
      <td>0.029389</td>
      <td>1.000000e-19</td>
      <td>8.637302e-04</td>
    </tr>
    <tr>
      <th>13003</th>
      <td>Start_50</td>
      <td>на</td>
      <td>0.016503</td>
      <td>1.000000e-19</td>
      <td>2.723400e-04</td>
    </tr>
    <tr>
      <th>13366</th>
      <td>Start_50</td>
      <td>там</td>
      <td>0.001764</td>
      <td>1.000000e-19</td>
      <td>3.110466e-06</td>
    </tr>
    <tr>
      <th>13485</th>
      <td>Start_50</td>
      <td>у</td>
      <td>0.005280</td>
      <td>1.000000e-19</td>
      <td>2.787604e-05</td>
    </tr>
    <tr>
      <th>13531</th>
      <td>Start_50</td>
      <td>он</td>
      <td>0.014427</td>
      <td>1.000000e-19</td>
      <td>2.081363e-04</td>
    </tr>
    <tr>
      <th>13555</th>
      <td>Start_50</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
    </tr>
    <tr>
      <th>24144</th>
      <td>Start_16</td>
      <td>на</td>
      <td>0.016503</td>
      <td>1.000000e-19</td>
      <td>2.723400e-04</td>
    </tr>
    <tr>
      <th>24376</th>
      <td>Start_16</td>
      <td>на</td>
      <td>0.016503</td>
      <td>1.000000e-19</td>
      <td>2.723400e-04</td>
    </tr>
    <tr>
      <th>26235</th>
      <td>Start_131</td>
      <td>я</td>
      <td>0.013387</td>
      <td>1.000000e-19</td>
      <td>1.792099e-04</td>
    </tr>
  </tbody>
</table>
</div>




```python
measure = data_result[data_result.prob_by_model<data_result.prob_by_human].shape[0]/data_result.shape[0]
print("{}% of data, where prob of cloze task is greater than prob of lstm ".format(round(measure,2)))
```

    0.81% of data, where prob of cloze task is greater than prob of lstm 



```python
data_result['Cross_entropy'] = -(0.0*np.log(data_result.prob_by_model)+1.0*np.log(data_result.prob_by_human))
```

    /home/semen/anaconda3/lib/python3.7/site-packages/ipykernel_launcher.py:1: RuntimeWarning: divide by zero encountered in log
      """Entry point for launching an IPython kernel.



```python
data_result.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>shown</th>
      <th>answer</th>
      <th>prob_by_model</th>
      <th>prob_by_human</th>
      <th>$R^2$</th>
      <th>Cross_entropy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>24</th>
      <td>Start_102</td>
      <td>он</td>
      <td>0.014427</td>
      <td>1.000000e-19</td>
      <td>2.081363e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>79</th>
      <td>Start_102</td>
      <td>я</td>
      <td>0.013387</td>
      <td>1.000000e-19</td>
      <td>1.792099e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>101</th>
      <td>Start_102</td>
      <td>не</td>
      <td>0.007831</td>
      <td>1.000000e-19</td>
      <td>6.131761e-05</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>226</th>
      <td>Start_102</td>
      <td>город</td>
      <td>0.000138</td>
      <td>1.000000e-19</td>
      <td>1.910112e-08</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>241</th>
      <td>Start_102</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
      <td>43.749117</td>
    </tr>
  </tbody>
</table>
</div>




```python
data_result[data_result.prob_by_human<0.00000000001]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>shown</th>
      <th>answer</th>
      <th>prob_by_model</th>
      <th>prob_by_human</th>
      <th>$R^2$</th>
      <th>Cross_entropy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>24</th>
      <td>Start_102</td>
      <td>он</td>
      <td>0.014427</td>
      <td>1.000000e-19</td>
      <td>2.081363e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>79</th>
      <td>Start_102</td>
      <td>я</td>
      <td>0.013387</td>
      <td>1.000000e-19</td>
      <td>1.792099e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>101</th>
      <td>Start_102</td>
      <td>не</td>
      <td>0.007831</td>
      <td>1.000000e-19</td>
      <td>6.131761e-05</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>226</th>
      <td>Start_102</td>
      <td>город</td>
      <td>0.000138</td>
      <td>1.000000e-19</td>
      <td>1.910112e-08</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>241</th>
      <td>Start_102</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>10456</th>
      <td>Start_50</td>
      <td>однако</td>
      <td>0.006184</td>
      <td>1.000000e-19</td>
      <td>3.823848e-05</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>10573</th>
      <td>Start_50</td>
      <td>он</td>
      <td>0.014427</td>
      <td>1.000000e-19</td>
      <td>2.081363e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>11037</th>
      <td>Start_50</td>
      <td>он</td>
      <td>0.014427</td>
      <td>1.000000e-19</td>
      <td>2.081363e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>11165</th>
      <td>Start_50</td>
      <td>у</td>
      <td>0.005280</td>
      <td>1.000000e-19</td>
      <td>2.787604e-05</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>11629</th>
      <td>Start_50</td>
      <td>у</td>
      <td>0.005280</td>
      <td>1.000000e-19</td>
      <td>2.787604e-05</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>11715</th>
      <td>Start_50</td>
      <td>за</td>
      <td>0.004480</td>
      <td>1.000000e-19</td>
      <td>2.006795e-05</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>11959</th>
      <td>Start_50</td>
      <td>на</td>
      <td>0.016503</td>
      <td>1.000000e-19</td>
      <td>2.723400e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>12075</th>
      <td>Start_50</td>
      <td>на</td>
      <td>0.016503</td>
      <td>1.000000e-19</td>
      <td>2.723400e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>12163</th>
      <td>Start_50</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>12221</th>
      <td>Start_50</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>12337</th>
      <td>Start_50</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>12511</th>
      <td>Start_50</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>12713</th>
      <td>Start_50</td>
      <td>на</td>
      <td>0.016503</td>
      <td>1.000000e-19</td>
      <td>2.723400e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>12832</th>
      <td>Start_50</td>
      <td>но</td>
      <td>0.029389</td>
      <td>1.000000e-19</td>
      <td>8.637302e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>13003</th>
      <td>Start_50</td>
      <td>на</td>
      <td>0.016503</td>
      <td>1.000000e-19</td>
      <td>2.723400e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>13366</th>
      <td>Start_50</td>
      <td>там</td>
      <td>0.001764</td>
      <td>1.000000e-19</td>
      <td>3.110466e-06</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>13485</th>
      <td>Start_50</td>
      <td>у</td>
      <td>0.005280</td>
      <td>1.000000e-19</td>
      <td>2.787604e-05</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>13531</th>
      <td>Start_50</td>
      <td>он</td>
      <td>0.014427</td>
      <td>1.000000e-19</td>
      <td>2.081363e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>13555</th>
      <td>Start_50</td>
      <td>в</td>
      <td>0.063573</td>
      <td>1.000000e-19</td>
      <td>4.041504e-03</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>24144</th>
      <td>Start_16</td>
      <td>на</td>
      <td>0.016503</td>
      <td>1.000000e-19</td>
      <td>2.723400e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>24376</th>
      <td>Start_16</td>
      <td>на</td>
      <td>0.016503</td>
      <td>1.000000e-19</td>
      <td>2.723400e-04</td>
      <td>43.749117</td>
    </tr>
    <tr>
      <th>26235</th>
      <td>Start_131</td>
      <td>я</td>
      <td>0.013387</td>
      <td>1.000000e-19</td>
      <td>1.792099e-04</td>
      <td>43.749117</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
