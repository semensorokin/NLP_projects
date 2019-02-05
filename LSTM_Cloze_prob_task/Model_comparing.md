
## Cloze task data filtering

drop all rows were we don't have a contex as a stimulus


```python
import pandas as pd
row_data = pd.read_excel('cloze_task_raw_data.xlsx')
print(row_data.shape)
row_data = row_data[row_data['shown'] != 'Введите первое слово']
print(row_data.shape)
```

    (64645, 16)
    (57836, 16)



```python
def clear(x):
    flag=0
    if x.isdigit():
        return 0
    if (len(x)==1) and (x not in 'ксявуоиа'):
        flag+=1
    for i in x:
        if i not in 'ячсмитьбюэждлорпавыфйцукенгшщзхъЯЧСМИТЬБЮФЫВАПРОЛДЖЭЪХЗЩЙЦШУГКНЕ':
             flag+=1
    if flag==0:
        return x
    else:
        return 0
row_data.answer = row_data.answer.astype(str)
row_data.answer = row_data.answer.apply(clear)
row_data = row_data[row_data['answer']!=0]
row_data.shape
```




    (57346, 16)



Count number of different answer for each stimulus and alse a index of confusion for rows.
If in experement we have 16 attempts to add the contex, when index of confusion is equel 16/max(all quantities of responses for each stimulus). Smaller the value of confuision, than we can be more confident about this example)


```python
sub_data = row_data[['shown', 'answer', 'word.id']]
grop_data = sub_data[['shown', 'answer']].groupby('shown').size()
grop_data = grop_data.reset_index(level=['shown'])
grop_data.columns = ['shown', 'summ']
grop_data['confusion'] = 1 - grop_data.summ/max(grop_data['summ'])
grop_data.head()
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
      <th>summ</th>
      <th>confusion</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>А</td>
      <td>15</td>
      <td>0.978571</td>
    </tr>
    <tr>
      <th>1</th>
      <td>А промывать</td>
      <td>15</td>
      <td>0.978571</td>
    </tr>
    <tr>
      <th>2</th>
      <td>А промывать манную</td>
      <td>15</td>
      <td>0.978571</td>
    </tr>
    <tr>
      <th>3</th>
      <td>А промывать манную крупу</td>
      <td>15</td>
      <td>0.978571</td>
    </tr>
    <tr>
      <th>4</th>
      <td>А промывать манную крупу перед</td>
      <td>15</td>
      <td>0.978571</td>
    </tr>
  </tbody>
</table>
</div>



Count the quantity of different response for each stimulus 


```python
grop_dats_0 = sub_data[['shown', 'answer']].groupby(['shown','answer']).size()
grop_dats_0 = grop_dats_0.reset_index(level=['shown', 'answer'])
grop_dats_0.columns = ['shown', 'answer', 'freq']
grop_dats_0.head()
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
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>А</td>
      <td>вот</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>А</td>
      <td>где</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>А</td>
      <td>ему</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>А</td>
      <td>зачем</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>А</td>
      <td>знаете</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



Merge tables


```python
data_res =  sub_data.merge(grop_data, left_on='shown', right_on='shown', how='outer')
data_res =  data_res.merge(grop_dats_0, left_on=['shown','answer'], right_on=['shown','answer'], how='outer')
data_res.head()
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
      <th>word.id</th>
      <th>summ</th>
      <th>confusion</th>
      <th>freq</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>А</td>
      <td>вот</td>
      <td>промывать</td>
      <td>15</td>
      <td>0.978571</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>А</td>
      <td>где</td>
      <td>промывать</td>
      <td>15</td>
      <td>0.978571</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>А</td>
      <td>ему</td>
      <td>промывать</td>
      <td>15</td>
      <td>0.978571</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>А</td>
      <td>зачем</td>
      <td>промывать</td>
      <td>15</td>
      <td>0.978571</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>А</td>
      <td>знаете</td>
      <td>промывать</td>
      <td>15</td>
      <td>0.978571</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



count the prob


```python
import numpy as np
data_res['prob'] = np.where(data_res['word.id']==data_res['answer'], data_res.freq/data_res.summ, 0)
data_res.head()
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
      <th>word.id</th>
      <th>summ</th>
      <th>confusion</th>
      <th>freq</th>
      <th>prob</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>А</td>
      <td>вот</td>
      <td>промывать</td>
      <td>15</td>
      <td>0.978571</td>
      <td>1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>А</td>
      <td>где</td>
      <td>промывать</td>
      <td>15</td>
      <td>0.978571</td>
      <td>1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>А</td>
      <td>ему</td>
      <td>промывать</td>
      <td>15</td>
      <td>0.978571</td>
      <td>1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>А</td>
      <td>зачем</td>
      <td>промывать</td>
      <td>15</td>
      <td>0.978571</td>
      <td>1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>А</td>
      <td>знаете</td>
      <td>промывать</td>
      <td>15</td>
      <td>0.978571</td>
      <td>1</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>



