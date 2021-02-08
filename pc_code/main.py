from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ListProperty
from kivy.event import EventDispatcher
import serial
import serial.tools.list_ports
#import time

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'multisamples', '0')


#Builder.load_file('apresentação.kv')

a = open('apresentacao.kv', 'r')
kv_string = a.read()
a.close()

root = Builder.load_string(kv_string)

py_serial = None

class Sw_status(EventDispatcher):
    #a = NumericProperty(1)
    sw_blue_change = BooleanProperty(False)
    sw_green_change = BooleanProperty(False)
    sw_red_change = BooleanProperty(False)
    label_status = NumericProperty(0)
    texto_conexao = StringProperty('[color=FF8C00] Desconectado [/color]')
    x = ListProperty()
    y = ListProperty()
    ch1 = StringProperty()
    ch2 = StringProperty()
    sw_nao_ler = BooleanProperty(True)

def callback(instance, value):
    print('My callback is call from', instance)
    print('and the a value changed to', value)
    #SwitchBlue.active = value


ins = Sw_status()
# ins.bind(a=callback)
ins.bind(sw_blue_change=callback)
ins.bind(sw_green_change=callback)
ins.bind(sw_red_change=callback)


a = '1'
b = '2'
c = '3'
a2 = a.encode('utf-8')
b2 = b.encode('utf-8')
c2 = c.encode('utf-8')

'''py_serial = serial.Serial('COM6', 9600, timeout=1, write_timeout=1)

a = '1'
a2 = a.encode('utf-8')

for i in range(10):
    char = py_serial.write(a2)
    print(a2)
    time.sleep(0.5)'''


class BLayout(BoxLayout, Screen):
    def __init__(self, **kwargs):
        super(BLayout, self).__init__(**kwargs)


class ImageReload(ButtonBehavior, Image):
    conexao = StringProperty()

    def __init__(self, **kwargs):
        super(ImageReload, self).__init__(**kwargs)
        self.source = 'Reload1.png'

    def on_press(self):
        self.source = 'Reload1_back.png'
        global py_serial

        if ins.label_status == 0:  #Primeira vez
            ins.texto_conexao = '[color=FF8C00] Conectando... [/color]'

            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                if "Arduino" in p.description:
                    print("This is an Arduino!")

            self.conexao = p[0]
            py_serial = serial.Serial(self.conexao, 9600, timeout=1, write_timeout=1)
            ins.label_status = 1
            ins.texto_conexao = '[color=00FFFF] Conectado (1ª vez) [/color]'
            print('Conectado 1ª vez')

        else:
            ins.texto_conexao = '[color=FF8C00] Destruindo... [/color]'
            py_serial.__del__()

            ins.texto_conexao = '[color=FF8C00] Destruido [/color]'
            ins.texto_conexao = '[color=FF8C00] Conectando... [/color]'

            py_serial = serial.Serial(self.conexao, 9600, timeout=1, write_timeout=1)
            ins.texto_conexao = '[color=00FFFF] Conectado [/color]'

            ins.sw_blue_change = False
            ins.sw_green_change = False
            ins.sw_red_change = False
            print('Reconexão')

    '''
    def conectar(self):
        global py_serial
        py_serial = serial.Serial('COM6', 9600, timeout=1, write_timeout=1)

    def destruir(self):
        global py_serial
        py_serial.__del__()

    def print_conectando(self):
        ins.texto_conexao = '[color=FF8C00] Conectando... [/color]'

    def print_conectado_pri(self):
        ins.texto_conexao = '[color=00FFFF] Conectado (1ª vez) [/color]'
    '''
    def on_release(self):
        self.source = 'Reload1.png'


class LabelStatus(Label):
    def __init__(self, **kwargs):
        super(LabelStatus, self).__init__(**kwargs)
        self.text = '[color=FF8C00] Conectando... [/color]'
        Clock.schedule_interval(lambda dt: self.change_text(), 0.1)
        
    def change_text(self):
        self.text = ins.texto_conexao


class SwitchBlue(Switch):
    led_aceso = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(SwitchBlue, self).__init__(**kwargs)
        Clock.schedule_interval(lambda dt: self.on_change_my(), 0.2)

    def on_change_my(self):
        global py_serial

        try:
            if ins.sw_blue_change == True:
                self.active = True

                if self.led_aceso == False:
                    char = py_serial.write(a2)
                    self.led_aceso = True

            else:
                self.active = False

                if self.led_aceso == True:
                    char = py_serial.write(a2)
                    self.led_aceso = False
        except AttributeError:
        # except Exception:
            ins.texto_conexao = '[color=FF0000] ERRO: Dispositivo não conectado [/color]'
            ins.sw_blue_change = False


class SwitchGreen(Switch):
    led_aceso = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(SwitchGreen, self).__init__(**kwargs)
        Clock.schedule_interval(lambda dt: self.on_change_my(), 0.2)

    def on_change_my(self):
        global py_serial

        try:
            if ins.sw_green_change == True:
                self.active = True

                if self.led_aceso == False:
                    char = py_serial.write(b2)
                    self.led_aceso = True
                    
            else:
                self.active = False

                if self.led_aceso == True:
                    char = py_serial.write(b2)
                    self.led_aceso = False
        except AttributeError:
            ins.texto_conexao = '[color=FF0000] ERRO: Dispositivo não conectado [/color]'
            ins.sw_green_change = False


