import numpy as np
import pandas as pd


########## Exception ########## 
class VariableNotInitializedError(Exception):
    def __init__(self, variable_name, suggestion=None):
        self.variable_name = variable_name
        self.suggestion = suggestion

    def __str__(self):
        if self.suggestion:
            err = f"Variable '{self.variable_name}' is not initialized yet. {self.suggestion}"
        else:
            err = f"Variable '{self.variable_name}' is not initialized yet."
        return err


########## Data Preparation ##########
class Cat2Num:
    def __init__(self):
        """
        Initializes an instance of the Cat2Num class.
        """
        self.dict_map = {}
        
    def cat2num(self, df: pd.DataFrame):
        """
        Converts categorical columns in a DataFrame to numerical values using a mapping dictionary.
        
        Args:
            df (pd.DataFrame): The DataFrame containing categorical columns to be converted.
        
        Returns:
            pd.DataFrame: A new DataFrame with categorical columns replaced by numerical values.
        """
        df = df.copy()
        for col in df:
            
            if df[col].dtype == 'object' or df[col].dtype == 'category':
                if df[col].dtype == 'category':
                    df[col] = df[col].astype('object')
                    
                self.dict_map[col] = {}
                unique_values = df[col].unique()
                for repl, orig in enumerate(unique_values):
                    self.dict_map[col][orig] = repl
                    df[col].replace(orig, repl, inplace=True)
                    
        return df
    
    def num2cat(self, df: pd.DataFrame):
        """
        Converts numerical values in the DataFrame back to their original categorical values using the stored mapping dictionary.
        
        Args:
            df (pd.DataFrame): The DataFrame containing numerical values to be converted back to categorical values.
        
        Returns:
            pd.DataFrame: A new DataFrame with numerical values replaced by their original categorical values.
        
        Raises:
            VariableNotInitializedError: If the `dict_map` variable is empty, indicating that 'cat2num()' has not been executed.
        """
        df = df.copy()
        if self.dict_map == {}:
            raise VariableNotInitializedError("dict_map", suggestion="Try executing 'cat2num()' first.")
            
        for col in df:
            if col in self.dict_map.keys():
                for orig, repl in self.dict_map[col].items():
                    df[col].replace(repl, orig, inplace=True)
                    
        return df
    
def split_data(df, test_size=0.25, shuffle=True, random_state=143):
    """
    Splits the provided DataFrame into train and test sets.

    Args:
        df (pd.DataFrame): The DataFrame to be split.
        test_size (float, optional): The proportion of the DataFrame to be included in the test set. Defaults to 0.25.
        shuffle (bool, optional): Whether to shuffle the DataFrame before splitting. Defaults to True.
        random_state (int, optional): The random seed for shuffling the DataFrame. Defaults to 143.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the train and test DataFrames.

    """
    if shuffle:
        df = df.sample(frac=1, random_state=random_state)
    
    train = df[:-int(len(df) * test_size)]
    test = df[-int(len(df) * test_size):]
    return train, test


########## Performance Metrics ##########
def confusion_matrix(y_true, y_pred):
    """
    Computes the confusion matrix based on the true and predicted labels.

    Args:
        y_true (List[Any]): The true labels.
        y_pred (List[Any]): The predicted labels.

    Returns:
        List[List[int]]: The confusion matrix.

    """
    labels = list(set(y_true).union(set(y_pred)))
    labels.sort()

    matrix = [[0] * len(labels) for _ in range(len(labels))]

    for true, pred in zip(y_true, y_pred):
        matrix[labels.index(true)][labels.index(pred)] += 1

    return matrix

def clf_metrics(matrix, class_labels):
    """
    Computes various classification metrics based on the confusion matrix.

    Args:
        matrix (np.ndarray): The confusion matrix.
        class_labels (List[Any]): The list of class labels.

    Returns:
        pd.DataFrame: A DataFrame containing the classification metrics.

    """
    FP = np.sum(matrix, axis=0) - np.diag(matrix)
    FN = np.sum(matrix, axis=1) - np.diag(matrix)
    TP = np.diag(matrix)
    TN = np.sum(matrix) - (FP + FN + TP)
    FP = FP.astype(float)
    FN = FN.astype(float)
    TP = TP.astype(float)
    TN = TN.astype(float)

    TPR = np.round(TP / (TP + FN), 2)
    TNR = np.round(TN / (TN + FP), 2)
    PPV = np.round(TP / (TP + FP), 2)
    F1 = np.round(2 * (PPV * TPR) / (PPV + TPR), 2)

    dataframe = pd.DataFrame(data={'Recall': TPR,
                                   'Specificity': TNR,
                                   'Precision': PPV,
                                   'F1-Score': F1,
                                   'Accuracy': np.round(np.sum(TP) / np.sum(matrix), 2)},
                             index=class_labels)
    dataframe.fillna(value=0, inplace=True)
    return dataframe

