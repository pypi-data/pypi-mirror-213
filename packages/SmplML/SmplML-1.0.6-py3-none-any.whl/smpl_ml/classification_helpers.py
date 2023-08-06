import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix

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
    
class Cat2Num:
    """
    Cat2Num: Categorical to Numerical
    """

    def __init__(self):
        self.dict_map = {}

    def cat2num(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert categorical columns in the DataFrame to numerical representation.

        Args:
            df (pd.DataFrame): The input DataFrame with categorical columns.

        Returns:
            pd.DataFrame: The DataFrame with categorical columns converted to numerical representation.
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

    def num2cat(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert numerical representation of categorical columns back to their original values.

        Args:
            df (pd.DataFrame): The input DataFrame with numerical representation of categorical columns.

        Returns:
            pd.DataFrame: The DataFrame with numerical representation converted back to original categorical values.
        
        Raises:
            VariableNotInitializedError: If `cat2num()` has not been executed before calling `num2cat()`.
        """
        df = df.copy()
        if self.dict_map == {}:
            raise VariableNotInitializedError("dict_map", suggestion="Try executing 'cat2num()' first.")

        for col in df:
            if col in self.dict_map.keys():
                for orig, repl in self.dict_map[col].items():
                    df[col].replace(repl, orig, inplace=True)

        return df
    
def split_data(df: pd.DataFrame, test_size: float = 0.25, shuffle: bool = True, random_state: int = 143) -> tuple:
    """
    Split the DataFrame into training and testing datasets.

    Args:
        df (pd.DataFrame): The input DataFrame to be split.
        test_size (float, optional): The proportion of the DataFrame to be used for testing. Defaults to 0.25.
        shuffle (bool, optional): Whether to shuffle the DataFrame before splitting. Defaults to True.
        random_state (int, optional): The random seed for shuffling the DataFrame. Defaults to 143.

    Returns:
        tuple: A tuple containing the training and testing datasets.

    """
    if shuffle:
        df = df.sample(frac=1, random_state=random_state)

    train = df[:-int(len(df) * test_size)]
    test = df[-int(len(df) * test_size):]
    return train, test


def metrics(matrix: np.ndarray, class_labels: list) -> pd.DataFrame:
    """
    Calculate performance metrics based on the confusion matrix.

    Args:
        matrix (np.ndarray): The confusion matrix.
        class_labels (list): The list of class labels.

    Returns:
        pd.DataFrame: A DataFrame containing performance metrics for each class.

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
                                   'F1-Score': F1},
                             index=class_labels)
    dataframe.fillna(value=0, inplace=True)
    dataframe['Accuracy'] = np.round(np.sum(TP) / np.sum(matrix), 2)
    return dataframe

class TrainClassifier:
    def __init__(self, df, target, features, model, test_size=0.25, random_state=143, shuffle=True):

        """
        Initialize the TrainClassifier object.

        Args:
            df (pd.DataFrame): The input DataFrame containing the data.
            target (str): The name of the target variable column.
            features (list): The list of feature columns.
            model: The machine learning model to be trained.
            test_size (float, optional): The proportion of the data to be used for testing. Defaults to 0.25.
            random_state (int, optional): The random seed for data shuffling. Defaults to 143.
            shuffle (bool, optional): Whether to shuffle the data before splitting. Defaults to True.
        """
        self.__df = df.copy()
        self.__target = target
        self.__features = features
        self.__model = model
        self.__test_size = test_size
        self.__random_state = random_state
        self.__shuffle = shuffle
        
        self.__train = None
        self.__test = None
        self.__split_data = split_data
        self.__lbl_encoder = Cat2Num()
        self.__split_data = split_data
        self.__confusion_matrix = confusion_matrix
        self.__metrics = metrics
        self.__clf = None
        
    def fit(self, verbose=True):
        """
        Fit the machine learning model using the training data.

        Args:
            verbose (bool, optional): Whether to display performance metrics. Defaults to True.
        """
        data = self.__lbl_encoder.cat2num(self.__df)
        train, test = self.__split_data(df=data, 
                                        test_size=self.__test_size, 
                                        shuffle=self.__shuffle, 
                                        random_state=self.__random_state)
        
        X_train, y_train = train[self.__features], train[self.__target]
        clf = self.__model.fit(X=X_train, y=y_train)
        
        if verbose:
            y_pred = clf.predict(X_train)
            matrix = self.__confusion_matrix(y_train, y_pred)
            report_df = self.__metrics(matrix, self.__lbl_encoder.dict_map[self.__target].keys())
            display(report_df)
                    
        self.__train = train
        self.__test = test
        self.__clf = clf
        
    def evaluate(self, verbose=True):
        """
        Evaluate the trained machine learning model using the test data.

        Args:
            verbose (bool, optional): Whether to display performance metrics. Defaults to True.

        Returns:
            trained_model: The trained machine learning model.

        Raises:
            VariableNotInitializedError: If `fit()` has not been executed before calling `evaluate()`.
        """
        if self.__clf == None:
            raise VariableNotInitializedError("model", suggestion="Try fitting it first using `fit()` method.")
            
        X_test = self.__test[self.__features]
        y_test = self.__test[self.__target]
        
        if verbose:
            y_pred = self.__clf.predict(X_test)
            matrix = self.__confusion_matrix(y_test, y_pred)
            report_df = self.__metrics(matrix, self.__lbl_encoder.dict_map[self.__target].keys())
            display(report_df)
        
        return self.__clf