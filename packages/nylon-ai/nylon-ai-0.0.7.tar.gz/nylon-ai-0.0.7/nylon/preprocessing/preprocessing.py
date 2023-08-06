import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from prince.ca import CA
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from autocorrect import Speller
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (OneHotEncoder,
                                   StandardScaler,
                                   FunctionTransformer, LabelEncoder)

import warnings

warnings.filterwarnings('ignore')


def initial_preprocessor(
        data,
        json_file):
    '''
    initial preprocessing function that's called in the case that the user doesn't provide a preprocessing option
    :param data: dataframe
    :param json_file: is the json file with the specifications for preprocessing
    :return initially preprocessed dataframe
    '''
    object_columns = [
        col for col,
                col_type in data.dtypes.iteritems() if col_type == 'object']

    # Handles dates without timestamps
    for col in object_columns:
        try:
            data[col] = pd.to_datetime(data[col], infer_datetime_format=True)
        except ValueError:
            pass

    # get target column
    target = json_file['data']['target']
    y = data[target]

    # remove rows where target is NaN
    data = data[y.notna()]
    y = y[y.notna()]

    del data[target]
    X_train, X_test, y_train, y_test = train_test_split(
        data, y, test_size=0.2)

    data = {
        'train': pd.concat([X_train], axis=1),
        'test': pd.concat([X_test], axis=1)
    }
    # preprocess the dataset
    full_pipeline = None
    if True:
        data, full_pipeline = structured_preprocessor(data)
    else:
        data.fillna(0, inplace=True)

    y = {'train': y_train, 'test': y_test}

    return data, y


def structured_preprocessor(data, ca_threshold=0.5, text=[]):
    '''
    structured preprocessing function that's called in the case that the user doesn't provide a preprocessing option, called after the initial changes
    :param data: dataframe
    :param ca_threshold: is correspondence analysis threshold for removing columns
    :param text: textual columns that require preprocessing by lemmatization, tokenization
    :return preprocessed dataframe
    '''

    # Preprocessing for datetime columns
    process_dates(data)

    # This will be used inside process_text once complete
    if len(text) > 0:
        text_preprocessing(data, text)

    # identifies the categorical and numerical columns
    categorical_columns = data['train'].select_dtypes(
        exclude=["number"]).columns
    numeric_columns = data['train'].columns[data['train'].dtypes.apply(
        lambda c: np.issubdtype(c, np.number))]

    # Removes text columns from categorical columns to use in separate pipeline
    categorical_columns = [
        cat_cols for cat_cols in categorical_columns if cat_cols not in text]

    full_pipeline = ColumnTransformer([], remainder="passthrough")

    if len(numeric_columns) != 0:
        # pipeline for numeric columns
        num_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy="median")),
            ('std_scaler', StandardScaler())
        ])

        full_pipeline.transformers.append(
            ("num", num_pipeline, numeric_columns))

    if len(text) != 0:
        # Each text col needs a separate pipeline
        for x in range(len(text)):
            full_pipeline.transformers.append(
                (f"text_{x}",
                 Pipeline(
                     [
                         ('test',
                          FunctionTransformer(
                              lambda x: np.reshape(
                                  x.to_numpy(),
                                  (-1,
                                   1)))),
                         ('imputer',
                          SimpleImputer(
                              strategy="constant",
                              fill_value="")),
                         ('raveler',
                          FunctionTransformer(
                              lambda x: x.ravel(),
                              accept_sparse=True)),
                         ('vect',
                          TfidfVectorizer()),
                         ('densifier',
                          FunctionTransformer(
                              lambda x: x.todense(),
                              accept_sparse=True)),
                         ('embedder',
                          FunctionTransformer(
                              textembedder,
                              accept_sparse=True))]),
                 text[x]))

    if len(categorical_columns) != 0:
        combined = pd.concat([data['train'], data['test']], axis=0)

        ca_threshold = combined.shape[0] * \
                       .25 if ca_threshold is None else combined.shape[0] * ca_threshold

        if too_many_values(combined[categorical_columns], ca_threshold):
            cat_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy="constant", fill_value="")),
                ('one_hotencoder', OneHotEncoder(handle_unknown='ignore')),
                ('transformer', FunctionTransformer(lambda x: x.toarray(), accept_sparse=True)),
                ('ca', CA(n_components=-1))
            ])
        else:
            cat_pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy="constant", fill_value="")),
                ('one_hotencoder', OneHotEncoder(handle_unknown='ignore'))
            ])

        full_pipeline.transformers.append(
            ('cat', cat_pipeline, categorical_columns))

    train = full_pipeline.fit_transform(data['train'])

    train_cols = generate_column_labels(full_pipeline, numeric_columns, text)

    test = full_pipeline.transform(data['test'])

    test_cols = generate_column_labels(full_pipeline, numeric_columns, text)

    # Ternary clause because when running housing.csv,
    # the product of preprocessing is np array, but not when using landslide
    # data... not sure why
    data['train'] = pd.DataFrame(
        (train.toarray() if not isinstance(
            train,
            np.ndarray) else train),
        columns=train_cols)
    data['test'] = pd.DataFrame(
        (test.toarray() if not isinstance(
            test,
            np.ndarray) else test),
        columns=test_cols)
    return data, full_pipeline