def reg_metrics(y_true, y_pred):
    """
    Computes various regression metrics based on the true and predicted values.

    Args:
        y_true (np.ndarray): The true values.
        y_pred (np.ndarray): The predicted values.

    Returns:
        pd.DataFrame: A DataFrame containing the regression metrics.

    """
    mse = np.round(np.mean((y_true - y_pred) ** 2),2)
    rmse = np.round(np.sqrt(mse),2)
    mae = np.round(np.mean(np.abs(y_true - y_pred)),2)
    r2 = np.round(1 - (np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2)),2)

    dataframe = pd.DataFrame(data={'MSE': mse,
                                   'RMSE': rmse,
                                   'MAE': mae,
                                   'R-squared': r2},
                             index=['Metrics'])
    
    return dataframe


########## Model Training Class ##########
class TrainModel:
    def __init__(self, df: pd.DataFrame, target: str, features: list, models, test_size=0.25, random_state=143, shuffle=True):
        """
        Initializes the TrainModel class.

        Args:
            df (pd.DataFrame): The input DataFrame.
            target (str): The target variable column name.
            features (list): A list of feature column names.
            models (Union[BaseEstimator, List[BaseEstimator]]): A single or a list of machine learning models.
            test_size (float, optional): The proportion of the dataset to include in the test split. Defaults to 0.25.
            random_state (int, optional): Random state for reproducibility. Defaults to 143.
            shuffle (bool, optional): Whether to shuffle the dataset before splitting. Defaults to True.
        """
        self.__df = df.copy()
        self.__target = target
        self.__features = features
        self.__models = models if isinstance(models, list) else [models]  # Convert single model to a list
        self.__test_size = test_size
        self.__random_state = random_state
        self.__shuffle = shuffle
        
        self.__lbl_encoder = Cat2Num()
        self.__split_data = split_data
        self.__reg_metrics = reg_metrics
        self.__clf_metrics = clf_metrics
        self.__conf_matrix = confusion_matrix
        self.__type = 'regression' if np.issubdtype(self.__df[self.__target].dtype, np.floating) else 'classification'
        self.__train = None
        self.__test = None
        
        self.fitted_models_dict = {}
        self.results_df = None
        
    def fit(self, verbose=True):
        """
        Fits the machine learning models/model on the training data.

        Args:
            verbose (bool, optional): Whether to display verbose output during fitting. Defaults to True.
        """
        data = self.__lbl_encoder.cat2num(self.__df)
        train, test = self.__split_data(df=data, 
                                        test_size=self.__test_size, 
                                        shuffle=self.__shuffle, 
                                        random_state=self.__random_state)

        X_train, y_train = train[self.__features], train[self.__target]

        for model in self.__models:
            fitted_model = model.fit(X=X_train, y=y_train)
            self.fitted_models_dict[model.__class__.__name__] = fitted_model

            y_pred = fitted_model.predict(X_train)

            if self.__type == 'regression':
                if verbose:
                    report_df = self.__reg_metrics(y_train, y_pred)
                    display(report_df)
            else:
                if verbose:
                    matrix = self.__conf_matrix(y_train, y_pred)
                    report_df = self.__clf_metrics(matrix, self.__lbl_encoder.dict_map[self.__target].keys())
                    display(report_df)

        self.__train = train
        self.__test = test
            
    def evaluate(self, verbose=True):
        """
        Evaluates the fitted machine learning models on the test data.

        Args:
            verbose (bool, optional): Whether to display verbose output during evaluation. Defaults to True.
        """
        if self.fitted_models_dict is None or len(self.fitted_models_dict) == 0:
            raise VariableNotInitializedError("models", suggestion="Try fitting it first using `fit()` method.")

        X_test, y_test = self.__test[self.__features], self.__test[self.__target]
        
        results_list = []
        
        for fitted_model in self.fitted_models_dict.values():
            y_pred = fitted_model.predict(X_test)

            if self.__type == 'regression':
                metrics_df = self.__reg_metrics(y_test, y_pred)
                metrics_df.insert(0, 'Model',fitted_model.__class__.__name__)
                results_list.append(metrics_df)
                
                if verbose:
                    display(metrics_df.drop('Model', axis=1))
                    
            elif self.__type == 'classification':
                matrix = self.__conf_matrix(y_test, y_pred)
                report_df = self.__clf_metrics(matrix, self.__lbl_encoder.dict_map[self.__target].keys())
                    
                metrics_df = pd.DataFrame(data={'Model':[fitted_model.__class__.__name__],
                                                'Accuracy':[report_df['Accuracy'][0]]})
                results_list.append(metrics_df)
                
                if verbose:
                    display(report_df)
        
            res_df = pd.concat(results_list)
        self.results_df = res_df.sort_values(by=res_df.columns[1], ascending=True if self.__type == 'regression' else False).reset_index(drop=True)