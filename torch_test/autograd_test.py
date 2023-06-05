import torch
from torchvision.models import resnet18, ResNet18_Weights


"""
신경망을 학습하는 것은 2단계로 이루어집니다:

순전파(Forward Propagation): 
순전파 단계에서, 신경망은 정답을 맞추기 위해 최선의 추측(best guess)을 합니다. 
이렇게 추측을 하기 위해서 입력 데이터를 각 함수들에서 실행합니다.

역전파(Backward Propagation): 
역전파 단계에서, 신경망은 추측한 값에서 발생한 오류(error)에 비례하여(proportionate) 매개변수들을 적절히 조절(adjust)합니다. 
출력(output)로부터 역방향으로 이동하면서 오류에 대한 함수들의 매개변수들의 미분값( 변화도(gradient) )을 수집하고, 
경사하강법(gradient descent)을 사용하여 매개변수들을 최적화 합니다. 역전파에 대한 자세한 설명은 3Blue1Brown의 비디오 를 참고하세요.

PyTorch에서 사용법
학습 단계를 하나만 살펴보겠습니다. 여기에서는 torchvision 에서 미리 학습된 resnet18 모델을 불러옵니다. 
3채널짜리 높이와 넓이가 64인 이미지 하나를 표현하는 무작위의 데이터 텐서를 생성하고, 이에 상응하는 label(정답) 을 무작위 값으로 초기화합니다. 
미리 학습된 모델의 정답(label)은 (1, 1000)의 모양(shape)을 갖습니다.
"""
model = resnet18(weights=ResNet18_Weights.DEFAULT)
data = torch.rand(1, 3, 64, 64)
labels = torch.rand(1, 1000)


"""
다음으로, 입력(input) 데이터를 모델의 각 층(layer)에 통과시켜 예측값(prediction)을 생성해보겠습니다. 이것이 순전파 단계 입니다.
"""
prediction = model(data)


"""
모델의 예측값과 그에 해당하는 정답(label)을 사용하여 오차(error, 손실(loss) )를 계산합니다. 
다음 단계는 신경망을 통해 이 에러를 역전파하는 것입니다. 
오차 텐서(error tensor)에 .backward() 를 호출하면 역전파가 시작됩니다. 
그 다음 Autograd가 매개변수(parameter)의 .grad 속성(attribute)에, 모델의 각 매개변수에 대한 변화도(gradient)를 계산하고 저장합니다.
"""
loss = (prediction - labels).sum()
loss.backward()


"""
다음으로, 옵티마이저(optimizer)를 불러옵니다.
이 예제에서는 학습율(learning rate) 0.1과 모멘텀(momentum) 0.9를 갖는 SGD입니다.
옵티마이저(optimizer)에 모델의 모든 매개변수를 등록합니다.
"""
optim = torch.optim.SGD(model.parameters(), lr=1e-2, momentum=0.9)
optim.step()



# Autograd에서 미분(differentiation)
"""
autograd 가 어떻게 변화도(gradient)를 수집하는지 살펴보겠습니다. 
requires_grad=True 를 갖는 2개의 텐서(tensor) a 와 b 를 만듭니다. 
requires_grad=True 는 autograd 에 모든 연산(operation)들을 추적해야 한다고 알려줍니다.
"""
a = torch.tensor([2., 3.], requires_grad=True)
b = torch.tensor([6., 4.], requires_grad=True)


"""
이제 a 와 b 로부터 새로운 텐서 Q 를 만듭니다
"""
Q = 3*a**3 - b**2


"""
이제 a 와 b 가 모두 신경망(NN)의 매개변수이고, Q 가 오차(error)라고 가정해보겠습니다. 
신경망을 학습할 때, 아래와 같이 매개변수들에 대한 오차의 변화도(gradient)를 구해야 합니다.

Q 에 대해서 .backward() 를 호출할 때, autograd는 이러한 변화도들을 계산하고 이를 각 텐서의 .grad 속성(attribute)에 저장합니다.
Q 는 벡터(vector)이므로 Q.backward() 에 gradient 인자(argument)를 명시적으로 전달해야 합니다. 
gradient 는 Q 와 같은 모양(shape)의 텐서로, Q 자기 자신에 대한 변화도(gradient)를 나타냅니다.
"""