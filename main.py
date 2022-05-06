from asyncio.windows_events import NULL
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QDialog, QLineEdit, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from UI.mainWindow import Ui_MainWindow as mw
from UI.pokemonPopup import Ui_Dialog as pp
import sys
import mariadb

class mainWindowEvents(QMainWindow):
    def __init__(self, MainWindow, cur):
        super().__init__()
        self.ui = mw()
        self.ui.setupUi(MainWindow)
        self.cur = cur
        self.ui.pushButton.clicked.connect(self.search)
        self.ui.pushButton_2.clicked.connect(self.random)

    def search(self):
        print("search")
        pkmn_id = self.ui.idSearchLineEdit.text()
        pkmn_name = self.ui.nameSearchLineEdit.text()
        if pkmn_name == '':
            pkmn_name = '\'\' or 1 = 1'
        if pkmn_id == '':
            pkmn_id = '\'\' or 1 = 1'
        pkmn_id += ")"
        pkmn_name += ")"
        print(pkmn_name, pkmn_id)

        statOrder = self.getStatOrder()
        statCondition = self.getStatCondition()
        typeCondition = self.getTypeCondition()
        regionCondition = self.getRegionCondition()

        executeString = f"""
select p.PKMN_ID, p.PKMN_NAME, t.PKMN_TYPE1, t.PKMN_TYPE2, ps.STATS_TOTAL, ps.STATS_HP, ps.STATS_ATTACK, ps.STATS_DEFENSE, ps.STATS_SP_ATTACK, ps.STATS_SP_DEFENSE, ps.STATS_SPEED, pw.PKMN_WEIGHT, r.PKMN_REGION, e.EVOLUTION_ID, e.EVOLVING_ID
from pokemoninfo as p
join pokemonstats as ps on p.PKMN_ID = ps.PKMN_ID
join pokemonweight as pw on p.PKMN_ID = pw.PKMN_ID
join regionfound as r on p.PKMN_ID = r.PKMN_ID
join evolutions as e on p.PKMN_ID = e.PKMN_ID
join typechart as t on p.PKMN_ID = t.PKMN_ID
where (p.PKMN_ID = {pkmn_id}
and (p.PKMN_NAME = {pkmn_name}
and {statCondition}
and {typeCondition}
and {regionCondition}"""

        executeString += statOrder
        #print(executeString)

        self.cur.execute(executeString)
        result = self.cur.fetchall()
        #data = self.getQuery()

        # self.model = TableModel(data)
        # self.ui.searchResultsTableWidget.setModel(self.model)
        # self.setCentralWidget(self.ui.searchResultsTableWidget)
        self.ui.searchResultsTableWidget.setRowCount(0)
        self.ui.searchResultsTableWidget.setColumnCount(0)
        for row_number, row_data in enumerate(result):
            self.ui.searchResultsTableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if row_number == 0:
                    self.ui.searchResultsTableWidget.insertColumn(column_number)
                self.ui.searchResultsTableWidget.setItem(row_number,
                    column_number, QTableWidgetItem(str(data)))
    def random(self):
        print("random")

    def getQuery(self):
        row_headers=[x[0] for x in cur.description]
        rv = self.cur.fetchall()
        # print(rv)
        # json_data = []
        # for result in rv:
        #     json_data.append(dict(zip(row_headers,result)))
        # print(json_data)
        # return json_data
        return rv

    def getRegionCondition(self):
        regionCondition = "("
        if self.ui.kantoCheckBox.isChecked():
            regionCondition += "r.PKMN_REGION = \'Kanto\' and "
        if self.ui.johtoCheckBox.isChecked():
            regionCondition += "r.PKMN_REGION = \'Johto\' and "
        if self.ui.hoennCheckBox.isChecked():
            regionCondition += "r.PKMN_REGION = \'Hoenn\' and "
        if self.ui.sinnohCheckBox.isChecked():
            regionCondition += "r.PKMN_REGION = \'Sinnoh\' and "
        if self.ui.unovaCheckBox.isChecked():
            regionCondition += "r.PKMN_REGION = \'Unova\' and "
        if self.ui.kalosCheckBox.isChecked():
            regionCondition += "r.PKMN_REGION = \'Kalos\' and "
        if self.ui.alolaCheckBox.isChecked():
            regionCondition += "r.PKMN_REGION = \'Alola\' and "
        if self.ui.galarCheckBox.isChecked():
            regionCondition += "r.PKMN_REGION = \'Galar\' and "
        if self.ui.hisuiCheckBox.isChecked():
            regionCondition += "r.PKMN_REGION = \'Hisui\' and "
        
        if len(regionCondition) == 1:
            return "(1 = 1)"
        else:
            return regionCondition[0:-5] + ")"


    def getStatCondition(self):
        statCondition = "("
        if self.ui.hpMinLineEdit.text() != "":
            statCondition += "ps.STATS_HP > " + self.ui.hpMinLineEdit.text() + " and "
        if self.ui.hpMaxLineEdit.text() != "":
            statCondition += "ps.STATS_HP < " + self.ui.hpMaxLineEdit.text() + " and "
        if self.ui.attackMinLineEdit.text() != "":
            statCondition += "ps.STATS_ATTACK > " + self.ui.attackMinLineEdit.text() + " and "
        if self.ui.attackMaxLineEdit.text() != "":
            statCondition += "ps.STATS_ATTACK < " + self.ui.hpMaxLineEdit.text() + " and "
        if self.ui.defenseMinLineEdit.text() != "":
            statCondition += "ps.STATS_DEFENSE > " + self.ui.defenseMinLineEdit.text() + " and "
        if self.ui.defenseMaxLineEdit.text() != "":
            statCondition += "ps.STATS_DEFENSE < " + self.ui.defenseMaxLineEdit.text() + " and "
        if self.ui.specialAttackMinLineEdit.text() != "":
            statCondition += "ps.STATS_DEFENSE > " + self.ui.specialAttackMinLineEdit.text() + " and "
        if self.ui.specialAttackMaxLineEdit.text() != "":
            statCondition += "ps.STATS_DEFENSE < " + self.ui.specialAttackMaxLineEdit.text() + " and "
        if self.ui.specialDefenseMinLineEdit.text() != "":
            statCondition += "ps.STATS_DEFENSE > " + self.ui.specialDefenseMinLineEdit.text() + " and "
        if self.ui.specialDefenseMaxLineEdit.text() != "":
            statCondition += "ps.STATS_DEFENSE > " + self.ui.specialDefenseMaxLineEdit.text() + " and "
        if self.ui.speedMinLineEdit.text() != "":
            statCondition += "ps.STATS_DEFENSE > " + self.ui.speedMinLineEdit.text() + " and "
        if self.ui.speedMaxLineEdit.text() != "":
            statCondition += "ps.STATS_DEFENSE < " + self.ui.speedMinLineEdit.text() + " and "

        if len(statCondition) == 1:
            return "(1 = 1)"
        else:
            return statCondition[0:-5] + ")"

    def getStatOrder(self):
        statOrderBy = "\norder by ("
        startingLen = len(statOrderBy)
        if self.ui.hpCheckBox.isChecked():
            statOrderBy += "ps.STATS_HP + "
        if self.ui.attackCheckBox.isChecked():
            statOrderBy += "ps.STATS_ATTACK + "
        if self.ui.defenseCheckBox.isChecked():
            statOrderBy += "ps.STATS_DEFENSE + "
        if self.ui.specialAttackCheckBox.isChecked():
            statOrderBy += "ps.STATS_SP_ATTACK + "
        if self.ui.specialDefenseCheckBox.isChecked():
            statOrderBy += "ps.STATS_SP_DEFENSE + "
        if self.ui.speedCheckBox.isChecked():
            statOrderBy += "ps.STATS_SPEED + "

        if len(statOrderBy) != startingLen:
            statOrderBy = statOrderBy[0:-3] + ") desc;"
            return statOrderBy
        else:
            return ";"

    def getTypeCondition(self):
        statCondition = "("
        if self.ui.normalCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Normal\' or t.PKMN_TYPE2 = \'Normal\') and "
        if self.ui.fireCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Fire\' or t.PKMN_TYPE2 = \'Fire\') and "
        if self.ui.waterCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Water\' or t.PKMN_TYPE2 = \'Water\') and "
        if self.ui.grassCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Grass\' or t.PKMN_TYPE2 = \'Grass\') and "
        if self.ui.electricCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Electric\' or t.PKMN_TYPE2 = \'Electric\') and "
        if self.ui.iceCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Ice\' or t.PKMN_TYPE2 = \'Ice\') and "
        if self.ui.fightingCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Fighting\' or t.PKMN_TYPE2 = \'Fighting\') and "
        if self.ui.poisonCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Poison\' or t.PKMN_TYPE2 = \'Poison\') and "
        if self.ui.groundCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Ground\' or t.PKMN_TYPE2 = \'Ground\') and "
        if self.ui.flyingCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Flying\' or t.PKMN_TYPE2 = \'Flying\') and "
        if self.ui.psychicCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Psychic\' or t.PKMN_TYPE2 = \'Psychic\') and "
        if self.ui.bugCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Bug\' or t.PKMN_TYPE2 = \'Bug\') and "
        if self.ui.rockCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Rock\' or t.PKMN_TYPE2 = \'Rock\') and "
        if self.ui.ghostCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Ghost\' or t.PKMN_TYPE2 = \'Ghost\') and "
        if self.ui.darkCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Dark\' or t.PKMN_TYPE2 = \'Dark\') and "
        if self.ui.dragonCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Dragon\' or t.PKMN_TYPE2 = \'Dragon\') and "
        if self.ui.steelCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Steel\' or t.PKMN_TYPE2 = \'Steel\') and "
        if self.ui.fairyCheckBox.isChecked():
            statCondition += "(t.PKMN_TYPE1 = \'Fairy\' or t.PKMN_TYPE2 = \'Fairy\') and "

        if len(statCondition) == 1:
            return "(1 = 1)"
        else:
            return statCondition[0:-5] + ")"

class pokemonPopUpEvents(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = pp()
        self.ui.setupUi(self)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

def initUI(cur):
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = mainWindowEvents(MainWindow, cur)
    MainWindow.show()
    sys.exit(app.exec_())

def initDB():
    try:
        conn = mariadb.connect(
            user="root",
            password="1234",
            host="127.0.0.1",
            port=3306,
            database="pokedex"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn.cursor()

if __name__ == '__main__':
    cur = initDB()
    initUI(cur)