import numpy as np


class Agent:
    # 에이전트 상태가 구성하는 값 개수
    STATE_DIM = 2 # 주식 보유 비율, 포트폴리오 가치 비율 2 차원

    # 매매 수수료 및 세금
    TRADING_CHARGE = 0 # 거래 수수료 미고려 (실제로는 0.015%선)
    TRADING_TAX = 0 # 거래세 미고려 (실제 0.3%)

    # 행동
    ACTION_BUY = 0 # 매수
    ACTION_SELL = 1 # 매도
    ACTION_HOLD = 2 # 관망
    ACTIONS = [ACTION_BUY, ACTION_SELL] # 인공 신경망에서 확률을 구할 행동들
    NUM_ACTIONS = len(ACTIONS) # 인공 신경망에서 고려할 출력값의 개수

    def __init__(self, environment, min_trading_unit=1, max_trading_unit=2,
                 delayed_reward_threshold = .05):
        # Environment 객체
        self.environment = environment

        # 최소 매매 단위, 최대 매매 단위, 지연보상 임계치
        self.min_trading_unit = min_trading_unit
        self.max_trading_unit = max_trading_unit
        self.delayed_reward_threshold = delayed_reward_threshold

        # Agent 클래스의 속성
        self.initial_balance = 0 # 초기 자본금
        self.balance = 0 # 현재 현금 잔고
        self.num_stocks = 0 # 보유 주식 수
        self.portfolio_value = 0 # balance + num_stocks * {현재 주식 가격}
        self.base_portfolio_value = 0 # 기준 포트폴리오 가치, 직전 학습 시점의 PV
        self.num_buy = 0 # 매수 횟수
        self.num_sell = 0 # 매도 횟수
        self.num_hold = 0 # 관망 횟수
        self.immediate_reward = 0 # 즉시 보상

        # Agent 클래스의 상태
        self.ratio_hold = 0  # 최대 보유할 수 있는 주식 수 대비 현재 보유 주식의 비율
        self.ratio_portfolio_value = 0 # 직전 지연 보상이 발생했을 때의 포트폴리오 가치 대비 현재 포트폴리오 가치의 비율

    def reset(self):
        '''
        Agent 클래스의 속성들을 초기화해 준다. 학습 단계에서 한 에포크마다 에이전트의 상태를 초기화해야 하기 때문이다.
        '''
        self.balance = self.initial_balance
        self.num_stocks = 0
        self.portfolio_value = self.initial_balance
        self.base_portfolio_value = self.initial_balance
        self.num_buy = 0
        self.num_sell = 0
        self.num_hold = 0
        self.immediate_reward = 0
        self.ratio_hold = 0
        self.ratio_portfolio_value =0

    def set_balance(self, balance):
        '''
        에이전트의 초기 자본금 설정
        :param balance:
        '''
        self.initial_balance = balance

    def get_states(self):
        '''
        에이전트의 상태 반환
        :return:
        '''
        self.ratio_hold = self.num_hold / int(self.portfolio_value / self.environment.get_price())
        self.ratio_portfolio_value = self.portfolio_value / self.initial_balance
        return (
            self.ratio_hold,
            self.ratio_portfolio_value
        )

    def decide_action(self, policy_network, sample, epsilon):
        confidence = 0.
        # 탐험 결정