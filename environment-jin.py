class Environment:

    PRICE_IDX = 4 # 종가의 인덱스 위치

    def __init__(self, chart_data=None):
        self.chart_data = chart_data
        self.observation = None
        self.idx = -1

    def reset(self):
        self.observation = None
        self.idx = -1

    def observe(self):
        if len(self.chart_data) > self.idx + 1: # 데이터의 길이가 0이 아니면
            self.idx += 1 # 인덱스를 한칸 앞으로 만들고(맨 처음에는 0으로 만들고)
            self.observation = self.chart_data.iloc[self.idx] # 해당 인덱스의 값을 받아온 다음에
            return self.observation # 받아온 인덱스를 갖고 observation에 넣는다
        return None

    def get_price(self): #
        if self.observation is not None: # 관찰한 값이 None이 아니라면
            return self.observation[self.PRICE_IDX] # 해당 인스턴스의 PRICE_IDX에 해당하는 값을 가지고 온다
        return None