class SwitchRed(Switch):
    led_aceso = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(SwitchRed, self).__init__(**kwargs)
        Clock.schedule_interval(lambda dt: self.on_change_my(), 0.2)

    def on_change_my(self):
        global py_serial

        try:
            if ins.sw_red_change == True:
                self.active = True

                if self.led_aceso == False:
                    char = py_serial.write(c2)
                    self.led_aceso = True
                    
            else:
                self.active = False

                if self.led_aceso == True:
                    char = py_serial.write(c2)
                    self.led_aceso = False
        except AttributeError:
            ins.texto_conexao = '[color=FF0000] ERRO: Dispositivo não conectado [/color]'
            ins.sw_red_change = False


class ImageButtonBlue(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButtonBlue, self).__init__(**kwargs)
        self.source = 'bbluepng2.png'

    def on_press(self):
        self.source = 'bbluepng_back2.png'

        #ins.a = 2
        if ins.sw_blue_change == True:
            ins.sw_blue_change = False
        else:
            ins.sw_blue_change = True

    def on_release(self):
        self.source = 'bbluepng2.png'
        #ins.a = 5
        # ins.sw_blue_change = False

    '''def clique(self):
        self.source = 'bbluepng_back2.png'''


class ImageButtonGreen(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButtonGreen, self).__init__(**kwargs)
        self.source = 'bgreenpng2.png'

    def on_press(self):
        self.source = 'bgreenpng_back2.png'

        if ins.sw_green_change == True:
            ins.sw_green_change = False
        else:
            ins.sw_green_change = True

    def on_release(self):
        self.source = 'bgreenpng2.png'


class ImageButtonRed(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButtonRed, self).__init__(**kwargs)
        self.source = 'bredpng2.png'

    def on_press(self):
        self.source = 'bredpng_back2.png'

        if ins.sw_red_change == True:
            ins.sw_red_change = False
        else:
            ins.sw_red_change = True

    def on_release(self):
        self.source = 'bredpng2.png'


class SwitchSensores(Switch):
    def __init__(self, **kwargs):
        super(SwitchSensores, self).__init__(**kwargs)
        Clock.schedule_interval(lambda dt: self.on_change_my(), 0.2)

    def on_change_my(self):
        if self.active == True:
            ins.sw_nao_ler = False
        else:
            ins.sw_nao_ler = True


class LabelAutoria(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Autor: Felipe Garcia \nGraduando em Eng. da Computação'


class LabelLDR(Label):
    # x = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Luminosidade ambiente: '
        Clock.schedule_interval(lambda dt: self.atualizar(), 0.2)

    def atualizar(self):
        if ins.sw_nao_ler == False:
            self.text = 'Luminosidade ambiente: ' + str(0.0) + '%'
        else:
            try:
                lumin = py_serial.readline()
                valor = lumin.decode('utf-8')

                listtemp = []
                for i in valor:
                    if i != '\n':
                        listtemp.append(i)

                print(listtemp)

                for i in listtemp:
                    if i != 'T':
                        ins.x.append(i)
                    else:
                        break

                print(ins.x)

                print('ins.x: ', ins.x)


                if len(ins.x) > 2:
                    ins.x.remove('L')
                    print(ins.x)
                    #ins.x.pop()

                    '''if ins.x[0] == 'T':
                        print(ins.x)'''

                    #ins.x.remove('L')
                    for i in ins.x:
                        ins.ch1 = ins.ch1 + i

                    print('ins.ch1', ins.ch1)

                    var = 0
                    y = 0
                    if len(ins.ch1) > 0:
                        var = int(ins.ch1)
                        y = 100 - ((100 / 1023) * var)
                        y = round(y, 2)

                    # print(y)

                    self.text = 'Luminosidade ambiente: ' + str(y) + '%'
                    listtemp.clear()
                    ins.x.clear()
                    ins.ch1 = ''
            except AttributeError:
                print('Não conectado (LDR Exception)')


class LabelLM35(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Temperatura ambiente: '
        Clock.schedule_interval(lambda dt: self.atualizar(), 0.2)
        
    def atualizar(self):
        if ins.sw_nao_ler == False:
            self.text = 'Temperatura ambiente: ' + str(0.0) + 'ºC'
        else:
            try:
                valorLido = py_serial.readline()
                valorLido = valorLido.decode('utf-8')

                print(valorLido)
                listtemp = []
                for i in valorLido:
                    if i != '\n':
                        listtemp.append(i)

                print('listtemp: ', listtemp)

                if len(listtemp) > 2:

                    c = 0
                    a = []
                    for i in listtemp:
                        if i == 'T':
                            a = listtemp[c:]
                            break
                        c += 1

                    ins.y = a
                    ins.y.pop()
                    print('ins.y: ', ins.y)

                    if len(ins.y) > 0:
                        #ins.y.pop(0)
                        ins.y.remove('T')
                        print(ins.y)

                        for i in ins.y:
                            ins.ch2 = ins.ch2 + i

                        print(ins.ch2)

                        var = 0
                        temperatura = 0
                        if len(ins.ch2) > 0:
                            var = int(ins.ch2)
                            temperatura = (5 / 1023) * var
                            temperatura = (temperatura * 100)
                            temperatura = round(temperatura, 2)

                        # print(temperatura)

                        self.text = 'Temperatura ambiente: ' + str(temperatura) + 'ºC'
                        listtemp.clear()
                        ins.y.clear()
                        ins.ch2 = ''
            except AttributeError:
                print('Não conectado (LM35 Exception)')

class teste_pyserial(App):
    def build(self):
        self.title = 'EngAmostra'
        self.icon = 'Icone2.png'
        return BLayout()


if __name__== '__main__':
    teste_pyserial().run()
