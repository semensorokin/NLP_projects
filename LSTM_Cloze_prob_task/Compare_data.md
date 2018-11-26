

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
gg['prob'] = np.where(gg.accuracy_x==1., (gg.all_fr*gg.index_norm)/(gg.index_norm*gg.sum_fr), 0)
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
    (679, 4)
            shown  accuracy_x  sum_fr      prob
    2    Start_10         1.0      71  0.014085
    8   Start_104         1.0      16  0.125000
    15  Start_110         1.0     151  0.006623
    19  Start_113         1.0     112  0.026786
    21  Start_114         1.0      93  0.032258



```python
res[res.prob>=1.]
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
      <th>sum_fr</th>
      <th>prob</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>311</th>
      <td>В современном обществе семья и школа оказывают...</td>
      <td>1.0</td>
      <td>17</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>421</th>
      <td>Во избежание ожогов надо нанести на лицо небол...</td>
      <td>1.0</td>
      <td>15</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>424</th>
      <td>Во избежание ожогов надо нанести на лицо небол...</td>
      <td>1.0</td>
      <td>15</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>548</th>
      <td>Дрозды и скворцы начали вить семейные гнёзда н...</td>
      <td>1.0</td>
      <td>15</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>738</th>
      <td>Зачем ему звонить‚ если откликается спокойный ...</td>
      <td>1.0</td>
      <td>17</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>795</th>
      <td>Ирине досталась отдельная комната в двухкомнатной</td>
      <td>1.0</td>
      <td>16</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>815</th>
      <td>Какие главные лекарства должны входить</td>
      <td>1.0</td>
      <td>63</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1184</th>
      <td>Олень бродил среди берёз‚ жевал талый снег</td>
      <td>1.0</td>
      <td>15</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1525</th>
      <td>С нескрываемой едкой иронией отзываются они др...</td>
      <td>1.0</td>
      <td>15</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1552</th>
      <td>Собаку‚ виновницу случившегося‚ приказали сечь...</td>
      <td>1.0</td>
      <td>15</td>
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
data_m =  data.merge(res, left_on='shown', right_on='shown', how='outer')
```


```python
data_m.shown.unique().shape
```




    (1206,)




```python
data_m = data_m.dropna()
result = data_m[['shown', 'answer', 'prob_x', 'prob_y']]
```


```python
check = data_cloze[data_cloze.accuracy==1.][['shown', 'answer']]
check = check.drop_duplicates()
data_result =  result.merge(check, left_on='shown', right_on='shown', how='outer')
```


```python
data_result = data_result[data_result.answer_x == data_result.answer_y]
data_result = data_result[['shown','answer_x','prob_x','prob_y']]
```