def process_dates(data):
    '''
    function to process dates
    :param data: dataframe
    :return dataframe with dates preprocessed
    '''
    for df in data:
        df = data[df]
        datetime_cols = df.select_dtypes('datetime64')
        for col in datetime_cols:
            df[f'{col}_DayOfWeek'] = df[col].dt.day_name()
            df[f'{col}_Year'] = df[col].dt.year
            df[f'{col}_Month'] = df[col].dt.month_name()
            df[f'{col}_MonthDay'] = df[col].dt.day

            del df[col]


# Preprocesses text for word embedding


def text_preprocessing(data, text_cols):
    '''
    function to process text
    :param data: dataframe
    :param text_cols: are the text columns that can be preprocessed
    :return dataframe with dates preprocessed
    '''
    lemmatizer = WordNetLemmatizer()
    combined = pd.concat([data['train'], data['test']], axis=0)

    spell = Speller(fast=True)
    for col in text_cols:
        combined[col] = combined[col].apply(
            lambda x: x.lower() if isinstance(x, str) else x)

    stop_words = set(stopwords.words('english'))

    for col in text_cols:
        preprocessed_text = []
        for words in combined[col]:
            if words is not np.nan:
                words = word_tokenize(words)
                words = [word for word in words if word.isalpha()]
                words = [word for word in words if word not in stop_words]
                words = [spell(word) for word in words]
                words = [lemmatizer.lemmatize(word) for word in words]

                preprocessed_text.append(' '.join(words))

            else:
                preprocessed_text.append(np.nan)

        combined[col] = preprocessed_text
    data['train'] = combined.iloc[:len(data['train'])]
    data['test'] = combined.iloc[len(data['train']):]


def textembedder(text):
    '''
    function to embed textual columns
    :param text: the text columns
    :return the text in embedded columns
    '''
    total = list()
    for i in text:
        total.append(np.sum(i))

    return np.reshape(total, (-1, 1))


# Sees if one hot encoding occurred, if not just uses numeric cols


def generate_column_labels(full_pipeline, numeric_cols, text_cols):
    # Check if one hot encoding was performed
    if 'cat' in full_pipeline.named_transformers_:
        # If ca was used
        if isinstance(full_pipeline.named_transformers_['cat'][-1], CA):
            ca = full_pipeline.named_transformers_['cat'][-1]
            encoded_cols = [f'CA_{x}' for x in range(len(ca.eigenvalues_))]
            cols = [*list(numeric_cols), *encoded_cols, *text_cols]

        else:
            try:
                encoded_cols = full_pipeline.named_transformers_[
                    'cat']['one_hotencoder'].get_feature_names()
                cols = [*list(numeric_cols), *encoded_cols, *text_cols]

            except Exception as error:
                # For debugging only
                (error)
                cols = list(numeric_cols)

        return cols
    else:
        return [*list(numeric_cols), *text_cols]


# Method to calculate how many columns the data set will
# have after one hot encoding
# Decides whether CA is needed or not essentially
# mca_threshold is the len of the dataset * .25 to calculate the proportion of
# when to apply CA
def too_many_values(data, ca_threshold):
    total_unique = 0
    for col in data:

        if total_unique > ca_threshold:
            return True
        # Use value_counts() due to same columns having strings and floats
        total_unique += len(data[col].value_counts())

    return False