check: did I lost some examples or not, as we can see the 


```python
data_res = data_res.drop_duplicates()
j = data_res[['shown', 'prob']].groupby('shown').sum()
j = j.reset_index(level=['shown'])
k =  j.merge(data_res[['shown','word.id']], left_on=['shown'], right_on=['shown'], how='outer')
k = k.drop_duplicates()
s = k.groupby(['shown','word.id']).sum()
s = s.reset_index(level=['shown', 'word.id'])
result = data_res[['shown', 'word.id', 'prob', 'confusion']]
result = result.drop_duplicates()
print(result.shape, s.shape)
result['is_dub'] = result[['shown', 'word.id', 'confusion']].duplicated(keep=False)
g =  result.query('(is_dub == True & prob > 0)|(is_dub==False)')
g.head()
```

    (1853, 4) (1222, 3)





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
      <th>word.id</th>
      <th>prob</th>
      <th>confusion</th>
      <th>is_dub</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>А</td>
      <td>промывать</td>
      <td>0.000000</td>
      <td>0.978571</td>
      <td>False</td>
    </tr>
    <tr>
      <th>15</th>
      <td>А промывать</td>
      <td>манную</td>
      <td>0.000000</td>
      <td>0.978571</td>
      <td>False</td>
    </tr>
    <tr>
      <th>40</th>
      <td>А промывать манную</td>
      <td>крупу</td>
      <td>0.333333</td>
      <td>0.978571</td>
      <td>True</td>
    </tr>
    <tr>
      <th>45</th>
      <td>А промывать манную крупу</td>
      <td>перед</td>
      <td>0.000000</td>
      <td>0.978571</td>
      <td>False</td>
    </tr>
    <tr>
      <th>60</th>
      <td>А промывать манную крупу перед</td>
      <td>тем</td>
      <td>0.000000</td>
      <td>0.978571</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>




```python
sub_data[['shown','word.id']].drop_duplicates().shape
```




    (1222, 2)



The window above can show us how the mean of probabilities is distributed by the lenght of the previos context. I do think that distribution of cloze task is close to slow expanencial(but only up on some threshold, in our case it is ten-word-context). 


```python
import matplotlib.pyplot as plt 

plot_data = g[['shown', 'prob']]
def get_len(x):
    return len(x.split())

def plot_mean_prob_distribution(plot_data, y_lbl):
    plot_data['context_len'] = plot_data.shown.apply(get_len)
    x1 = plot_data.groupby('context_len').sum()
    x1 = x1.reset_index(level=['context_len'])
    x2 = plot_data.groupby('context_len').size()
    x2 = x2.reset_index(level=['context_len'])
    plotting = x1.merge(x2, left_on = 'context_len', right_on = 'context_len', how = 'outer')
    plotting.columns = ['context_len', 'prob', 'abs_freq']
    plotting['frequency'] = plotting['prob']/plotting['abs_freq']
    
    plt.subplot(221)
    plot1, =plt.plot(plotting.context_len.tolist(), plotting.frequency.tolist(), 'b--', label="$y=x^2$")
    plt.ylim(0,y_lbl)
    plt.grid()

    plt.subplot(222)
    plt.bar(x= plotting.context_len.tolist(), height = plotting.frequency.tolist())
    plt.ylim(0,y_lbl)

    _=plt.show()
    
plot_mean_prob_distribution(plot_data, 0.5)
```

    /home/semen/.local/lib/python3.6/site-packages/ipykernel_launcher.py:8: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      



![png](Model_comparing_files/Model_comparing_16_1.png)


Compute median and plot it. Why it is also necessary? Because the median values are more stable and less dependant on the "emmissions" of the model.


