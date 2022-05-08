from selenium import webdriver
from bs4 import BeautifulSoup
from asyncio.windows_events import NULL
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QDialog, QLineEdit, QTableWidgetItem, QLabel, QErrorMessage
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtCore import Qt
from UI.mainWindow import Ui_MainWindow as mw
from UI.pokemonPopup import Ui_Dialog as pp
from UI.pokemonPopupMainMenu import Ui_MainWindow as ppmw
import sys
import requests
import urllib.request
import time
import os
import mariadb
import PyQt5

class mainWindowEvents(QMainWindow):
    def __init__(self, MainWindow, cur):
        super().__init__()
        self.ui = mw()
        self.ui.setupUi(MainWindow)
        self.cur = cur.cursor()
        self.conn = cur
        self.ui.searchResultsTableWidget.verticalHeader().setVisible(False)
        self.ui.searchResultsTableWidget.horizontalHeader().setVisible(False)
        self.ui.pushButton.clicked.connect(self.search)
        self.ui.createButton.clicked.connect(self.create)
        self.ui.searchResultsTableWidget.cellClicked.connect(self.searchCellClicked)
        self.ui.deletePokemonButton.setVisible(False)
        self.ui.updateButton.setVisible(False)
        self.ui.createPokemonButton.setVisible(False)

        self.ui.createPokemonButton.clicked.connect(self.createPokemon)
        self.ui.updateButton.clicked.connect(self.updatePokemon)
        self.ui.deletePokemonButton.clicked.connect(self.deletePokemon)

    def createPokemon(self):
        print("create pokemon")
        isgood = True
        if self.ui.pokemonNameLabel.text() == "" :
            isgood = False
        if self.ui.idLabel.text() == "":
            isgood = False
        if self.ui.attackLabel.text() == "":
            isgood = False
        if self.ui.hpLabel.text() == "":
            isgood = False
        if self.ui.defenseLabel.text() == "":
            isgood = False
        if self.ui.specialAttackLabel.text() == "":
            isgood = False
        if self.ui.specialDefenseLabel.text() == "":
            isgood = False
        if self.ui.speedLabel.text() == "":
            isgood = False
        if self.ui.weightLabel.text() == "":
            isgood = False
        if self.ui.evolutionIDLabel.text() == "":
            isgood = False
        if self.ui.evolvingIDLabel.text() == "":
            isgood = False
        if self.ui.type1LineEdit.text() == "":
            isgood = False
        if self.ui.type2LineEdit.text() == "":
            isgood = False
        if isgood == False:
            print("error man")
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.showMessage('Fill in every field')
            error_dialog.exec_()
            return
            # Put an error label
        self.cur.execute(f"select exists (select * from pokemoninfo where PKMN_ID = {self.ui.idLabel.text()[1:]});")
        data = self.cur.fetchall()
        if data[0][0] == 1:
            print("error man")
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.showMessage('ID is already in database')
            error_dialog.exec_()
            return
        
        self.cur.execute(f"INSERT INTO pokemoninfo (PKMN_ID, PKMN_NAME) VALUES ({self.ui.idLabel.text()[1:]}, \'{self.ui.pokemonNameLabel.text()}\');")
        self.cur.execute(f"INSERT INTO pokemonweight (PKMN_ID, PKMN_WEIGHT) VALUES({self.ui.idLabel.text()[1:]}, {self.ui.weightLabel.text()});")
        self.cur.execute(f"INSERT INTO regionfound(PKMN_REGION, PKMN_ID) VALUES(\'{self.ui.regionLineEdit.text()}\',{self.ui.idLabel.text()[1:]});")
        self.cur.execute(f"INSERT INTO typechart (PKMN_TYPE1, PKMN_TYPE2, PKMN_ID) VALUES (\'{self.ui.type1LineEdit.text()}\',\'{self.ui.type2LineEdit.text()}\',{self.ui.idLabel.text()[1:]});")
        sHP = int(self.ui.hpLabel.text())
        sAttack = int(self.ui.attackLabel.text())
        sDefense = int(self.ui.defenseLabel.text())
        sSpAttack = int(self.ui.specialAttackLabel.text())
        sSpDefense = int(self.ui.specialDefenseLabel.text())
        sSpeed = int(self.ui.speedLabel.text())
        sTotal = sHP + sAttack + sDefense + sSpAttack + sSpDefense + sSpeed
        self.cur.execute(f"insert into PokemonStats(PKMN_ID, STATS_TOTAL, STATS_HP, STATS_ATTACK, STATS_DEFENSE, STATS_SP_ATTACK, STATS_SP_DEFENSE, STATS_SPEED) VALUES({self.ui.idLabel.text()[1:]},{sTotal},{sHP},{sAttack},{sDefense},{sSpAttack},{sSpDefense},{sSpeed});")
        self.cur.execute(f"INSERT INTO Evolutions(PKMN_ID, PKMN_NAME, EVOLUTION_ID, EVOLVING_ID)  VALUES({self.ui.idLabel.text()[1:]},\'{self.ui.pokemonNameLabel.text()}\',{self.ui.evolutionIDLabel.text()},{self.ui.evolvingIDLabel.text()});")
        self.conn.commit()


    def updatePokemon(self):
        self.cur.execute(f"select exists (select * from pokemoninfo where PKMN_ID = {self.ui.idLabel.text()[1:]});")
        data = self.cur.fetchall()
        if data[0][0] == 0:
            print("error man")
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.showMessage('Use a valid ID to update')
            error_dialog.exec_()
            return
        isgood = True
        if self.ui.pokemonNameLabel.text() == "" :
            isgood = False
        if self.ui.idLabel.text() == "":
            isgood = False
        if self.ui.attackLabel.text() == "":
            isgood = False
        if self.ui.hpLabel.text() == "":
            isgood = False
        if self.ui.defenseLabel.text() == "":
            isgood = False
        if self.ui.specialAttackLabel.text() == "":
            isgood = False
        if self.ui.specialDefenseLabel.text() == "":
            isgood = False
        if self.ui.speedLabel.text() == "":
            isgood = False
        if self.ui.weightLabel.text() == "":
            isgood = False
        if self.ui.evolutionIDLabel.text() == "":
            isgood = False
        if self.ui.evolvingIDLabel.text() == "":
            isgood = False
        if self.ui.type1LineEdit.text() == "":
            isgood = False
        if self.ui.type2LineEdit.text() == "":
            isgood = False
        if isgood == False:
            print("error man")
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.showMessage('Fill in every field')
            error_dialog.exec_()
            return
        self.cur.execute(f"UPDATE pokemonweight SET PKMN_WEIGHT = {self.ui.weightLabel.text()} WHERE PKMN_ID = {self.ui.idLabel.text()[1:]}")
        self.cur.execute(f"UPDATE regionfound SET PKMN_REGION = \'{self.ui.regionLineEdit.text()}\' WHERE PKMN_ID = {self.ui.idLabel.text()[1:]}")
        self.cur.execute(f"UPDATE pokemoninfo SET PKMN_NAME = \'{self.ui.pokemonNameLabel.text()}\' WHERE PKMN_ID = {self.ui.idLabel.text()[1:]}")
        self.cur.execute(f"UPDATE typechart SET PKMN_TYPE1 = \'{self.ui.type1LineEdit.text()}\', PKMN_TYPE2 = \'{self.ui.type2LineEdit.text()}\' WHERE PKMN_ID = {self.ui.idLabel.text()[1:]}")
        sHP = int(self.ui.hpLabel.text())
        sAttack = int(self.ui.attackLabel.text())
        sDefense = int(self.ui.defenseLabel.text())
        sSpAttack = int(self.ui.specialAttackLabel.text())
        sSpDefense = int(self.ui.specialDefenseLabel.text())
        sSpeed = int(self.ui.speedLabel.text())
        sTotal = sHP + sAttack + sDefense + sSpAttack + sSpDefense + sSpeed
        self.cur.execute(f"UPDATE pokemonstats SET STATS_TOTAL = {sTotal}, STATS_HP = {sHP}, STATS_ATTACK = {sAttack}, STATS_DEFENSE = {sDefense}, STATS_SP_ATTACK = {sSpAttack}, STATS_SP_DEFENSE = {sSpDefense}, STATS_SPEED = {sSpeed} WHERE PKMN_ID = {self.ui.idLabel.text()[1:]}")
        evolv = self.ui.evolvingIDLabel.text()
        evolu = self.ui.evolutionIDLabel.text()
        if evolv == "None":
            evolv = "NULL"
        if evolu == "None":
            evolu = "NULL"
        self.cur.execute(f"UPDATE evolutions SET PKMN_NAME = \'{self.ui.pokemonNameLabel.text()}\', EVOLUTION_ID = {evolu}, EVOLVING_ID = {evolv} WHERE PKMN_ID = {self.ui.idLabel.text()[1:]}")
        self.conn.commit()

    def deletePokemon(self):
        if not self.ui.idLabel.text()[1:].isdigit():
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.showMessage('Enter an ID to delete')
            error_dialog.exec_()
            return
        self.cur.execute(f"DELETE FROM pokemonweight WHERE PKMN_ID = {self.ui.idLabel.text()[1:]}")
        self.cur.execute(f"DELETE FROM regionfound WHERE PKMN_ID = {self.ui.idLabel.text()[1:]}")
        self.cur.execute(f"DELETE FROM pokemonstats WHERE PKMN_ID = {self.ui.idLabel.text()[1:]}")
        self.cur.execute(f"DELETE FROM typechart WHERE PKMN_ID = {self.ui.idLabel.text()[1:]}")
        self.cur.execute(f"DELETE FROM evolutions WHERE PKMN_ID = {self.ui.idLabel.text()[1:]}")
        self.cur.execute(f"DELETE FROM pokemoninfo WHERE PKMN_ID = {self.ui.idLabel.text()[1:]}")
        self.conn.commit()
        print("delete pokemon")
        self.ui.pokemonNameLabel.setText("")
        self.ui.pokemonNameLabel.setFont(QFont('MS Shell Dlg 2', 16))
        self.ui.idLabel.setText("")
        self.ui.attackLabel.setText("")
        self.ui.hpLabel.setText("")
        self.ui.defenseLabel.setText("")
        self.ui.specialAttackLabel.setText("")
        self.ui.specialDefenseLabel.setText("")
        self.ui.speedLabel.setText("")
        self.ui.totalLabel.setText("")
        self.ui.weightLabel.setText("")
        self.ui.createPokemonButton.setVisible(False)
        self.ui.updateButton.setVisible(False)
        self.ui.deletePokemonButton.setVisible(False)
        self.ui.evolvesFromPictureLabel.setPixmap(QPixmap())
        self.ui.pokemonPictureLabel.setPixmap(QPixmap())
        self.ui.evolvesToPictureLabel.setPixmap(QPixmap())
        self.ui.type1LineEdit.setText("")
        self.ui.type2LineEdit.setText("")
        self.ui.regionLineEdit.setText("")
        self.ui.region2LineEdit.setText("")
        self.ui.evolvingIDLabel.setText("")
        self.ui.evolutionIDLabel.setText("")

    def create(self):
        self.ui.pokemonNameLabel.setText("")
        self.ui.pokemonNameLabel.setFont(QFont('MS Shell Dlg 2', 16))
        self.ui.idLabel.setText("")
        self.ui.attackLabel.setText("")
        self.ui.hpLabel.setText("")
        self.ui.defenseLabel.setText("")
        self.ui.specialAttackLabel.setText("")
        self.ui.specialDefenseLabel.setText("")
        self.ui.speedLabel.setText("")
        self.ui.totalLabel.setText("")
        self.ui.weightLabel.setText("")
        self.ui.createPokemonButton.setEnabled(True)
        self.ui.createPokemonButton.setVisible(True)
        self.ui.updateButton.setVisible(False)
        self.ui.deletePokemonButton.setVisible(False)
        self.ui.evolvesFromPictureLabel.setPixmap(QPixmap())
        self.ui.pokemonPictureLabel.setPixmap(QPixmap())
        self.ui.evolvesToPictureLabel.setPixmap(QPixmap())
        self.ui.type1LineEdit.setText("")
        self.ui.type2LineEdit.setText("")
        self.ui.regionLineEdit.setText("")
        self.ui.region2LineEdit.setText("")
        self.ui.evolvingIDLabel.setText("")
        self.ui.evolutionIDLabel.setText("")
        

    def searchCellClicked(self, row, col):
        item = self.ui.searchResultsTableWidget.item(row, col)
        pkmn_id = self.ui.searchResultsTableWidget.item(row, 0).text()
        executeString = f"""
select p.PKMN_ID, p.PKMN_NAME, t.PKMN_TYPE1, t.PKMN_TYPE2, ps.STATS_TOTAL, ps.STATS_HP, ps.STATS_ATTACK, ps.STATS_DEFENSE, ps.STATS_SP_ATTACK, ps.STATS_SP_DEFENSE, ps.STATS_SPEED, pw.PKMN_WEIGHT, r.PKMN_REGION, e.EVOLUTION_ID, e.EVOLVING_ID
from pokemoninfo as p
join pokemonstats as ps on p.PKMN_ID = ps.PKMN_ID
join pokemonweight as pw on p.PKMN_ID = pw.PKMN_ID
join regionfound as r on p.PKMN_ID = r.PKMN_ID
join evolutions as e on p.PKMN_ID = e.PKMN_ID
join typechart as t on p.PKMN_ID = t.PKMN_ID
where (p.PKMN_ID = {pkmn_id})"""

        self.cur.execute(executeString)
        data = self.getQuery()

        download = str(data[0]["PKMN_NAME"])
        url_image = webScraper(download)

        image = QImage()
        image.loadFromData(requests.get(url_image).content)
        self.ui.pokemonPictureLabel.setAlignment(Qt.AlignCenter)
        self.ui.pokemonPictureLabel.setPixmap(QPixmap(image))
        executeString2 = f"select EVOLUTION_ID from evolutions where (PKMN_ID = {pkmn_id});"
        self.cur.execute(executeString2)
        evolutions = self.getQuery()

        print(evolutions[0]['EVOLUTION_ID']) #can remove when done testing

        if evolutions[0]['EVOLUTION_ID'] is not None and int(pkmn_id) <= 60:
            executeString3 = f"select PKMN_ID from evolutions where EVOLUTION_ID = {evolutions[0]['EVOLUTION_ID']} order by PKMN_ID"
            self.cur.execute(executeString3)
            order = self.getQuery()
            print(order) #Can remove when done testing


            if order[0]['PKMN_ID'] == data[0]["PKMN_ID"]:
                download = "black screen"
                url_image = webScraper(download)
                image = QImage()
                image.loadFromData(requests.get(url_image).content)
                self.ui.evolvesToPictureLabel.setAlignment(Qt.AlignCenter)
                self.ui.evolvesToPictureLabel.setPixmap(QPixmap(image))

                executeString4 = f"select PKMN_NAME from pokemoninfo where (PKMN_ID = {order[1]['PKMN_ID']})"
                self.cur.execute(executeString4)
                UpperName = self.getQuery()
                url_image = webScraper(UpperName[0]["PKMN_NAME"])
                image2 = QImage()
                image2.loadFromData(requests.get(url_image).content)
                self.ui.evolvesFromPictureLabel.setPixmap(QPixmap(image2))

            elif order[1]['PKMN_ID'] == data[0]["PKMN_ID"]:
                executeString5 = f"select PKMN_NAME from pokemoninfo where (PKMN_ID = {order[0]['PKMN_ID']})"
                self.cur.execute(executeString5)
                lowerName = self.getQuery()
                url_image = webScraper(lowerName[0]["PKMN_NAME"])
                image = QImage()
                image.loadFromData(requests.get(url_image).content)
                self.ui.evolvesToPictureLabel.setPixmap(QPixmap(image))

                executeString5 = f"select PKMN_NAME from pokemoninfo where (PKMN_ID = {order[2]['PKMN_ID']})"
                self.cur.execute(executeString5)
                higherName = self.getQuery()
                url_image = webScraper(higherName[0]["PKMN_NAME"])
                image = QImage()
                image.loadFromData(requests.get(url_image).content)
                self.ui.evolvesFromPictureLabel.setPixmap(QPixmap(image))
            try:
                if order[2]['PKMN_ID'] == data[0]["PKMN_ID"]:
                    download = "black screen"
                    url_image = webScraper(download)
                    image = QImage()
                    image.loadFromData(requests.get(url_image).content)
                    self.ui.evolvesFromPictureLabel.setAlignment(Qt.AlignCenter)
                    self.ui.evolvesFromPictureLabel.setPixmap(QPixmap(image))

                    executeString7 = f"select PKMN_NAME from pokemoninfo where (PKMN_ID = {order[1]['PKMN_ID']})"
                    self.cur.execute(executeString7)
                    middle = self.getQuery()
                    url_image = webScraper(middle[0]["PKMN_NAME"])
                    image = QImage()
                    image.loadFromData(requests.get(url_image).content)
                    self.ui.evolvesToPictureLabel.setAlignment(Qt.AlignCenter)
                    self.ui.evolvesToPictureLabel.setPixmap(QPixmap(image))

            except:
                print("Error for the big pokemon")

        self.ui.createPokemonButton.setVisible(False)
        self.ui.updateButton.setVisible(True)
        self.ui.deletePokemonButton.setVisible(True)

        self.ui.pokemonNameLabel.setText(str(data[0]["PKMN_NAME"]))
        self.ui.pokemonNameLabel.setFont(QFont('MS Shell Dlg 2', 16))
        self.ui.idLabel.setText("#" + str(data[0]["PKMN_ID"]))
        self.ui.attackLabel.setText(str(data[0]["STATS_ATTACK"]))
        self.ui.hpLabel.setText(str(data[0]["STATS_HP"]))
        self.ui.defenseLabel.setText(str(data[0]["STATS_DEFENSE"]))
        self.ui.specialAttackLabel.setText(str(data[0]["STATS_SP_ATTACK"]))
        self.ui.specialDefenseLabel.setText(str(data[0]["STATS_SP_DEFENSE"]))
        self.ui.speedLabel.setText(str(data[0]["STATS_SPEED"]))
        self.ui.totalLabel.setText(str(data[0]["STATS_TOTAL"]))
        self.ui.weightLabel.setText(str(data[0]["PKMN_WEIGHT"]))
        self.ui.evolutionIDLabel.setText(str(data[0]["EVOLUTION_ID"]))
        self.ui.evolvingIDLabel.setText(str(data[0]["EVOLVING_ID"]))

        if data[0]['PKMN_TYPE1'] != 'NULL':
            self.ui.type1LineEdit.setText(str(data[0]["PKMN_TYPE1"]))
        if data[0]['PKMN_TYPE2'] != 'NULL':
            self.ui.type2LineEdit.setText(str(data[0]['PKMN_TYPE2']))
        self.ui.regionLineEdit.setText(str(data[0]['PKMN_REGION']))

    def search(self):
        #print("search")
        pkmn_id = self.ui.idSearchLineEdit.text()
        pkmn_name = '\'' + str(self.ui.nameSearchLineEdit.text()) + '\''
        #print(pkmn_name)
        if pkmn_name == '' or pkmn_name == '\'\'':
            pkmn_name = '\'\' or 1 = 1'
        if pkmn_id == '':
            pkmn_id = '\'\' or 1 = 1'
        pkmn_id += ")"
        pkmn_name += ")"
        #print(pkmn_name, pkmn_id)

        statOrder = self.getStatOrder()
        statCondition = self.getStatCondition()
        typeCondition = self.getTypeCondition()
        regionCondition = self.getRegionCondition()

        executeString = f"""
select p.PKMN_ID, p.PKMN_NAME
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
        print(executeString)
        self.cur.execute(executeString)
        result = self.cur.fetchall()
        #data = self.getQuery()
        print(result)
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
    # def random(self):
    #     print("random")

    def getQuery(self):
        row_headers=[x[0] for x in self.cur.description]
        rv = self.cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        print(json_data)
        return json_data

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

def webScraper(download):
    site = 'https://www.google.com/search?tbm=isch&q=' + download

    htmldata = getdata(site)
    soup = BeautifulSoup(htmldata, 'html.parser')
    List = []
    for item in soup.find_all('img'):
        List.append(item['src'])

    url_image = List[1]
    return url_image


def getdata(url):
    r = requests.get(url)
    return r.text


def initUI(cur):
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = mainWindowEvents(MainWindow, cur)
    MainWindow.show()
    sys.exit(app.exec_())

def initDB():
    try:
        #conn = mariadb.connect(
        #    user="root",
        #    password="1234",
        #    host="127.0.0.1",
        #    port=3306,
        #    database="pokedex"
        #)
        conn = mariadb.connect(
           user="root",
           password="Jiddo123",
           host="127.0.0.1",
           port=3306,
           database="pokedex"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn

if __name__ == '__main__':
    cur = initDB()
    initUI(cur)