class InvestigationSettings:
    def __init__(self):
        self._plot_setting = None
        self._h_finite_differences = None
        self._detect_instabilities = False

    @property
    def PlotSetting(self):
        return self._plot_setting

    def set_PlotSetting(self, value):
        self._plot_setting = value

    @property
    def FiniteDifferencesStepWidth(self):
        return self._h_finite_differences

    def set_FiniteDifferencesStepWidth(self, value):
        self._h_finite_differences = value
        
    @property
    def DetectInstabilities(self):
        return self._detect_instabilities

    def set_DetectInstabilities(self, value):
        self._detect_instabilities = bool(value)