```python
import numpy as np

def tl(x):
    d = []
    d.append(x)
    return d

def mediann(x):
    return np.median(x)

def plot_median_distribution(plot_data, y_lbl):
    
    plot_data['context_len'] = plot_data.shown.apply(get_len)
    plot_data.prob = plot_data.prob.apply(tl)
    x1 = plot_data.groupby('context_len').sum()
    x1 = x1.reset_index(level=['context_len'])
    plotting = x1

    plotting['mediann'] = plotting['prob'].apply(mediann)
    
    data = np.array(plotting.prob)

    plt.subplot(221)
    plot1, =plt.plot(plotting.context_len.tolist(), plotting.mediann.tolist(), 'b--', label="$y=x^2$")
    plt.ylim(0,y_lbl)
    plt.grid()

    plt.subplot(222)
    plt.bar(x= plotting.context_len.tolist(), height = plotting.mediann.tolist())
    plt.ylim(0,y_lbl)
    
    plt.subplot(212)
    plt.boxplot(data)
    

    _=plt.show()

    
plot_median_distribution(plot_data, 0.5)
```

    /home/semen/.local/lib/python3.6/site-packages/ipykernel_launcher.py:13: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      del sys.path[0]
    /home/semen/.local/lib/python3.6/site-packages/pandas/core/generic.py:4405: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self[name] = value



![png](Model_comparing_files/Model_comparing_18_1.png)


## LSTM Data


```python
lstm = pd.read_excel('LSTM_prob_w_pos.xlsx')
```


```python
lstm[['shown','answer']].drop_duplicates().shape
```




    (1312, 2)




```python
sub_lstm = lstm[['shown','answer', 'prob', 'pos.tag']]
sub_lstm = sub_lstm[sub_lstm.shown != 'Введите первое слово']
sub_lstm.shape
```




    (1223, 4)




```python
plot_data_lstm = sub_lstm[['shown', 'prob']]
plot_mean_prob_distribution(plot_data_lstm, 0.5)
```

    /home/semen/.local/lib/python3.6/site-packages/ipykernel_launcher.py:8: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      



![png](Model_comparing_files/Model_comparing_23_1.png)



```python
plot_median_distribution(plot_data_lstm,0.5)
```

    /home/semen/.local/lib/python3.6/site-packages/ipykernel_launcher.py:13: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      del sys.path[0]



![png](Model_comparing_files/Model_comparing_24_1.png)



```python
ggg = g.merge(sub_lstm, left_on=['shown','word.id'], right_on=['shown','answer'], how='outer')
ress = ggg[['shown','word.id', 'prob_x', 'confusion', 'prob_y', 'pos.tag']]
ress.head()
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
      <th>word.id</th>
      <th>prob_x</th>
      <th>confusion</th>
      <th>prob_y</th>
      <th>pos.tag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>А</td>
      <td>промывать</td>
      <td>0.000000</td>
      <td>0.978571</td>
      <td>1.986770e-07</td>
      <td>INFN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>А промывать</td>
      <td>манную</td>
      <td>0.000000</td>
      <td>0.978571</td>
      <td>9.952960e-06</td>
      <td>ADJF</td>
    </tr>
    <tr>
      <th>2</th>
      <td>А промывать манную</td>
      <td>крупу</td>
      <td>0.333333</td>
      <td>0.978571</td>
      <td>9.152956e-02</td>
      <td>NOUN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>А промывать манную крупу</td>
      <td>перед</td>
      <td>0.000000</td>
      <td>0.978571</td>
      <td>7.796750e-04</td>
      <td>PREP</td>
    </tr>
    <tr>
      <th>4</th>
      <td>А промывать манную крупу перед</td>
      <td>тем</td>
      <td>0.000000</td>
      <td>0.978571</td>
      <td>1.503523e-02</td>
      <td>CONJ</td>
    </tr>
  </tbody>
</table>
</div>



## Comparing


```python
ress['diff'] = (ress.prob_x - ress.prob_y)**2
print(sum(ress['diff']))
```

    55.21226830615383


    /home/semen/.local/lib/python3.6/site-packages/ipykernel_launcher.py:1: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      """Entry point for launching an IPython kernel.



```python
import numpy as np
import matplotlib.pyplot as plt 
from scipy import stats

