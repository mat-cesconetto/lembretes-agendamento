import sys
import datetime
import app1
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QDateEdit, QHBoxLayout, QLabel, QTimeEdit
from PyQt6.QtGui import QIcon, QPixmap, QCursor

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Agenda')
        self.setWindowIcon(QIcon('venv/src/calendar.ico'))
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.resize(1000, 700)
        
        # Título da aplicação
        title = QLabel('Agenda')
        title.setObjectName('title')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop)
        title.setContentsMargins(0, 0, 0, 0)
        
        # Linha de entrada para nome e descrição do compromisso
        linha1 = QHBoxLayout()
        self.input_padrao('Nome do Compromisso', 'input_nome', linha1)
        self.input_padrao('Descrição do Compromisso', 'input_desc', linha1)
        layout.addLayout(linha1)

        # Linha de entrada para data e horário do compromisso
        linha2 = QHBoxLayout()
        self.data_tempo('Data do Compromisso', 'input_data', linha2, tempo=False)
        self.data_tempo('Hora de Início', 'input_hora_inicial', linha2, tempo=True)
        self.data_tempo('Hora de Término', 'input_hora_final', linha2, tempo=True)
        layout.addLayout(linha2)

        # Botão para marcar o compromisso
        linha3 = QHBoxLayout()
        button = QPushButton('Marcar Compromisso', clicked=self.marcar)
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        linha3.addWidget(button)
        layout.addLayout(linha3)

        # Linha para exibir compromissos
        linha4 = QHBoxLayout()
        label = QLabel('Seus Compromissos')
        imagem = QPixmap('venv/src/reload.png')
        imagem_redimensionada = imagem.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image = QLabel()
        self.image.setPixmap(imagem_redimensionada)
        self.image.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.image.mousePressEvent = self.on_click
        linha4.addWidget(label)
        linha4.addWidget(self.image)
        linha4.addStretch()
        
        # Grupo que reúne a linha 4 com a text edit para exibir compromissos
        grupo = QVBoxLayout()
        grupo.addLayout(linha4)
        self.textao = QTextEdit()
        grupo.addWidget(self.textao)
        layout.addLayout(grupo)

    def input_padrao(self, titulo, nome, linha):
        """
        Cria campos de entrada padrão (QLineEdit) com um título.

        Args:
            titulo (str): Texto do título do campo de entrada.
            nome (str): Nome do atributo para armazenar o campo de entrada.
            linha (QHBoxLayout): Layout onde o campo será adicionado.
        """
        input_layout = QVBoxLayout()
        label = QLabel(titulo)
        input = QLineEdit()
        setattr(self, nome, input)
        input_layout.addWidget(label)
        input_layout.addWidget(input)
        linha.addLayout(input_layout)

    def data_tempo(self, titulo, nome, linha, tempo=False):
        """
        Cria campos de entrada para data (QDateEdit) e hora (QTimeEdit) com um título.

        Args:
            titulo (str): Texto do título do campo de entrada.
            nome (str): Nome do atributo para armazenar o campo de entrada.
            linha (QHBoxLayout): Layout onde o campo será adicionado.
            tempo (bool): Define se o campo será de tempo (True) ou data (False).
        """
        input_layout = QVBoxLayout()
        label = QLabel(titulo)
        if tempo:
            comp = QTimeEdit()
            comp.setDisplayFormat('HH:mm')
        else:
            comp = QDateEdit()
            comp.setCalendarPopup(True)
            comp.setDate(QDate.currentDate())
        setattr(self, nome, comp)
        input_layout.addWidget(label)
        input_layout.addWidget(comp)
        linha.addLayout(input_layout)

    def marcar(self):
        """
        Obtém os dados dos campos de entrada e cria um compromisso no Google Calendar.
        """
        titulo = self.input_nome.text()
        descricao = self.input_desc.text()
        data = datetime.datetime.strptime(self.input_data.text(), '%d/%m/%Y').strftime('%Y-%m-%d')
        hora_inicial = self.input_hora_inicial.text() + ':00-03:00'
        hora_final = self.input_hora_final.text() + ':00-03:00'
        inicio = data + 'T' + hora_inicial
        fim = data + 'T' + hora_final
        app1.main(inicio, fim, titulo, descricao)

    def on_click(self, event):
        """
        Atualiza a lista de compromissos quando a imagem de reload é clicada.
        """
        self.textao.setText(app1.proximos())

# Inicializa a aplicação PyQt
app = QApplication(sys.argv)
app.setStyleSheet('''
    #title {
        font-size: 45px;
        margin-bottom: 20px;
        font-family: Georgia, serif;
    }
    QLabel {
        font-size: 25px;
        margin-top: 30px;
    }
    QLineEdit, QDateEdit, QTimeEdit, QPushButton, QTextEdit {
        font-size: 20px;
        padding: 5px;
    }
    * {
        font-family: "Gill Sans", sans-serif;
''')

# Cria e exibe a janela principal
janela = MyApp()
janela.show()
app.exec()
