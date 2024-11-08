import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

# 1. 데이터 로드 및 전처리
cat_data = np.load('cat.npy')
X = cat_data / 255.0
X = X.reshape(-1, 28, 28, 1)
X = shuffle(X, random_state=42)
X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

# 2. 오토인코더 모델 구축
input_img = Input(shape=(28, 28, 1))

# 인코더
x = Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)

x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
encoded = MaxPooling2D((2, 2), padding='same')(x)

# 디코더 (수정된 부분)
x = Conv2D(8, (3, 3), activation='relu', padding='same')(encoded)
x = UpSampling2D((2, 2))(x)

x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)  # padding='same' 추가
x = UpSampling2D((2, 2))(x)

decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

# 모델 생성
autoencoder = Model(input_img, decoded)

# 3. 모델 컴파일 및 학습
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

autoencoder.fit(X_train, X_train,
                epochs=10,
                batch_size=256,
                shuffle=True,
                validation_data=(X_test, X_test))

# 4. 결과 확인
decoded_imgs = autoencoder.predict(X_test[:10])

# 원본과 재구성 이미지 비교
n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
    # 원본 이미지
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(X_test[i].reshape(28, 28), cmap='gray')
    plt.title("sample")
    plt.axis('off')

    # 재구성된 이미지
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i].reshape(28, 28), cmap='gray')
    plt.title("regusung")
    plt.axis('off')
plt.show()