gradient, intercept, r_value, p_value, std_err = stats.linregress(ress.prob_x, ress.prob_y)
mn=np.min(ress.prob_x)
mx=np.max(ress.prob_y)
x1=np.linspace(mn,mx,500)
y1=gradient*x1+intercept
plt.plot(ress.prob_x,ress.prob_y,'ob')
plt.plot(x1,y1,'-r')
plt.show()
```


![png](Model_comparing_files/Model_comparing_28_0.png)



```python
from sklearn.metrics import mutual_info_score
MI = mutual_info_score(ress.prob_x, ress.prob_y)
MI
```




    3.6634010037120004



## Cloze task pos tagging with pymorthy


```python
data = row_data[['shown','answer','word.id']]
k = data[['shown','word.id']].drop_duplicates()
k.shape
```




    (1222, 2)




```python
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
def pos_t_cor_w(cor_w):
    ps = {}
    for indx, pos_variant in enumerate(morph.parse(cor_w)):
        if pos_variant.tag.POS not in ps:
            ps[pos_variant.tag.POS] = pos_variant.score
        else:
            ps[pos_variant.tag.POS] += pos_variant.score
            
    return list(ps.items())
```


```python
correct_word_tags = {}
for context, word in list(zip( k['shown'].tolist(), k['word.id'].tolist())):
    correct_word_tags[(context,word)] = pos_t_cor_w(word)
```


```python
def tolist_(x):
    return [x]
