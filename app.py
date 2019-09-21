from PySide2 import QtWidgets, QtGui
import currency_converter

class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Currency Converter")
        self.converter = currency_converter.CurrencyConverter(fallback_on_missing_rate=True, fallback_on_wrong_date=True)
        self.setup_ui()
        self.set_default_values()
        self.setup_connections()

    def set_default_values(self):
        self.cbb_currencyFrom.addItems(sorted(list(self.converter.currencies)))
        self.cbb_currencyTo.addItems(sorted(list(self.converter.currencies)))
        self.cbb_currencyFrom.setCurrentText("EUR")
        self.cbb_currencyTo.setCurrentText("HKD")

        self.spn_amount.setRange(0, 1000000000)
        self.spn_amountConverted.setRange(0, 1000000000)
        self.spn_amount.setValue(100)
        self.compute()

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.cbb_currencyFrom = QtWidgets.QComboBox()
        self.spn_amount = QtWidgets.QDoubleSpinBox()
        self.cbb_currencyTo = QtWidgets.QComboBox()
        self.spn_amountConverted = QtWidgets.QDoubleSpinBox()
        self.btn_reverseCurrency = QtWidgets.QPushButton("Reverse")

        self.layout.addWidget(self.cbb_currencyFrom)
        self.layout.addWidget(self.spn_amount)
        self.layout.addWidget(self.cbb_currencyTo)
        self.layout.addWidget(self.spn_amountConverted)
        self.layout.addWidget(self.btn_reverseCurrency)
    
    def setup_connections(self):
        self.cbb_currencyFrom.activated.connect(self.compute)
        self.cbb_currencyTo.activated.connect(self.compute)
        self.spn_amount.valueChanged.connect(self.compute)
        self.btn_reverseCurrency.clicked.connect(self.reverse_currency)


    def compute(self):
        amount = self.spn_amount.value()
        currency_from = self.cbb_currencyFrom.currentText()
        currency_to = self.cbb_currencyTo.currentText()

        try:
            result = self.converter.convert(amount, currency_from, currency_to)
        except currency_converter.currency_converter.RateNotFoundError:
            print("Impossible to convert")
        else:
            self.spn_amountConverted.setValue(result)

    def reverse_currency(self):
        currency_from = self.cbb_currencyFrom.currentText()
        currency_to = self.cbb_currencyTo.currentText()

        self.cbb_currencyFrom.setCurrentText(currency_to)
        self.cbb_currencyTo.setCurrentText(currency_from)

        self.compute()


app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()