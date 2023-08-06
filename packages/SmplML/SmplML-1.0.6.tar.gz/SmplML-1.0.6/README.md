# SmplML / SimpleML: Simplified Machine Learning for Classification and Regression

SmplML is a user-friendly Python module for streamlined machine learning classification and regression. It offers intuitive functionality for data preprocessing, model training, and evaluation. Ideal for beginners and experts alike, SmplML simplifies ML tasks, enabling you to gain valuable insights from your data with ease.

## Features

- Data preprocessing: Easily handle encoding categorical variables and data partitioning.
- Model training: Train various classification and regression models with just a few lines of code.
- Model evaluation: Evaluate model performance using common metrics.
- This module is designed to seamlessly handle various scikit-learn models, making it flexible for handling sklearn-like model formats.
- Added training feature for training multiple models for experimentation.

## Installation

<strong>You can install SmpML using pip:</strong>
```shell
pip install SimpleML
```

## Usage
The `TrainModel` class is designed to handle both classification and regression tasks. It determines the task type based on the `target` parameter. If the `target` has a `float` data type, the class automatically redirects the procedures to regression; otherwise, it assumes a classification task. 

### Data Preparation
Data  preparation like data spliting and converting categorical data into numerical data is also automatically executed when calling the `fit()` method.


```python
import seaborn as sns
import pandas as pd
from smpl_ml.smpl_ml import TrainModel
```

### Classification Task


```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
```


```python
df = sns.load_dataset('penguins')
df.head()
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
      <th>species</th>
      <th>island</th>
      <th>bill_length_mm</th>
      <th>bill_depth_mm</th>
      <th>flipper_length_mm</th>
      <th>body_mass_g</th>
      <th>sex</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Adelie</td>
      <td>Torgersen</td>
      <td>39.1</td>
      <td>18.7</td>
      <td>181.0</td>
      <td>3750.0</td>
      <td>Male</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Adelie</td>
      <td>Torgersen</td>
      <td>39.5</td>
      <td>17.4</td>
      <td>186.0</td>
      <td>3800.0</td>
      <td>Female</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Adelie</td>
      <td>Torgersen</td>
      <td>40.3</td>
      <td>18.0</td>
      <td>195.0</td>
      <td>3250.0</td>
      <td>Female</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Adelie</td>
      <td>Torgersen</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Adelie</td>
      <td>Torgersen</td>
      <td>36.7</td>
      <td>19.3</td>
      <td>193.0</td>
      <td>3450.0</td>
      <td>Female</td>
    </tr>
  </tbody>
</table>
</div>




```python
clf_target = 'sex'
clf_features = df.iloc[:, df.columns != clf_target].columns

print(f"Class: {clf_target}")
print(f"Features: {clf_features}")
```

    Class: sex
    Features: Index(['species', 'island', 'bill_length_mm', 'bill_depth_mm',
           'flipper_length_mm', 'body_mass_g'],
          dtype='object')
    

#### Single Classification Model Training


```python
# Initialize TrainModel object
clf_trainer = TrainModel(df.dropna(), target=clf_target, features=clf_features, models=LogisticRegression(C=0.01, max_iter=10_000))

# Fit the object
clf_trainer.fit()
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
      <th>Recall</th>
      <th>Specificity</th>
      <th>Precision</th>
      <th>F1-Score</th>
      <th>Accuracy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>0.85</td>
      <td>0.82</td>
      <td>0.83</td>
      <td>0.84</td>
      <td>0.84</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>0.82</td>
      <td>0.85</td>
      <td>0.84</td>
      <td>0.83</td>
      <td>0.84</td>
    </tr>
  </tbody>
</table>
</div>


The displayed dataframe when calling the `fit()` method contains the training results, this output can be suppressed by setting `verbose=False`.


```python
# Evaluate the model
clf_trainer.evaluate()
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
      <th>Recall</th>
      <th>Specificity</th>
      <th>Precision</th>
      <th>F1-Score</th>
      <th>Accuracy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>0.73</td>
      <td>0.86</td>
      <td>0.83</td>
      <td>0.78</td>
      <td>0.8</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>0.86</td>
      <td>0.73</td>
      <td>0.77</td>
      <td>0.81</td>
      <td>0.8</td>
    </tr>
  </tbody>
</table>
</div>


The displayed dataframe when calling the `evaluate()` method contains the testing results, this output can be suppressed by setting `verbose=False`.


```python
# Access the fitted model
clf_trainer.fitted_models_dict
```




    {'LogisticRegression': LogisticRegression(C=0.01, max_iter=10000)}



#### Multiple Classification Model Training


```python
# Initialize TrainModel object
clfs = [LogisticRegression(), DecisionTreeClassifier(), RandomForestClassifier(), SVC(), KNeighborsClassifier()]

