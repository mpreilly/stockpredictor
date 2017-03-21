import pandas as pd
import tensorflow as tf
import tempfile

COLUMNS = ['Stock', 'Closing_Price', 'Percent_Change', 'Volume', 'PEG_Ratio',
            'Short_Ratio', 'Pct_Change_from_Year_High', 'Pct_Change_from_Year_Low',
            'Pct_Change_from_50_day_Moving_Avg', 'Ratio_to_Target', 'Stochastic_Oscillator']

df_train = pd.read_csv('data/training_1day_data.csv', names=COLUMNS, skiprows=1)
df_test = pd.read_csv('data/testing_1day_data.csv', names=COLUMNS, skiprows=1)

training_nextday = pd.read_csv('data/training_1day_nextdaychanges.csv', names=('next_day_pct_change',))
testing_nextday = pd.read_csv('data/testing_1day_nextdaychanges.csv', names=('next_day_pct_change',))

LABEL_COLUMN = 'label'
df_train[LABEL_COLUMN] = (training_nextday['next_day_pct_change'] > 0).astype(int)
df_test[LABEL_COLUMN] = (testing_nextday['next_day_pct_change'] > 0).astype(int)

# data_cols = ['Closing_Price', 'Percent_Change', 'Volume', 'PEG_Ratio',
#             'Short_Ratio', 'Pct_Change_from_Year_High', 'Pct_Change_from_Year_Low',
#             'Pct_Change_from_50_day_Moving_Avg', 'Ratio_to_Target', 'Stochastic_Oscillator']

data_cols = ['Percent_Change', 'Volume', 'Stochastic_Oscillator']

def input_fn(df):
    feature_cols = {k: tf.constant(df[k].values)
                    for k in data_cols}
    label = tf.constant(df[LABEL_COLUMN].values)
    return feature_cols, label

def train_input_fn():
    return input_fn(df_train)

def eval_input_fn():
    return input_fn(df_test)

# closing_price = tf.contrib.layers.real_valued_column('Closing_Price')
pct_change = tf.contrib.layers.real_valued_column('Percent_Change')
volume = tf.contrib.layers.real_valued_column('Volume')
# peg = tf.contrib.layers.real_valued_column('PEG_Ratio')
# short = tf.contrib.layers.real_valued_column('Short_Ratio')
# pct_high = tf.contrib.layers.real_valued_column('Pct_Change_from_Year_High')
# pct_low = tf.contrib.layers.real_valued_column('Pct_Change_from_Year_Low')
# pct_avg = tf.contrib.layers.real_valued_column('Pct_Change_from_50_day_Moving_Avg')
# ratio_target = tf.contrib.layers.real_valued_column('Ratio_to_Target')
sto_osc = tf.contrib.layers.real_valued_column('Stochastic_Oscillator')

model_dir = tempfile.mkdtemp()
# m = tf.contrib.learn.LinearClassifier(feature_columns=[closing_price, pct_change,
#                 volume, peg, short, pct_high, pct_low, pct_avg, ratio_target, sto_osc],
#                 model_dir=model_dir)

m = tf.contrib.learn.LinearClassifier(feature_columns=[pct_change,
                volume, sto_osc],
                model_dir=model_dir)

m.fit(input_fn=train_input_fn, steps=2000)

results = m.evaluate(input_fn=eval_input_fn, steps=1)
for key in sorted(results):
    print '%s: %s' % (key, results[key])
