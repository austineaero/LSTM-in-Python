{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "wrong-jimmy",
   "metadata": {},
   "source": [
    "# Import Libraries"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "distributed-omega",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Using TensorFlow backend.\n"
     ]
    }
   ],
   "source": [
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import pandas as pd\n",
    "import tensorflow as tf\n",
    "from math import sqrt\n",
    "from sklearn.metrics import mean_squared_error\n",
    "from sklearn.preprocessing import MinMaxScaler\n",
    "from keras.models import Sequential\n",
    "from keras.layers import Dense, Flatten, LSTM, RepeatVector, TimeDistributed, Dropout"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "blank-estate",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "1 Physical GPUs, 1 Logical GPUs\n"
     ]
    }
   ],
   "source": [
    "# To test and connect your work to your gpu if you have one\n",
    "gpus = tf.config.experimental.list_physical_devices('GPU')\n",
    "if gpus:\n",
    "    try:\n",
    "        # Restrict TensorFlow to only use the fourth GPU\n",
    "        tf.config.experimental.set_visible_devices(gpus[0], 'GPU')\n",
    "\n",
    "        # Currently, memory growth needs to be the same across GPUs\n",
    "        for gpu in gpus:\n",
    "            tf.config.experimental.set_memory_growth(gpu, True)\n",
    "        logical_gpus = tf.config.experimental.list_logical_devices('GPU')\n",
    "        print(len(gpus), \"Physical GPUs,\", len(logical_gpus), \"Logical GPUs\")\n",
    "    except RuntimeError as e:\n",
    "        # Memory growth must be set before GPUs have been initialized\n",
    "        print(e)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "simplified-brave",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<module 'tensorflow_core._api.v2.version' from 'C:\\\\Users\\\\Austin\\\\anaconda3\\\\envs\\\\deep_learning\\\\lib\\\\site-packages\\\\tensorflow_core\\\\_api\\\\v2\\\\version\\\\__init__.py'>"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "tf.version"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "numeric-australia",
   "metadata": {},
   "source": [
    "# Preprocessing"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "static-cruise",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>co2</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>count</th>\n",
       "      <td>135099.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>mean</th>\n",
       "      <td>688.833011</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>std</th>\n",
       "      <td>385.845573</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>min</th>\n",
       "      <td>369.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>25%</th>\n",
       "      <td>429.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>50%</th>\n",
       "      <td>483.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>75%</th>\n",
       "      <td>852.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>max</th>\n",
       "      <td>2626.000000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                 co2\n",
       "count  135099.000000\n",
       "mean      688.833011\n",
       "std       385.845573\n",
       "min       369.000000\n",
       "25%       429.000000\n",
       "50%       483.000000\n",
       "75%       852.000000\n",
       "max      2626.000000"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Import the data\n",
    "df = pd.read_csv('C:/Users/Austin/Documents/Jeff Kimmel/CO2.csv') # Change this directory to yours.\n",
    "df.describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "retired-wrapping",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>co2</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>ts</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>11/21/2016 0:47</th>\n",
       "      <td>708</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>11/21/2016 0:48</th>\n",
       "      <td>694</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>11/21/2016 0:49</th>\n",
       "      <td>693</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>11/21/2016 0:50</th>\n",
       "      <td>692</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>11/21/2016 0:51</th>\n",
       "      <td>690</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                 co2\n",
       "ts                  \n",
       "11/21/2016 0:47  708\n",
       "11/21/2016 0:48  694\n",
       "11/21/2016 0:49  693\n",
       "11/21/2016 0:50  692\n",
       "11/21/2016 0:51  690"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Set date_time as index\n",
    "df = df.set_index('ts')\n",
    "# Show the data\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "surgical-brunei",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "Index: 135099 entries, 11/21/2016 0:47 to 3/28/2017 9:30\n",
      "Data columns (total 1 columns):\n",
      " #   Column  Non-Null Count   Dtype  \n",
      "---  ------  --------------   -----  \n",
      " 0   co2     135099 non-null  float32\n",
      "dtypes: float32(1)\n",
      "memory usage: 1.5+ MB\n"
     ]
    }
   ],
   "source": [
    "df = df.astype('float32')\n",
    "df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "spoken-sperm",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([[0.15019937],\n",
       "       [0.14399646],\n",
       "       [0.14355339],\n",
       "       ...,\n",
       "       [0.43597692],\n",
       "       [0.4337616 ],\n",
       "       [0.44040757]], dtype=float32)"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# normalise or scale data to be between 0 and 1\n",
    "scaler = MinMaxScaler(feature_range=(0,1))\n",
    "df1 = scaler.fit_transform(np.array(df).reshape(-1,1))\n",
    "df1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "dental-induction",
   "metadata": {},
   "outputs": [],
   "source": [
    "# split the co2 dataset into train/test sets\n",
    "# The first 9 datasets are truncated so as to give a proper split into 30mins-interval\n",
    "def split_dataset(data):\n",
    "    # split in the ratio 70-30\n",
    "    train, test = data[9:int(len(df)*.7)], data[int(len(df)*.7):]\n",
    "    # restructure into windows of 30min data\n",
    "    train = np.array(np.split(train, len(train)/30))\n",
    "    test = np.array(np.split(test, len(test)/30))\n",
    "    return train, test"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "liquid-needle",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(3152, 30, 1)\n",
      "0.14355339 0.31103235\n",
      "(1351, 30, 1)\n",
      "0.3256535 0.44040757\n"
     ]
    }
   ],
   "source": [
    "train, test = split_dataset(df1)\n",
    "# validate train data\n",
    "print(train.shape)\n",
    "print(train[0, 0, 0], train[-1, -1, 0])\n",
    "# validate test\n",
    "print(test.shape)\n",
    "print(test[0, 0, 0], test[-1, -1, 0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "treated-marina",
   "metadata": {},
   "outputs": [],
   "source": [
    "# convert history into inputs and outputs\n",
    "def to_supervised(train, n_input, n_out=30):\n",
    "    # flatten data\n",
    "    data = train.reshape((train.shape[0]*train.shape[1], train.shape[2]))\n",
    "    X, y = list(), list()\n",
    "    in_start = 0\n",
    "    # step over the entire history one time step at a time\n",
    "    for _ in range(len(data)):\n",
    "        # define the end of the input sequence\n",
    "        in_end = in_start + n_input\n",
    "        out_end = in_end + n_out\n",
    "        # ensure we have enough data for this instance\n",
    "        if out_end <= len(data):\n",
    "            x_input = data[in_start:in_end, 0]\n",
    "            x_input = x_input.reshape((len(x_input), 1))\n",
    "            X.append(x_input)\n",
    "            y.append(data[in_end:out_end, 0])\n",
    "        # move along one time step\n",
    "        in_start += 1\n",
    "    return np.array(X), np.array(y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "sufficient-organization",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "((94501, 30, 1), (94501, 30))"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Quick check to test the function \"to_supervised\"\n",
    "train_x, train_y = to_supervised(train, 30)\n",
    "test_x, test_y = to_supervised(test, 30)\n",
    "train_x.shape, train_y.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "younger-relation",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([[ 693.     ,  695.     ,  695.     , ...,  733.     ,  733.     ,\n",
       "         735.     ],\n",
       "       [ 695.     ,  695.     ,  696.     , ...,  733.     ,  735.     ,\n",
       "         739.     ],\n",
       "       [ 695.     ,  696.     ,  697.     , ...,  735.     ,  739.     ,\n",
       "         741.99994],\n",
       "       ...,\n",
       "       [1076.0001 , 1067.     , 1099.     , ..., 1081.     , 1071.0001 ,\n",
       "        1061.0001 ],\n",
       "       [1067.     , 1099.     , 1089.     , ..., 1071.0001 , 1061.0001 ,\n",
       "        1050.     ],\n",
       "       [1099.     , 1089.     , 1073.0001 , ..., 1061.0001 , 1050.     ,\n",
       "        1069.     ]], dtype=float32)"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# I am transforming back to the original dataset so you see that y is actually 30mins ahead.\n",
    "# X1 and y1 are just for this test. \n",
    "X1 = train_x.reshape(94501, 30) # reshape from 3D to 2D\n",
    "X1 = scaler.inverse_transform(X1)\n",
    "y1 = scaler.inverse_transform(train_y)\n",
    "X1 # The first row of X1 starts from the 10th row in the dataset"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "earned-remainder",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([[ 739.     ,  741.99994,  743.     , ..., 1050.     , 1064.     ,\n",
       "        1102.0001 ],\n",
       "       [ 741.99994,  743.     ,  747.     , ..., 1064.     , 1102.0001 ,\n",
       "        1113.     ],\n",
       "       [ 743.     ,  747.     ,  756.     , ..., 1102.0001 , 1113.     ,\n",
       "        1153.     ],\n",
       "       ...,\n",
       "       [1050.     , 1069.     , 1091.     , ..., 1056.     , 1056.     ,\n",
       "        1062.     ],\n",
       "       [1069.     , 1091.     , 1096.     , ..., 1056.     , 1062.     ,\n",
       "        1067.     ],\n",
       "       [1091.     , 1096.     , 1078.0001 , ..., 1062.     , 1067.     ,\n",
       "        1071.0001 ]], dtype=float32)"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "y1 # Each value is 30mins ahead of the first data of X1 "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "manual-publicity",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1152x576 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# As you can see the first X1 value 693 has a corresponding y1 value 739\n",
    "# Check the dataset. The first 9 data in the CO2 excel sheet were truncated. \n",
    "# So start from the 10th data in the sheet which is 693. Now count, 30 from 693, you will get 739- the value of y1\n",
    "# Here is a plot of X1 and y1 just for visualisation.\n",
    "\n",
    "plt.figure(figsize=(16,8))\n",
    "plt.title('Model', fontsize=18)\n",
    "plt.xlabel('Time_Step', fontsize=18)\n",
    "plt.ylabel('CO2', fontsize=18)\n",
    "plt.plot(X1[:,0][:100]) # First 100 data in the first column.\n",
    "plt.plot(y1[:,0][:100]) # First 100 data in the first column\n",
    "plt.legend(['X1', 'y1'], loc='upper right')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "hourly-thursday",
   "metadata": {},
   "source": [
    "# LSTM Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "elementary-teach",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Model: \"sequential_1\"\n",
      "_________________________________________________________________\n",
      "Layer (type)                 Output Shape              Param #   \n",
      "=================================================================\n",
      "lstm_1 (LSTM)                (None, 200)               161600    \n",
      "_________________________________________________________________\n",
      "repeat_vector_1 (RepeatVecto (None, 30, 200)           0         \n",
      "_________________________________________________________________\n",
      "lstm_2 (LSTM)                (None, 30, 200)           320800    \n",
      "_________________________________________________________________\n",
      "time_distributed_1 (TimeDist (None, 30, 100)           20100     \n",
      "_________________________________________________________________\n",
      "time_distributed_2 (TimeDist (None, 30, 1)             101       \n",
      "=================================================================\n",
      "Total params: 502,601\n",
      "Trainable params: 502,601\n",
      "Non-trainable params: 0\n",
      "_________________________________________________________________\n"
     ]
    }
   ],
   "source": [
    "# train the model\n",
    "n_input = 30\n",
    "train_x, train_y = to_supervised(train, n_input)\n",
    "# define parameters\n",
    "verbose, epochs, batch_size = 1, 10, 30\n",
    "n_timesteps, n_features, n_outputs = train_x.shape[1], train_x.shape[2], train_y.shape[1]\n",
    "# reshape output into [# LSTM Modelsamples, timesteps, features]\n",
    "train_y = train_y.reshape((train_y.shape[0], train_y.shape[1], 1))\n",
    "# define model\n",
    "model = Sequential()\n",
    "model.add(LSTM(200, activation='relu', dropout=0.2, input_shape=(n_timesteps, n_features)))\n",
    "model.add(RepeatVector(n_outputs))\n",
    "model.add(LSTM(200, activation='relu', dropout=0.2, return_sequences=True))\n",
    "model.add(TimeDistributed(Dense(100, activation='relu')))\n",
    "model.add(TimeDistributed(Dense(1)))\n",
    "model.compile(loss='mse', optimizer='adam')\n",
    "model.summary()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "id": "expired-merchandise",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch 1/10\n",
      "94501/94501 [==============================] - 239s 3ms/step - loss: 0.0070\n",
      "Epoch 2/10\n",
      "94501/94501 [==============================] - 244s 3ms/step - loss: 0.0066 3\n",
      "Epoch 3/10\n",
      "94501/94501 [==============================] - 234s 2ms/step - loss: 0.0064\n",
      "Epoch 4/10\n",
      "94501/94501 [==============================] - 203s 2ms/step - loss: 0.0064\n",
      "Epoch 5/10\n",
      "94501/94501 [==============================] - 190s 2ms/step - loss: 0.0065\n",
      "Epoch 6/10\n",
      "94501/94501 [==============================] - 189s 2ms/step - loss: 0.0063\n",
      "Epoch 7/10\n",
      "94501/94501 [==============================] - 189s 2ms/step - loss: 0.0067\n",
      "Epoch 8/10\n",
      "94501/94501 [==============================] - 190s 2ms/step - loss: 0.0062\n",
      "Epoch 9/10\n",
      "94501/94501 [==============================] - 191s 2ms/step - loss: 0.0063 \n",
      "Epoch 10/10\n",
      "94501/94501 [==============================] - 191s 2ms/step - loss: 0.0063\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "<keras.callbacks.callbacks.History at 0x2dbf5539cf8>"
      ]
     },
     "execution_count": 44,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# fit network\n",
    "model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size, verbose=verbose)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "celtic-redhead",
   "metadata": {},
   "outputs": [],
   "source": [
    "from keras.models import load_model\n",
    "\n",
    "# model.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'\n",
    "# del model - deletes the existing model\n",
    "\n",
    "model = load_model('my_model.h5') # returns a compiled model identical to the previous one"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "insured-capacity",
   "metadata": {},
   "outputs": [],
   "source": [
    "# make a forecast\n",
    "def forecast(model, history, n_input):\n",
    "    # flatten data\n",
    "    data = np.array(history)\n",
    "    data = data.reshape((data.shape[0]*data.shape[1], data.shape[2]))\n",
    "    # retrieve last observations for input data\n",
    "    input_x = data[-n_input:, 0]\n",
    "    # reshape into [1, n_input, 1]\n",
    "    input_x = input_x.reshape((1, len(input_x), 1))\n",
    "    # forecast the next 30min\n",
    "    yhat = model.predict(input_x, verbose=0)\n",
    "    # we only want the vector forecast\n",
    "    yhat = yhat[0]\n",
    "    return yhat"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "individual-hierarchy",
   "metadata": {},
   "outputs": [],
   "source": [
    "# evaluate one or more 30min forecasts against expected values\n",
    "def evaluate_forecasts(actual, predicted):\n",
    "    scores = list()\n",
    "    # calculate an RMSE score for each minute\n",
    "    for i in range(actual.shape[1]):\n",
    "        # calculate mse\n",
    "        mse = mean_squared_error(actual[:, i], predicted[:, i])\n",
    "        # calculate rmse\n",
    "        rmse = sqrt(mse)\n",
    "        # store\n",
    "        scores.append(rmse)\n",
    "    # calculate overall RMSE\n",
    "    s = 0\n",
    "    for row in range(actual.shape[0]):\n",
    "        for col in range(actual.shape[1]):\n",
    "            s += (actual[row, col] - predicted[row, col])**2\n",
    "    score = sqrt(s / (actual.shape[0] * actual.shape[1]))\n",
    "    return score, scores"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "small-atlanta",
   "metadata": {},
   "outputs": [],
   "source": [
    "# evaluate a single model\n",
    "def evaluate_model(train, test, n_input):\n",
    "    # fit model\n",
    "    model = load_model('my_model.h5')\n",
    "    # history is a list of 30min-interval data\n",
    "    history = [x for x in train]\n",
    "    # walk-forward validation over each 30min \n",
    "    predictions = list()\n",
    "    for i in range(len(test)):\n",
    "        # predict the 30min\n",
    "        yhat_sequence = forecast(model, history, n_input)\n",
    "        # store the predictions\n",
    "        predictions.append(yhat_sequence)\n",
    "        # get real observation and add to history for predicting the next 30min\n",
    "        history.append(test[i, :])\n",
    "    # evaluate predictions (minutes) for each 30min\n",
    "    predictions = np.array(predictions)\n",
    "    score, scores = evaluate_forecasts(test[:, :, 0], predictions)\n",
    "    return score, scores\n",
    "\n",
    "# summarize scores\n",
    "def summarize_scores(name, score, scores):\n",
    "    s_scores = ', '.join(['{:.1f}'.format(s) for s in scores])\n",
    "    print('{}: [{:.3f}] {}'.format(name, score, s_scores))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "powered-sending",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "lstm: [0.071] 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# evaluate model and get scores. The scores are approximately 0.1 but the actual values are as depicted in the graph.\n",
    "n_input = 30\n",
    "score, scores = evaluate_model(train, test, n_input)\n",
    "# summarize scores\n",
    "summarize_scores('lstm', score, scores)\n",
    "# plot scores\n",
    "time = [t for t in range(1,31)]\n",
    "plt.plot(time, scores, marker='o', label='lstm')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "id": "english-jackson",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(40471, 30)"
      ]
     },
     "execution_count": 28,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "test_y.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "id": "powerful-water",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(40471, 30)"
      ]
     },
     "execution_count": 31,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Lets Do the prediction and check performance metrics\n",
    "test_pred = model.predict(test_x) # test_pred is the prediction on test_x\n",
    "test_pred1 = test_pred.reshape(40471, 30) \n",
    "test_y1 = test_y # test_y is the actual value of y 30 minutes ahead given x\n",
    "test_x1 = test_x.reshape(40471, 30)\n",
    "test_y1.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "id": "polyphonic-oasis",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Transform back to original form\n",
    "test_x1 = scaler.inverse_transform(test_x1)\n",
    "test_y1 = scaler.inverse_transform(test_y1)\n",
    "test_pred1 = scaler.inverse_transform(test_pred1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 66,
   "id": "oriented-sleeping",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1152x576 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Plot test vs predictions \n",
    "time = np.arange(1,501) # 30 minute data needed for prediction\n",
    "time_pred = np.arange(31,531)\n",
    "#time = [t for t in range(1,1001)]\n",
    "plt.figure(figsize=(16,8))\n",
    "plt.title('Model')\n",
    "plt.xlabel('Time(min)', fontsize=18)\n",
    "plt.ylabel('CO2', fontsize=18)\n",
    "plt.plot(time, test_x1[-530:-30, 0])\n",
    "plt.plot(time_pred, test_y1[-500:, 0])\n",
    "plt.plot(time_pred, test_pred1[-500:, 0])\n",
    "plt.legend(['Dataset', 'Actual', 'Predictions'], loc='lower right')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 65,
   "id": "adapted-placement",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(500,)"
      ]
     },
     "execution_count": 65,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "test_x1[-530:-30, 0].shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 67,
   "id": "protecting-account",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>x_Dataset</th>\n",
       "      <th>Actual</th>\n",
       "      <th>Predicted</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>425.0</td>\n",
       "      <td>463.000000</td>\n",
       "      <td>447.339233</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>425.0</td>\n",
       "      <td>472.000000</td>\n",
       "      <td>446.436981</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>425.0</td>\n",
       "      <td>472.000000</td>\n",
       "      <td>454.209259</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>426.0</td>\n",
       "      <td>472.000000</td>\n",
       "      <td>458.603729</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>426.0</td>\n",
       "      <td>466.999969</td>\n",
       "      <td>459.567352</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>495</th>\n",
       "      <td>1212.0</td>\n",
       "      <td>1303.000122</td>\n",
       "      <td>1014.933105</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>496</th>\n",
       "      <td>1201.0</td>\n",
       "      <td>1318.000000</td>\n",
       "      <td>1014.199646</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>497</th>\n",
       "      <td>1209.0</td>\n",
       "      <td>1329.000000</td>\n",
       "      <td>1017.519409</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>498</th>\n",
       "      <td>1221.0</td>\n",
       "      <td>1325.000000</td>\n",
       "      <td>1025.810791</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>499</th>\n",
       "      <td>1210.0</td>\n",
       "      <td>1304.000000</td>\n",
       "      <td>1029.229248</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>500 rows × 3 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "     x_Dataset       Actual    Predicted\n",
       "0        425.0   463.000000   447.339233\n",
       "1        425.0   472.000000   446.436981\n",
       "2        425.0   472.000000   454.209259\n",
       "3        426.0   472.000000   458.603729\n",
       "4        426.0   466.999969   459.567352\n",
       "..         ...          ...          ...\n",
       "495     1212.0  1303.000122  1014.933105\n",
       "496     1201.0  1318.000000  1014.199646\n",
       "497     1209.0  1329.000000  1017.519409\n",
       "498     1221.0  1325.000000  1025.810791\n",
       "499     1210.0  1304.000000  1029.229248\n",
       "\n",
       "[500 rows x 3 columns]"
      ]
     },
     "execution_count": 67,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# This is how the predicted values compare with the actual test result for 30 minutes data. \n",
    "valid = pd.DataFrame({'x_Dataset':test_x1[-530:-30, 0], 'Actual':test_y1[-500:, 0], 'Predicted':test_pred1[-500:, 0]})\n",
    "valid"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "unnecessary-taste",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