clf_trainer = TrainModel(df.dropna(), target=clf_target, features=clf_features, models=clfs, test_size=0.4)

# Fit the object
clf_trainer.fit(verbose=False)
```


```python
# Evaluate the model
clf_trainer.evaluate(verbose=True)
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
      <th>Recall</th>
      <th>Specificity</th>
      <th>Precision</th>
      <th>F1-Score</th>
      <th>Accuracy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>0.76</td>
      <td>0.81</td>
      <td>0.82</td>
      <td>0.79</td>
      <td>0.78</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>0.81</td>
      <td>0.76</td>
      <td>0.75</td>
      <td>0.78</td>
      <td>0.78</td>
    </tr>
  </tbody>
</table>
</div>



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
      <th>Recall</th>
      <th>Specificity</th>
      <th>Precision</th>
      <th>F1-Score</th>
      <th>Accuracy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>0.86</td>
      <td>0.83</td>
      <td>0.85</td>
      <td>0.85</td>
      <td>0.84</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>0.83</td>
      <td>0.86</td>
      <td>0.84</td>
      <td>0.83</td>
      <td>0.84</td>
    </tr>
  </tbody>
</table>
</div>



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
      <th>Recall</th>
      <th>Specificity</th>
      <th>Precision</th>
      <th>F1-Score</th>
      <th>Accuracy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>0.84</td>
      <td>0.86</td>
      <td>0.87</td>
      <td>0.85</td>
      <td>0.85</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>0.86</td>
      <td>0.84</td>
      <td>0.83</td>
      <td>0.84</td>
      <td>0.85</td>
    </tr>
  </tbody>
</table>
</div>



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
      <th>Recall</th>
      <th>Specificity</th>
      <th>Precision</th>
      <th>F1-Score</th>
      <th>Accuracy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>0.49</td>
      <td>0.73</td>
      <td>0.67</td>
      <td>0.57</td>
      <td>0.6</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>0.73</td>
      <td>0.49</td>
      <td>0.56</td>
      <td>0.63</td>
      <td>0.6</td>
    </tr>
  </tbody>
</table>
</div>



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
      <th>Recall</th>
      <th>Specificity</th>
      <th>Precision</th>
      <th>F1-Score</th>
      <th>Accuracy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Male</th>
      <td>0.74</td>
      <td>0.78</td>
      <td>0.79</td>
      <td>0.76</td>
      <td>0.76</td>
    </tr>
    <tr>
      <th>Female</th>
      <td>0.78</td>
      <td>0.74</td>
      <td>0.73</td>
      <td>0.75</td>
      <td>0.76</td>
    </tr>
  </tbody>
</table>
</div>


#### Results


```python
clf_trainer.results_df
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
      <th>Model</th>
      <th>Accuracy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>RandomForestClassifier</td>
      <td>0.85</td>
    </tr>
    <tr>
      <th>1</th>
      <td>DecisionTreeClassifier</td>
      <td>0.84</td>
    </tr>
    <tr>
      <th>2</th>
      <td>LogisticRegression</td>
      <td>0.78</td>
    </tr>
    <tr>
      <th>3</th>
      <td>KNeighborsClassifier</td>
      <td>0.76</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SVC</td>
      <td>0.60</td>
    </tr>
  </tbody>
</table>
</div>




```python
clf_trainer.fitted_models_dict
```




    {'LogisticRegression': LogisticRegression(),
     'DecisionTreeClassifier': DecisionTreeClassifier(),
     'RandomForestClassifier': RandomForestClassifier(),
     'SVC': SVC(),
     'KNeighborsClassifier': KNeighborsClassifier()}



Accuracy results and the fitted models can be accessed through the `results_df` and `fitted_models_dict` attributes.

### Regression Task


```python
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
```


```python
df = sns.load_dataset('penguins')
df.head()
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
      <th>species</th>
      <th>island</th>
      <th>bill_length_mm</th>
      <th>bill_depth_mm</th>
      <th>flipper_length_mm</th>
      <th>body_mass_g</th>
      <th>sex</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Adelie</td>
      <td>Torgersen</td>
      <td>39.1</td>
      <td>18.7</td>
      <td>181.0</td>
      <td>3750.0</td>
      <td>Male</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Adelie</td>
      <td>Torgersen</td>
      <td>39.5</td>
      <td>17.4</td>
      <td>186.0</td>
      <td>3800.0</td>
      <td>Female</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Adelie</td>
      <td>Torgersen</td>
      <td>40.3</td>
      <td>18.0</td>
      <td>195.0</td>
      <td>3250.0</td>
      <td>Female</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Adelie</td>
      <td>Torgersen</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Adelie</td>
      <td>Torgersen</td>
      <td>36.7</td>
      <td>19.3</td>
      <td>193.0</td>
      <td>3450.0</td>
      <td>Female</td>
    </tr>
  </tbody>