data.answer = data.answer.apply(tolist_)
```

    /home/semen/.local/lib/python3.6/site-packages/pandas/core/generic.py:4405: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self[name] = value



```python
nt = data[['shown', 'answer', 'word.id']].groupby(['shown', 'word.id']).sum()
nt = nt.reset_index()
nt.head()
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
      <th>word.id</th>
      <th>answer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>А</td>
      <td>промывать</td>
      <td>[вот, где, ему, зачем, знаете, зори, когда, кт...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>А промывать</td>
      <td>манную</td>
      <td>[глаза, горло, желудок, ли, макароны, мозги, м...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>А промывать манную</td>
      <td>крупу</td>
      <td>[кашу, кашу, кашу, кашу, кашу, кашу, кашу, каш...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>А промывать манную крупу</td>
      <td>перед</td>
      <td>[блин, лучше, лучше, не, не, не, не, не, не, н...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>А промывать манную крупу перед</td>
      <td>тем</td>
      <td>[варкой, варкой, варкой, варкой, варкой, варко...</td>
    </tr>
  </tbody>
</table>
</div>




```python
f = list(zip(nt['shown'].tolist(), nt['word.id'].tolist()))
answer_dict = {}
for indx,i in enumerate(f):
    answer_dict[i] = nt.answer.tolist()[indx] 
```


```python
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
def pos_t_ans(true_tag_distr, answers):
    normalize = len(answers)
    res = 0
    for answer in answers:
        ps = {}
        for indx, pos_variant in enumerate(morph.parse(answer)):
            if pos_variant.tag.POS not in ps:
                ps[pos_variant.tag.POS] = pos_variant.score
            else:
                ps[pos_variant.tag.POS] += pos_variant.score
     
        for tag, prob in true_tag_distr:
            if tag in ps:
                res += ps[tag]*prob
    res /=normalize     
        
    return res
```


```python
i = 0
res = []
for cont_word, answers in answer_dict.items():
    res.append(pos_t_ans(correct_word_tags[cont_word],answers))
print(len(res))
nt['prob'] = res
```

    1222



```python
plot_data = nt[['shown', 'prob']]
plot_mean_prob_distribution(plot_data,1)
```

    /home/semen/.local/lib/python3.6/site-packages/ipykernel_launcher.py:8: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      



![png](Model_comparing_files/Model_comparing_39_1.png)



```python
plot_median_distribution(plot_data,1)
```

    /home/semen/.local/lib/python3.6/site-packages/ipykernel_launcher.py:13: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      del sys.path[0]



![png](Model_comparing_files/Model_comparing_40_1.png)


## LSTM data pos tagging


```python
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
import re
def pos_t_ans(answers_prob):
    tags_prob = {'NOUN':0, 'ADJF':0, 'ADJS':0,'COMP':0,'VERB':0,'INFN':0,
'PRTF':0,'PRTS':0, 'GRND':0, 'NUMR':0, 'ADVB':0, 'NPRO':0, 'PRED':0,
'PREP':0, 'CONJ':0,'PRCL':0,'INTJ':0}
    tags_count = {'NOUN':0, 'ADJF':0, 'ADJS':0,'COMP':0,'VERB':0,'INFN':0,
'PRTF':0,'PRTS':0, 'GRND':0, 'NUMR':0, 'ADVB':0, 'NPRO':0, 'PRED':0,
'PREP':0, 'CONJ':0,'PRCL':0,'INTJ':0}
    for answer,prob in answers_prob:
        k = re.findall('[а-яА-Я]+',answer)
        if len(k)>0:
            answer = k[0]
            for indx, pos_variant in enumerate(morph.parse(answer)):
                if pos_variant.tag.POS!=None:
                    tags_prob[pos_variant.tag.POS] += (pos_variant.score)
                    #tags_prob[pos_variant.tag.POS] += (pos_variant.score*prob)
                    if pos_variant.score>0:
                        tags_count[pos_variant.tag.POS] += 1

    t_p = list(tags_prob.items())
    t_p.sort(key = lambda x:x[1])
    pos, prob = t_p[-1]
    if prob!=0:
        prob /=tags_count[pos]
    return pos, prob
```


```python
import json
json_data=open('data.json').read()
data = json.loads(json_data)
lstm_tag_max_prob = []
lstm_best_tag = []
for context in list(data.keys()):
    pos, prob = pos_t_ans(data.get(context))
    lstm_tag_max_prob.append((context,prob))
    lstm_best_tag.append((context,pos))
print(len(lstm_best_tag))
```

    1187



```python
Context = [i for i, j in lstm_tag_max_prob]
Probs_lstm_tag = [j for i, j in lstm_tag_max_prob]
lstm_best_tag = [j for i, j in lstm_best_tag]
lstm_tags_prob = pd.DataFrame({'shown' :Context, 'prob' : Probs_lstm_tag, 'tag':lstm_best_tag })
lstm_tags_prob.head()

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
      <th>prob</th>
      <th>tag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>на</td>
      <td>0.397501</td>
      <td>NOUN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>на болотах</td>
      <td>0.738495</td>
      <td>VERB</td>
    </tr>
    <tr>
      <th>2</th>
      <td>на болотах оставался</td>
      <td>0.243669</td>
      <td>ADJF</td>
    </tr>
    <tr>
      <th>3</th>
      <td>на болотах оставался ещё</td>
      <td>0.385341</td>
      <td>ADJF</td>
    </tr>
    <tr>
      <th>4</th>
      <td>на болотах оставался ещё лёд</td>
      <td>0.303169</td>
      <td>NOUN</td>
    </tr>
  </tbody>
</table>
</div>




```python
def prep(x):
    h = x.replace(' - ', '-')
    h = h.replace(' : " ', ' ')
    return h
plot_data = lstm_tags_prob[['shown', 'prob']]
plot_data.shown = plot_data.shown.apply(prep)
plot_mean_prob_distribution(plot_data, 1)
```


![png](Model_comparing_files/Model_comparing_45_0.png)



```python
plot_median_distribution(plot_data,1)
```


![png](Model_comparing_files/Model_comparing_46_0.png)


## Tag models comparing


```python
lstm_tags_prob['diff'] = (nt['prob'] - lstm_tags_prob.prob)**2
print(sum(lstm_tags_prob['diff']))
```

    234.3961547021695



```python
import numpy as np
import matplotlib.pyplot as plt 
from scipy import stats


gradient, intercept, r_value, p_value, std_err = stats.linregress(nt['prob'][:1187], lstm_tags_prob.prob)
mn=np.min(nt['prob'][:1187])
mx=np.max(lstm_tags_prob.prob)
x1=np.linspace(mn,mx,500)
y1=gradient*x1+intercept
plt.plot(nt['prob'][:1187],lstm_tags_prob.prob,'ob')
plt.plot(x1,y1,'-r')
plt.show()
```


![png](Model_comparing_files/Model_comparing_49_0.png)



```python
from sklearn.metrics import mutual_info_score
MI = mutual_info_score(lstm_tags_prob.prob, nt['prob'][:1187])
MI
```




    6.722463492206198



## Cloze task data semantic research


```python
h = open('Close_task_answers.vec.vec', 'r').readlines()
word2ind = {}
vecs = []
for ind, j in enumerate(h[1:]):
    word2ind[j.split(' ')[0]] = ind
    vecs.append(j.split(' ')[1:])
```


```python
import numpy as np
from sklearn.cluster import KMeans
km = KMeans(n_clusters=40, init='k-means++', n_init=10, max_iter=500).fit_predict(np.array(vecs))
```


```python
ind2word = {j:i for i,j in word2ind.items()}
```


```python
clusters = []
for word_cluster in range(40):
    new_cluster = []
    for ind, i in enumerate(km):
        if i == word_cluster:
            new_cluster.append(ind2word[ind])
    clusters.append(new_cluster)
print(sum(len(i) for i in clusters))
```

    9294



```python
for i in [j[:10] for j in clusters]:
    print (', '.join(i))
    print('###############################')

```

    был, стал, получил, родился, работал, сам, начал, назначен, умер, удалось
    ###############################
    другими, двумя, своими, всеми, которыми, такими, тремя, людьми, первыми, местами
    ###############################
    была, она, стала, получила, вышла, сама, появилась, началась, находилась, вошла
    ###############################
    список, несколько, которых, других, среди, всех, около, двух, наиболее, этих
    ###############################
    является, таким, одним, первым, этим, своим, другим, самым, всем, главным
    ###############################
    однажды, случайно, домой, увидел, видит, неожиданно, пытаясь, внезапно, спас, мимо
    ###############################
    в, и, на, с, по, года, из, а, к, году
    ###############################
    чтобы, сделать, использовать, найти, делать, писать, работать, оставить, стать, создать
    ###############################
    язык, населения, истории, жизни, церкви, образования, деятельности, культуры, книги, права
    ###############################
    болезни, крови, врач, лечения, больных, больницы, кровь, болезнь, больнице, детям
    ###############################
    жизнь, себе, друг, друга, любовь, образ, смерть, хочет, любви, ради
    ###############################
    воды, поверхности, температура, воду, энергии, газа, вода, волны, веществ, воде
    ###############################
    были, все, они, которые, другие, эти, две, некоторые, свои, такие
    ###############################
    оружие, золото, камень, изделий, детали, надписью, изделия, изготовления, камня, бумаги
    ###############################
    области, россии, ссср, марта, войны, сайт, участник, великой, москва, член
    ###############################
    вид, который, один, этот, первый, русский, большой, новый, свой, должен
    ###############################
    день, дня, мир, земле, часов, звезды, ночь, пер, земля, свет
    ###############################
    цвета, мужчины, очки, ткани, белое, кожи, волосы, одежду, одежда, костюм
    ###############################
    для, или, без, описание, карты, размер, имеет, индекс, работы, человека
    ###############################
    свою, эту, работу, которую, первую, одну, всю, историю, группу, большую
    ###############################
    пищи, стол, стола, еды, обычай, рыбу, печь, еду, спать, подарки
    ###############################
    летом, климат, зимой, лето, лета, ветра, градусов, весна, ветер, холодной
    ###############################
    о, об, городе, виде, языке, месте, мире, русском, матче, одном
    ###############################
    улица, дом, церковь, площади, музей, дома, корпус, доме, переулок, собор
    ###############################
    этой, которой, своей, которая, первой, одной, другой, такой, новой, основной
    ###############################
    район, района, города, село, реки, центра, город, находится, центр, сельского
    ###############################
    тела, руки, тело, глаза, сверху, голову, руках, угол, голова, глаз
    ###############################
    не, что, это, то, если, есть, статьи, может, можно, нет
    ###############################
    компании, компания, производства, строительства, долларов, производство, сети, завода, промышленности, средства
    ###############################
    животных, животные, птицы, кот, рыбы, насекомые, рыб, птица, яйца, жуков
    ###############################
    история, эта, одна, первая, большая, новая, книга, должна, страна, работа
    ###############################
    стали, могли, получили, начали, жители, вошли, работали, находились, приняли, прошли
    ###############################
    университета, наук, институт, образование, окончил, школы, университет, школа, университете, степень
    ###############################
    род, николай, сын, иван, герой, иванович, отец, детей, семье, андрей
    ###############################
    лука, продукты, масло, рис, соль, вина, масла, пищу, приготовления, кофе
    ###############################
    растений, растения, леса, листья, лес, дерево, лесной, деревьев, дерева, лесу
    ###############################
    я, вы, мне, да, кто, мы, меня, ну, вам, нас
    ###############################
    игры, песни, фильма, театра, роли, театр, кино, альбома, фильме, песня
    ###############################
    могут, являются, обычно, имеют, происходит, проходит, работает, находятся, встречается, называют
    ###############################
    мм, машины, конструкции, скорости, двигатель, орудия, устройства, машин, установки, автомобиль
    ###############################



```python

```