```python
data_result.columns = ['shown', 'answer', 'prob_by_model', 'prob_by_human']
data_result['R^2'] = (data_result.prob_by_human-data_result.prob_by_model)**2
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
data_result
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
      <th>R^2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>На болотах оставался</td>
      <td>еще</td>
      <td>0.124899</td>
      <td>0.029412</td>
      <td>9.117721e-03</td>
    </tr>
    <tr>
      <th>1</th>
      <td>На болотах оставался ещё лёд‚</td>
      <td>но</td>
      <td>0.039917</td>
      <td>0.362963</td>
      <td>1.043589e-01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>На болотах оставался ещё лёд‚ но</td>
      <td>на</td>
      <td>0.031502</td>
      <td>0.043796</td>
      <td>1.511303e-04</td>
    </tr>
    <tr>
      <th>3</th>
      <td>На болотах оставался ещё лёд‚ но на</td>
      <td>берегах</td>
      <td>0.003701</td>
      <td>0.007299</td>
      <td>1.294580e-05</td>
    </tr>
    <tr>
      <th>4</th>
      <td>На болотах оставался ещё лёд‚ но на берегах</td>
      <td>реки</td>
      <td>0.014212</td>
      <td>0.080882</td>
      <td>4.444963e-03</td>
    </tr>
    <tr>
      <th>5</th>
      <td>На болотах оставался ещё лёд‚ но на берегах ре...</td>
      <td>трава</td>
      <td>0.003874</td>
      <td>0.192593</td>
      <td>3.561461e-02</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Он</td>
      <td>был</td>
      <td>0.048258</td>
      <td>0.006711</td>
      <td>1.726100e-03</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Он ловко поддел концом</td>
      <td>ножа</td>
      <td>0.045508</td>
      <td>0.102941</td>
      <td>3.298552e-03</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Он ловко поддел концом ножа замочки‚</td>
      <td>и</td>
      <td>0.051944</td>
      <td>0.355556</td>
      <td>9.217985e-02</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Он ловко поддел концом ножа замочки‚ и</td>
      <td>они</td>
      <td>0.072151</td>
      <td>0.187970</td>
      <td>1.341391e-02</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Он ловко поддел концом ножа замочки‚ и они</td>
      <td>отскочили</td>
      <td>0.002742</td>
      <td>0.014706</td>
      <td>1.431301e-04</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Ваня раскрыл было</td>
      <td>рот</td>
      <td>0.467625</td>
      <td>0.225225</td>
      <td>5.875769e-02</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Ваня раскрыл было рот‚</td>
      <td>но</td>
      <td>0.661029</td>
      <td>0.790909</td>
      <td>1.686880e-02</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Ваня раскрыл было рот‚ но</td>
      <td>понял</td>
      <td>0.004546</td>
      <td>0.018349</td>
      <td>1.905118e-04</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Ваня раскрыл было рот‚ но понял‚</td>
      <td>что</td>
      <td>0.958914</td>
      <td>0.962963</td>
      <td>1.639039e-05</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Ваня раскрыл было рот‚ но понял‚ что что-то</td>
      <td>не</td>
      <td>0.241922</td>
      <td>0.523364</td>
      <td>7.921003e-02</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Ваня раскрыл было рот‚ но понял‚ что что-то не</td>
      <td>так</td>
      <td>0.575578</td>
      <td>0.761468</td>
      <td>3.455488e-02</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Ваня раскрыл было рот‚ но понял‚ что что-то не...</td>
      <td>и</td>
      <td>0.452314</td>
      <td>0.528302</td>
      <td>5.774183e-03</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Ваня раскрыл было рот‚ но понял‚ что что-то не...</td>
      <td>промолчал</td>
      <td>0.000886</td>
      <td>0.125000</td>
      <td>1.540423e-02</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Сделав мне</td>
      <td>знак</td>
      <td>0.002992</td>
      <td>0.010309</td>
      <td>5.354131e-05</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Сделав мне знак помолчать‚</td>
      <td>он</td>
      <td>0.164170</td>
      <td>0.729167</td>
      <td>3.192215e-01</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Сделав мне знак помолчать‚ он</td>
      <td>приложил</td>
      <td>0.000852</td>
      <td>0.010417</td>
      <td>9.148500e-05</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Сделав мне знак помолчать‚ он приложил</td>
      <td>ухо</td>
      <td>0.115581</td>
      <td>0.085106</td>
      <td>9.287244e-04</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Сделав мне знак помолчать‚ он приложил ухо</td>
      <td>к</td>
      <td>0.826187</td>
      <td>0.905263</td>
      <td>6.253093e-03</td>
    </tr>
    <tr>
      <th>29</th>
      <td>Сделав мне знак помолчать‚ он приложил ухо к</td>
      <td>двери</td>
      <td>0.015418</td>
      <td>0.484211</td>
      <td>2.197665e-01</td>
    </tr>
    <tr>
      <th>34</th>
      <td>Я</td>
      <td>люблю</td>
      <td>0.003210</td>
      <td>0.008734</td>
      <td>3.051129e-05</td>
    </tr>
    <tr>
      <th>35</th>
      <td>Я сделала</td>
      <td>шаг</td>
      <td>0.023332</td>
      <td>0.056818</td>
      <td>1.121335e-03</td>
    </tr>
    <tr>
      <th>36</th>
      <td>Я сделала шаг</td>
      <td>навстречу</td>
      <td>0.042140</td>
      <td>0.177778</td>
      <td>1.839768e-02</td>
    </tr>
    <tr>
      <th>37</th>
      <td>Я сделала шаг навстречу: приехала</td>
      <td>к</td>
      <td>0.092345</td>
      <td>0.303371</td>
      <td>4.453180e-02</td>
    </tr>
    <tr>
      <th>38</th>
      <td>Я сделала шаг навстречу: приехала к ней‚</td>
      <td>попросив</td>
      <td>0.000050</td>
      <td>0.011364</td>
      <td>1.279971e-04</td>
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
      <th>733</th>
      <td>Считается‚ что коллекционирование раритетных м...</td>
      <td>шоу-бизнеса</td>
      <td>0.089278</td>
      <td>0.066667</td>
      <td>5.112773e-04</td>
    </tr>
    <tr>
      <th>734</th>
      <td>Торговля продуктами</td>
      <td>питания</td>
      <td>0.163265</td>
      <td>0.230769</td>
      <td>4.556833e-03</td>
    </tr>
    <tr>
      <th>735</th>
      <td>Торговля продуктами питания</td>
      <td>является</td>
      <td>0.004347</td>
      <td>0.083333</td>
      <td>6.238855e-03</td>
    </tr>
    <tr>
      <th>736</th>
      <td>Торговля продуктами питания является</td>
      <td>одной</td>
      <td>0.077346</td>
      <td>0.076923</td>
      <td>1.787859e-07</td>
    </tr>
    <tr>
      <th>737</th>
      <td>Торговля продуктами питания является одной</td>
      <td>из</td>
      <td>0.995638</td>
      <td>0.933333</td>
      <td>3.881836e-03</td>
    </tr>
    <tr>
      <th>738</th>
      <td>Торговля продуктами питания является одной из</td>
      <td>самых</td>
      <td>0.292348</td>
      <td>0.285714</td>
      <td>4.400613e-05</td>
    </tr>
    <tr>
      <th>739</th>
      <td>Торговля продуктами питания является одной из ...</td>
      <td>прибыльных</td>
      <td>0.017299</td>
      <td>0.285714</td>
      <td>7.204701e-02</td>
    </tr>
    <tr>
      <th>740</th>
      <td>Торговля продуктами питания является одной из ...</td>
      <td>отраслей</td>
      <td>0.305058</td>
      <td>0.333333</td>
      <td>7.994775e-04</td>
    </tr>
    <tr>
      <th>741</th>
      <td>Торговля продуктами питания является одной из ...</td>
      <td>в</td>
      <td>0.100149</td>
      <td>0.076923</td>
      <td>5.394517e-04</td>
    </tr>
    <tr>
      <th>743</th>
      <td>Клиенты воровали</td>
      <td>из</td>
      <td>0.028697</td>
      <td>0.083333</td>
      <td>2.985102e-03</td>
    </tr>
    <tr>
      <th>744</th>
      <td>Один футболист‚ который получил растяжение‚</td>
      <td>не</td>
      <td>0.035322</td>
      <td>0.333333</td>
      <td>8.881070e-02</td>
    </tr>
    <tr>
      <th>745</th>
      <td>Один футболист‚ который получил растяжение‚ не...</td>
      <td>в</td>
      <td>0.095617</td>
      <td>0.928571</td>
      <td>6.938137e-01</td>
    </tr>
    <tr>
      <th>746</th>
      <td>Один футболист‚ который получил растяжение‚ не...</td>
      <td>игре</td>
      <td>0.015405</td>
      <td>0.357143</td>
      <td>1.167845e-01</td>
    </tr>
    <tr>
      <th>747</th>
      <td>Наши власти позволяют</td>
      <td>себе</td>
      <td>0.215054</td>
      <td>0.307692</td>
      <td>8.581789e-03</td>
    </tr>
    <tr>
      <th>748</th>
      <td>Наши власти позволяют себе излишества‚ создава...</td>
      <td>общества</td>
      <td>0.001888</td>
      <td>0.230769</td>
      <td>5.238640e-02</td>
    </tr>
    <tr>
      <th>749</th>
      <td>Ненужный коврик из твёрдой</td>
      <td>пластмассы</td>
      <td>0.010510</td>
      <td>0.083333</td>
      <td>5.303263e-03</td>
    </tr>
    <tr>
      <th>750</th>
      <td>Ненужный коврик из твёрдой пластмассы пригодит...</td>
      <td>подставка</td>
      <td>0.000019</td>
      <td>0.333333</td>
      <td>1.110982e-01</td>
    </tr>
    <tr>
      <th>751</th>
      <td>Ненужный коврик из твёрдой пластмассы пригодит...</td>
      <td>для</td>
      <td>0.512068</td>
      <td>0.571429</td>
      <td>3.523681e-03</td>
    </tr>
    <tr>
      <th>752</th>
      <td>Ненужный коврик из твёрдой пластмассы пригодит...</td>
      <td>посуды</td>
      <td>0.008749</td>
      <td>0.083333</td>
      <td>5.562781e-03</td>
    </tr>
    <tr>
      <th>753</th>
      <td>Когда родители пригрозили не взять её</td>
      <td>с</td>
      <td>0.098012</td>
      <td>0.538462</td>
      <td>1.939961e-01</td>
    </tr>
    <tr>
      <th>754</th>
      <td>Когда родители пригрозили не взять её с</td>
      <td>собой</td>
      <td>0.859795</td>
      <td>0.846154</td>
      <td>1.860755e-04</td>
    </tr>
    <tr>
      <th>755</th>
      <td>Когда родители пригрозили не взять её с собой‚</td>
      <td>маша</td>
      <td>0.000831</td>
      <td>0.083333</td>
      <td>6.806588e-03</td>
    </tr>
    <tr>
      <th>756</th>
      <td>Когда родители пригрозили не взять её с собой‚...</td>
      <td>расстроилась</td>
      <td>0.051342</td>
      <td>0.461538</td>
      <td>1.682608e-01</td>
    </tr>
    <tr>
      <th>757</th>
      <td>От внимания</td>
      <td>наблюдателя</td>
      <td>0.000024</td>
      <td>0.019608</td>
      <td>3.835426e-04</td>
    </tr>
    <tr>
      <th>758</th>
      <td>От внимания наблюдателя</td>
      <td>не</td>
      <td>0.042131</td>
      <td>0.058824</td>
      <td>2.786424e-04</td>
    </tr>
    <tr>
      <th>759</th>
      <td>От внимания наблюдателя не</td>
      <td>должна</td>
      <td>0.000957</td>
      <td>0.020000</td>
      <td>3.626235e-04</td>
    </tr>
    <tr>
      <th>760</th>
      <td>От внимания наблюдателя не должна</td>
      <td>ускользать</td>
      <td>0.000054</td>
      <td>0.040000</td>
      <td>1.595655e-03</td>
    </tr>
    <tr>
      <th>761</th>
      <td>От внимания наблюдателя не должна ускользать</td>
      <td>даже</td>
      <td>0.009129</td>
      <td>0.039216</td>
      <td>9.052350e-04</td>
    </tr>
    <tr>
      <th>762</th>
      <td>От внимания наблюдателя не должна ускользать даже</td>
      <td>малейшая</td>
      <td>0.005202</td>
      <td>0.215686</td>
      <td>4.430383e-02</td>
    </tr>
    <tr>
      <th>763</th>
      <td>От внимания наблюдателя не должна ускользать д...</td>
      <td>деталь</td>
      <td>0.148185</td>
      <td>0.711538</td>
      <td>3.173669e-01</td>
    </tr>
  </tbody>
</table>
<p>660 rows × 5 columns</p>
</div>




```python
measure = data_result[data_result.prob_by_model<data_result.prob_by_human].shape[0]/data_result.shape[0]
print("{}% of data, where prob of cloze task is greater than prob of lstm ".format(round(measure,2)))
```

    0.84% of data, where prob of cloze task is greater than prob of lstm 



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
      <th>R^2</th>
      <th>Cross_entropy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>На болотах оставался</td>
      <td>еще</td>
      <td>0.124899</td>
      <td>0.029412</td>
      <td>0.009118</td>
      <td>3.526361</td>
    </tr>
    <tr>
      <th>1</th>
      <td>На болотах оставался ещё лёд‚</td>
      <td>но</td>
      <td>0.039917</td>
      <td>0.362963</td>
      <td>0.104359</td>
      <td>1.013454</td>
    </tr>
    <tr>
      <th>2</th>
      <td>На болотах оставался ещё лёд‚ но</td>
      <td>на</td>
      <td>0.031502</td>
      <td>0.043796</td>
      <td>0.000151</td>
      <td>3.128221</td>
    </tr>
    <tr>
      <th>3</th>
      <td>На болотах оставался ещё лёд‚ но на</td>
      <td>берегах</td>
      <td>0.003701</td>
      <td>0.007299</td>
      <td>0.000013</td>
      <td>4.919981</td>
    </tr>
    <tr>
      <th>4</th>
      <td>На болотах оставался ещё лёд‚ но на берегах</td>
      <td>реки</td>
      <td>0.014212</td>
      <td>0.080882</td>
      <td>0.004445</td>
      <td>2.514760</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