</table>
</div>




```python
reg_target = 'bill_length_mm'
reg_features = df.iloc[:, df.columns != reg_target].columns

print(f"Class: {reg_target}")
print(f"Features: {reg_features}")
```

    Class: bill_length_mm
    Features: Index(['species', 'island', 'bill_depth_mm', 'flipper_length_mm',
           'body_mass_g', 'sex'],
          dtype='object')
    

#### Single Regression Model Training


```python
# Initialize TrainModel object
reg_trainer = TrainModel(df.dropna(), 
                         target=reg_target, 
                         features=reg_features,
                         models=LinearRegression())

# Fit the object
reg_trainer.fit(verbose=False)
```


```python
# Evaluate the model
reg_trainer.evaluate()
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
      <th>MSE</th>
      <th>RMSE</th>
      <th>MAE</th>
      <th>R-squared</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Metrics</th>
      <td>6.3</td>
      <td>2.51</td>
      <td>1.91</td>
      <td>0.81</td>
    </tr>
  </tbody>
</table>
</div>



```python
# Access the model
reg_trainer.fitted_models_dict
```




    {'LinearRegression': LinearRegression()}



#### Multiple Regression Model Training


```python
# Initialize TrainModel object
regs = [LinearRegression(), DecisionTreeRegressor(), RandomForestRegressor(), SVR(), GradientBoostingRegressor()]

reg_trainer = TrainModel(df.dropna(), target=reg_target, features=reg_features, models=regs, test_size=0.4)

# Fit the object
reg_trainer.fit(verbose=False)
```


```python
# Evaluate the model
reg_trainer.evaluate(verbose=False)
```

#### Results


```python
reg_trainer.results_df
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
      <th>Model</th>
      <th>MSE</th>
      <th>RMSE</th>
      <th>MAE</th>
      <th>R-squared</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>RandomForestRegressor</td>
      <td>5.74</td>
      <td>2.40</td>
      <td>1.87</td>
      <td>0.81</td>
    </tr>
    <tr>
      <th>1</th>
      <td>GradientBoostingRegressor</td>
      <td>6.58</td>
      <td>2.57</td>
      <td>1.94</td>
      <td>0.79</td>
    </tr>
    <tr>
      <th>2</th>
      <td>DecisionTreeRegressor</td>
      <td>6.98</td>
      <td>2.64</td>
      <td>2.06</td>
      <td>0.77</td>
    </tr>
    <tr>
      <th>3</th>
      <td>LinearRegression</td>
      <td>7.63</td>
      <td>2.76</td>
      <td>2.11</td>
      <td>0.75</td>
    </tr>
    <tr>
      <th>4</th>
      <td>SVR</td>
      <td>21.51</td>
      <td>4.64</td>
      <td>3.63</td>
      <td>0.31</td>
    </tr>
  </tbody>
</table>
</div>




```python
reg_trainer.fitted_models_dict
```




    {'LinearRegression': LinearRegression(),
     'DecisionTreeRegressor': DecisionTreeRegressor(),
     'RandomForestRegressor': RandomForestRegressor(),
     'SVR': SVR(),
     'GradientBoostingRegressor': GradientBoostingRegressor()}




```python

```
