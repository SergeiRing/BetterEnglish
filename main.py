#****** Imports ******#

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
import random
from conventor import convent, fm
#----------------------------------#

#****** Settings Window ******#
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 700)
from kivy.core.window import Window
Window.clearcolor = (.16, .16, .16, 0)
#--------------------------------------#

#****** Styles ******#
Builder.load_string("""
#: import Window kivy.core.window.Window
<MyButton@Button>:
    size_hint_y:None
    height:Window.height/2

<MainScreen>:
    BoxLayout:
        orientation:'vertical'
        padding:(20)
        AnchorLayout:
            size_hint:(1, .4)
            anchor_x:'center'
            anchor_y:'top'
            Label:
                text:"BetterEnglish"
                font_name:'Fonts/Bauhaus93'
                font_size:50
                size_hint:(.5, .2)
                focus: False
        AnchorLayout:
            size_hint:(1, .3)
            anchor_x:'center'
            anchor_y:'top'
            Label:
                text:root.lableText
                font_name:'Fonts/Bauhaus93'
                font_size:root.lableSize
                size_hint:(.5, .2)
                color:(0, 0, 0, 1)     
        TextInput:
            size_hint:(1, .58)
            font_name:'Fonts/Moscow'
            font_size:20
            focus:True
            multiline: False
            text:root.inputText
            on_text_validate:root.brains(self.text)
        AnchorLayout:
            size_hint:(1, .02)
            anchor_x:'right'
            anchor_y :'bottom'
            Label:
                text:"Powered by lazyProger™"
                size_hint:(.3, .2)
                font_name:'Fonts/Bauhaus93'
                font_size:18


<SettingsScreen>:
    BoxLayout:
        orientation:'vertical'
        AnchorLayout:
            size_hint:(1, .2)
            anchor_x:'center'
            anchor_y:'center'
            Label:
                font_size:50
                font_name:'Fonts/Dominican'
                text:'Choose Dictionary'
        ScrollView:
            size_hint:(1, .6)
            BoxLayout:
                size_hint_y:None
                height:Window.height
                MyBoxLayout:
                    orientation:'vertical'
                    size_hint:(1, 1)
        AnchorLayout:
            padding:10
            anchor_x:'left'
            anchor_y:'center'
            size_hint:(1, .2)
            Button:
                text:"OK"
                size_hint:(.3, .4)
                font_size:30
                color:(0,0,0, 1)                
                background_color:(255, 255, 255, 255)
                font_name:'Fonts/Bauhaus93'
                on_press:root.manager.current='main'

""")
#-----------------------------------------------------#

#****** MyBoxLayout for ScrollView ******#
class MyBoxLayout(BoxLayout):
    files = []
    def checkBox(self, checkbox, value):
        if value:
            self.files.append(checkbox.id)
        else:
            self.files.pop(self.files.index(checkbox.id))

    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        all_files = fm.load('UserDictionaries')
        for file in all_files:
            b = GridLayout(cols=2)
            b.add_widget(Label(text=str(file.replace('.txt', ''))))
            cb = CheckBox(id=file)
            cb.bind(active=self.checkBox)
            b.add_widget(cb)
            self.add_widget(b)
#---------------------------------------------------------------------#


#****** Main Class ******#
class MainScreen(Screen):
    new = False
    lableText = StringProperty('')
    inputText = StringProperty('')
    lableSize = NumericProperty(40)
    def open_modalView(self, liist):
        view = ModalView(size_hint=(None, None), size=(400, 400), auto_dismiss=False)
        al = AnchorLayout(size=(400, 50), anchor_x='right', anchor_y='top')
        al_2 = AnchorLayout(size_hint=(None, None), size=(390, 350), anchor_x='left', anchor_y='bottom')
        vma = TextInput(size_hint=(None, None), size=(388, 300), readonly=True, font_size=20)
        for i in liist:
            vma.text+=i+'\n'
        al_2.add_widget(vma)
        al.add_widget(Button(size_hint=(.1, .1), on_press=view.dismiss, font_size=30, font_name='Fonts/Bauhaus93', text='+', background_color=(.16, .16, .16, 0)))
        view.add_widget(al)
        view.add_widget(al_2)
        view.open()
    def search_word(self, prevWords):
        self.word = random.choice(self.prevWords)
        prevWords.remove(self.word)
        length = str(self.word.keys()).replace('dict_keys([\'', '').replace('dict_keys([\"', '').replace('\'])', '').replace('"])', '')
        if len(length)>=38:
            self.lableSize=33
        return self.word
    def brains(self, text):
        if self.new == False:
            self.test_list = []
            self.words = convent(MyBoxLayout().files)
            self.again_or_no = 'no'
            self.word = '' # Текущее слово
            self.total = 0 # Переменная для выведения результата
            self.all_words = len(self.words) # Переменная для хранения кол-ва всех слов
            self.prevWords = [] # Оставшиеся слова
            for i in range(len(self.words)):   # Наполнение массива prevWords элементами массива words
                self.prevWords.append(self.words[i])
            self.new = True
        self.inputText = text
        if self.prevWords != []:
            if self.lableText == '':
                self.word = self.search_word(self.prevWords)
                self.key = str(self.word.keys()).replace('dict_keys([\'', '').replace('dict_keys([\"', '').replace('\'])', '').replace('"])', '')
                self.lableText += (self.key)
            else:
                if self.word[self.key] in self.inputText:
                    self.total += 1
                    self.test_list.append('{}({})-True'.format(self.key, self.word[self.key]))
                    self.word = self.search_word(self.prevWords)
                    self.key = str(self.word.keys()).replace('dict_keys([\'', '').replace('dict_keys([\"', '').replace('\'])', '').replace('"])', '')
                    self.lableText = (self.key)
                    self.inputText=''
                else:
                    self.test_list.append('{}({})-False'.format(self.key, self.word[self.key]))
                    self.word = self.search_word(self.prevWords)
                    self.key = str(self.word.keys()).replace('dict_keys([\'', '').replace('dict_keys([\"', '').replace('\'])', '').replace('"])', '')
                    self.lableText = self.key
                    self.inputText=''
        else:
            if self.again_or_no == 'no':
                try:
                    if self.word[self.key] in self.inputText:
                        self.total += 1
                        self.test_list.append('{}({})-True'.format(self.key, self.word[self.key]))
                    else:
                        self.test_list.append('{}({})-False'.format(self.key, self.word[self.key]))
                    self.lableText = 'Result: {}/{}'.format(self.total, self.all_words)
                    self.again_or_no = 'again'
                    self.open_modalView(self.test_list)
                except:
                    self.labelText = 'You haven\'t got any words :('
            else:
               self.inputText = ''
               self.lableText=''
               self.again_or_no = 'no'
               self.total = 0
               self.new = False
               for i in range(len(self.words)):
                   self.prevWords.append(self.words[i])

#****** Screen 'Choosing Dictionaries' ******#
class SettingsScreen(Screen):
    pass
#---------------------------------------------#

#****** Manager ******#

sm = ScreenManager()
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(MainScreen(name='main'))

#---------------------------------------------#

#****** launch ******#
class TestApp(App):
    def build(self):
        return sm
if __name__ == '__main__':
    TestApp().run()
#-------------------------#
