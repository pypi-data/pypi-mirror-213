class bmi_class():
    def __init__(self):
        self.weight = 0
        self.height = 0
        self.result = ""
    def bmi_calculator(self):
        return round(self.weight/(self.height*self.height)*10000, 2)
    def bmi_text(self, x):
        if x > 25.0:
            self.result = "비만"
        elif x > 23.0 and x < 24.9:
            self.result = "과체중"
        elif x > 18.5 and x < 22.9:
            self.result = "정상"
        elif x < 18.5:
            self.result =  "저체중"
        return self.result
