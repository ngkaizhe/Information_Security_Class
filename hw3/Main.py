import os
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from PIL import Image
from Crypto.Cipher import AES
from kivy.factory import Factory
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from mode.CBC import CBC
from mode.ECB import ECB
from mode.CTR import CTR
from mode.CTR2 import CTR2
#import win32timezone

kivy.require('1.11.1')  # replace with your current kivy version !


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ShowScreen(Widget):

    defaultLocation = os.path.join(os.getcwd(), 'asset/default.png')
    tempResultLocation = os.path.join(os.getcwd(), 'asset/tempResult.ppm')
    tempCauseLocation = os.path.join(os.getcwd(), 'asset/tempCause.ppm')

    beforeProcessingLocation = StringProperty(defaultLocation)
    afterProcessingLocation = StringProperty(defaultLocation)

    beforeProcessingWidget = ObjectProperty(None)
    afterProcessingWidget = ObjectProperty(None)

    beforeProcessingImg = Image.open(defaultLocation)
    afterProcessingImg = Image.open(defaultLocation)

    @staticmethod
    def to16Bytes(data):
        if len(data) < 16:
            return data + ('0' * (16 - len(data)))
        return data[:16]

    @staticmethod
    def to8Bytes(data):
        if len(data) < 8:
            return data + ('0' * (8 - len(data)))
        return data[:8]

    def encrypt(self, **kwargs):
        mode = kwargs['mode']
        key = (self.to16Bytes(kwargs['key'])).encode('utf-8')

        if mode == 'ECB':
            ecb = ECB()
            self.afterProcessingImg = ecb.ECB_encrypt(
                self.beforeProcessingWidget.source, key)
        elif mode == 'CBC':
            cbc = CBC()
            iv = (self.to16Bytes(kwargs['IV'])).encode('utf-8')
            self.afterProcessingImg = cbc.CBC_encrypt(
                self.beforeProcessingWidget.source, key, iv)
        elif mode == 'CTR':
            ctr = CTR()
            nonce = (self.to8Bytes(kwargs['Nonce'])).encode('utf-8')
            intial_value = int(kwargs['InitialValue'])
            self.afterProcessingImg = ctr.CTR_encrypt(
                self.beforeProcessingWidget.source, key, nonce, intial_value)
        elif mode == 'CTR2':
            ctr2 = CTR2()
            nonce = (self.to8Bytes(kwargs['Nonce'])).encode('utf-8')
            intial_value = int(kwargs['InitialValue'])
            seed = int(kwargs['Seed'])
            self.afterProcessingImg = ctr2.CTR2_encrypt(
                self.beforeProcessingWidget.source, key, nonce, intial_value, seed)

        self.afterProcessingImg.save(self.tempResultLocation)
        self.afterProcessingWidget.source = self.tempResultLocation
        self.afterProcessingWidget.reload()

    def decrypt(self, **kwargs):
        mode = kwargs['mode']
        key = (self.to16Bytes(kwargs['key'])).encode('utf-8')

        if mode == 'ECB':
            ecb = ECB()
            self.afterProcessingImg = ecb.ECB_decrypt(
                self.beforeProcessingWidget.source, key)
        elif mode == 'CBC':
            cbc = CBC()
            iv = (self.to16Bytes(kwargs['IV'])).encode('utf-8')
            self.afterProcessingImg = cbc.CBC_decrypt(
                self.beforeProcessingWidget.source, key, iv)
        elif mode == 'CTR':
            ctr = CTR()
            nonce = (self.to8Bytes(kwargs['Nonce'])).encode('utf-8')
            intial_value = int(kwargs['InitialValue'])
            self.afterProcessingImg = ctr.CTR_decrypt(
                self.beforeProcessingWidget.source, key, nonce, intial_value)
        elif mode == 'CTR2':
            ctr2 = CTR2()
            nonce = (self.to8Bytes(kwargs['Nonce'])).encode('utf-8')
            intial_value = int(kwargs['InitialValue'])
            seed = int(kwargs['Seed'])
            self.afterProcessingImg = ctr2.CTR2_decrypt(
                self.beforeProcessingWidget.source, key, nonce, intial_value, seed)

        self.afterProcessingImg.save(self.tempResultLocation)
        self.afterProcessingWidget.source = self.tempResultLocation
        self.afterProcessingWidget.reload()

    def dismiss_popup(self):
        self._popup.dismiss()

    def LoadImage(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def SaveResult(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def UseResult(self):
        # update ui
        self.afterProcessingImg.save(self.tempCauseLocation)
        self.beforeProcessingWidget.source = self.tempCauseLocation
        self.beforeProcessingWidget.reload()
        self.afterProcessingWidget.source = self.defaultLocation
        self.afterProcessingWidget.reload()

    def load(self, path, filename):
        self.beforeProcessingWidget.source = os.path.join(path, filename[0])
        self.beforeProcessingImg = Image.open(
            self.beforeProcessingWidget.source)
        self.dismiss_popup()

    def save(self, path, filename):
        self.afterProcessingImg.save(os.path.join(path, filename))
        self.dismiss_popup()


class ShowApp(App):

    def build(self):
        return ShowScreen()


if __name__ == '__main__':
    Factory.register('ShowScreen', cls=ShowScreen)
    Factory.register('LoadDialog', cls=LoadDialog)
    Factory.register('SaveDialog', cls=SaveDialog)

    ShowApp().run()
