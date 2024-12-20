import matplotlib.pyplot as plt
import numpy as np
import collections.abc as c
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton,QGroupBox
from PyQt5.QtGui import QDoubleValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from converter.stl2array import stl2array
from view.cam_transform import CamTransform
from view.world_transform import WorldTransform

CANVAS2_XY_LIM : float = 160
AXIS_LENGTH : int = 24
COLOR_OBJ_3D : str = 'purple'
STL_OBJ_3D : str = 'tomcat'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.set_variables()    
        self.setWindowTitle("T1 Visao - Marcellus T. B. + Vinicius M. ")
        self.setGeometry(100, 100, 1280, 720)
        self.setup_ui()

    def set_variables(self):
        self.obj_3d = stl2array(STL_OBJ_3D)
        self.default_cam = np.eye(4) 
        self.cam = np.array([[  0.469   , -0.062   , 0.881  , -203.916],
                             [  -0.883  , -0.033   , 0.468  , -101.573],
                             [   0.     , -0.998   , -0.07  ,   20.5  ],
                             [   0.     ,  0.      , 0.     ,    1.   ]])
        self.px_base = 1280  
        self.px_altura = 720 
        self.dist_foc = 50 
        self.stheta = 0 
        self.ox = self.px_base/2 
        self.oy = self.px_altura/2 
        self.ccd = [36,24] 
        self.sx = self.px_base / self.ccd[0]
        self.sy = self.px_altura / self.ccd[1]

        self.projection_matrix = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0]])
        self.intr_param_matrix = np.array([[self.dist_foc * self.sx , self.dist_foc * self.stheta, self.ox],
                                           [0 , self.dist_foc * self.sy, self.oy],
                                           [0,0,1]])
        self.extr_param_matrix = self.cam
        
    def setup_ui(self):
        # Criar o layout de grade
        grid_layout = QGridLayout()

        # Criar os widgets
        line_edit_widget1 = self.create_world_widget("Ref Mundo")
        line_edit_widget2  = self.create_cam_widget("Ref Camera")
        line_edit_widget3  = self.create_intrinsic_widget("Params Instr")

        self.canvas = self.create_matplotlib_canvas()

        # Adicionar os widgets ao layout de grade
        grid_layout.addWidget(line_edit_widget1, 0, 0)
        grid_layout.addWidget(line_edit_widget2, 0, 1)
        grid_layout.addWidget(line_edit_widget3, 0, 2)
        grid_layout.addWidget(self.canvas, 1, 0, 1, 3)

        # Criar um widget para agrupar o botão de reset
        reset_widget = QWidget()
        reset_layout = QHBoxLayout()
        reset_widget.setLayout(reset_layout)

        # Criar o botão de reset vermelho
        reset_button = QPushButton("Reset")
        reset_button.setFixedSize(50, 30)  # Define um tamanho fixo para o botão (largura: 50 pixels, altura: 30 pixels)
        style_sheet = """
            QPushButton {
                color : white ;
                background: rgba(255, 127, 130,128);
                font: inherit;
                border-radius: 5px;
                line-height: 1;
            }
        """
        reset_button.setStyleSheet(style_sheet)
        reset_button.clicked.connect(self.reset_canvas)

        # Adicionar o botão de reset ao layout
        reset_layout.addWidget(reset_button)

        # Adicionar o widget de reset ao layout de grade
        grid_layout.addWidget(reset_widget, 2, 0, 1, 3)

        # Criar um widget central e definir o layout de grade como seu layout
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        
        # Definir o widget central na janela principal
        self.setCentralWidget(central_widget)

    def create_intrinsic_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['n_pixels_base: [px]', 'n_pixels_altura: [px]', 'ccd_x: [mm]', 'ccd_y: [mm]', 'dist_focal: [mm]', 's0: [px/mm]']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar Intrinseco")

        # Você deverá criar, no espaço reservado ao final, a função self.update_params_intrinsc ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_params_intrinsc(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget
    
    def create_world_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle [deg]):', 'Y(move):', 'Y(angle [deg]):', 'Z(move):', 'Z(angle [deg]):']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator() # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar Mundo")

        # Você deverá criar, no espaço reservado ao final, a função self.update_world ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_world(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_cam_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle [deg]):', 'Y(move):', 'Y(angle [deg]):', 'Z(move):', 'Z(angle [deg]):']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator() # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar Câmera")

        # Você deverá criar, no espaço reservado ao final, a função self.update_cam ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_cam(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_matplotlib_canvas(self):
        # Criar um widget para exibir os gráficos do Matplotlib
        canvas_widget = QWidget()
        canvas_layout = QHBoxLayout()
        canvas_widget.setLayout(canvas_layout)

        # Criar um objeto FigureCanvas para exibir o gráfico 2D
        self.fig1, self.ax1 = plt.subplots()
        self.ax1.set_title("Imagem")
        self.canvas1 = FigureCanvas(self.fig1)

        self.set_ax1_plot()
        obj_2d = self.projection_2d()
        self.ax1.plot(obj_2d[0,:],obj_2d[1,:])
        self.ax1.grid('True')
        self.ax1.set_aspect('equal')  
        canvas_layout.addWidget(self.canvas1)

        # Criar um objeto FigureCanvas para exibir o gráfico 3D
        self.fig2 = plt.figure()
        self.ax2 = self.fig2.add_subplot(111, projection='3d')

        self.set_ax2_plot(CANVAS2_XY_LIM)
        self.draw_default_cam(length=AXIS_LENGTH)
        self.draw_cam(length=AXIS_LENGTH)
        self.ax2.plot(self.obj_3d[0,:],self.obj_3d[1,:],self.obj_3d[2,:],COLOR_OBJ_3D)

        self.canvas2 = FigureCanvas(self.fig2)
        canvas_layout.addWidget(self.canvas2)

        # Retornar o widget de canvas
        return canvas_widget

    def set_ax1_plot(self):

        self.ax1.set_title("2D Projection")
        self.ax1.set_xlim([0,self.px_base])
        self.ax1.set_ylim([self.px_altura,0])


    def set_ax2_plot(self, lim_xy : float):
        self.ax2.set_title("3D VIEW")

        self.ax2.set_xlabel("X")
        self.ax2.set_xlim([-lim_xy,lim_xy])

        self.ax2.set_ylabel("Y")
        self.ax2.set_ylim([-lim_xy,lim_xy])

        self.ax2.set_zlabel("Z")
        self.ax2.set_zlim([-lim_xy,lim_xy])

    def draw_default_cam(self,length=3):
        # Plot vector of x-axis
        self.ax2.quiver(self.default_cam[0,-1], self.default_cam[1,-1], self.default_cam[2,-1],
                        self.default_cam[0,0], self.default_cam[1,0], self.default_cam[2,0],
                        color='red', pivot='tail', length=length)
        
        # Plot vector of y-axis
        self.ax2.quiver(self.default_cam[0,-1], self.default_cam[1,-1], self.default_cam[2,-1],
                        self.default_cam[0,1], self.default_cam[1,1], self.default_cam[2,1],
                        color='green', pivot='tail', length=length)
        # Plot vector of z-axis
        self.ax2.quiver(self.default_cam[0,-1], self.default_cam[1,-1], self.default_cam[2,-1],
                         self.default_cam[0,2], self.default_cam[1,2], self.default_cam[2,2],
                         color='blue', pivot='tail', length=length)

    def draw_cam(self,length=3):
        # Plot vector of x-axis
        self.ax2.quiver(self.cam[0,-1], self.cam[1,-1], self.cam[2,-1],
                        self.cam[0,0], self.cam[1,0], self.cam[2,0],
                        color='red', pivot='tail', length=length)
        
        # Plot vector of y-axis
        self.ax2.quiver(self.cam[0,-1], self.cam[1,-1], self.cam[2,-1],
                        self.cam[0,1], self.cam[1,1], self.cam[2,1],
                        color='green', pivot='tail', length=length)
        # Plot vector of z-axis
        self.ax2.quiver(self.cam[0,-1], self.cam[1,-1], self.cam[2,-1],
                         self.cam[0,2], self.cam[1,2], self.cam[2,2],
                         color='blue', pivot='tail', length=length)

    def update_params_intrinsc(self, line_edits : list[QLineEdit]) -> None:
        # ['n_pixels_base:', 'n_pixels_altura:', 'ccd_x:', 'ccd_y:', 'dist_focal:', 's0:']

        intr_values = self.intr_values(line_edits)

        self.px_base = intr_values[0]
        self.px_altura = intr_values[1]
        self.ccd[0] = intr_values[2]
        self.ccd[1] = intr_values[3]
        self.dist_foc = intr_values[4]
        self.stheta = intr_values[5]

        self.ox = self.px_base/2 
        self.oy = self.px_altura/2 
        self.sx = self.px_base / self.ccd[0]
        self.sy = self.px_altura / self.ccd[1]

        self.intr_param_matrix = np.array([[self.dist_foc * self.sx , self.dist_foc * self.stheta, self.ox],
                                           [0 , self.dist_foc * self.sy, self.oy],
                                           [0,0,1]])
        
        self.update_canvas()

    def update_world(self,line_edits : list[QLineEdit]):
        # labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']
        
        world_values = self.line_values(line_edits)
        world_transf = WorldTransform(*world_values)
        self.cam = world_transf.build_cam(self.cam)
        self.update_canvas()


    def update_cam(self,line_edits : list[QLineEdit]):
        # labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']

        cam_values = self.line_values(line_edits)
        cam_transf = CamTransform(*cam_values)
        self.cam = cam_transf.build_cam(self.cam)
        self.update_canvas()
    
    def line_values(self, line_edits : list[QLineEdit]) -> list[float | int]:
        values = []
        for i in range(0,6):
            read_input = line_edits[i].text()
            if len(read_input) != 0:
                try:
                    values.append(float(line_edits[i].text()))
                except:
                    values.append(0)
            else: 
                values.append(0)

        return values
    
    def intr_values(self, line_edits : list[QLineEdit]) -> list[float | int]:
        # ['n_pixels_base:', 'n_pixels_altura:', 'ccd_x:', 'ccd_y:', 'dist_focal:', 's0:']

        values = [self.px_base,
                  self.px_altura,
                  self.ccd[0],
                  self.ccd[1],
                  self.dist_foc,
                  self.stheta]
        
        for i in range(0,6):
            read_input = line_edits[i].text()
            if len(read_input) != 0:
                try:
                    values[i] = float(line_edits[i].text())
                except:
                    pass

        return values
    
    def projection_2d(self):
        w2c = CamTransform.inv_transf(self.cam)
        proj = self.intr_param_matrix @ self.projection_matrix @  w2c

        obj_2d = proj @ self.obj_3d

        if obj_2d[2,:].all() != 0:
           obj_2d = obj_2d / obj_2d[2,:]

        return obj_2d

    
    def update_canvas(self):

        plt.close('all')

        #UPDATE CANVAS1
        self.ax1.clear()
        self.set_ax1_plot()
        self.ax1.grid('True')
        self.ax1.set_aspect('equal')
        obj_2d = self.projection_2d()
        self.ax1.plot(obj_2d[0,:],obj_2d[1,:])
        self.canvas1.draw()

        #UPDATE CANVAS2
        self.ax2.clear()
        self.set_ax2_plot(CANVAS2_XY_LIM)
        self.draw_default_cam(length=AXIS_LENGTH)
        self.draw_cam(length=AXIS_LENGTH)
        self.ax2.plot(self.obj_3d[0,:],self.obj_3d[1,:],self.obj_3d[2,:],COLOR_OBJ_3D)
        self.canvas2.draw()

    def reset_canvas(self):
        self.set_variables()
        self.update_canvas()
        print("\nCanvas Resetado!\n")