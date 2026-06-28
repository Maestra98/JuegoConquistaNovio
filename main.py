from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import random
from kivy.uix.label import Label

# Tamaño para probar en PC (proporción de móvil)
Window.size = (450, 800)
Window.clearcolor = (15/255, 23/255, 42/255, 1)


class Juego(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size = Window.size

        with self.canvas.before:
            Color(15/255, 23/255, 42/255, 1)
            self.fondo = Rectangle(pos=(0, 0), size=self.size)

        self.bind(size=self.actualizar_fondo)

        # Novia abajo
        self.novia = Image(
            source="assets/novia.png",
            size_hint=(None, None),
            size=(90, 90)
        )

        self.novia.pos = (
            Window.width/2 - self.novia.width/2,
            40
        )

        self.add_widget(self.novia)

        # Juego terminado
        self.juego_terminado = False
        # Lista de corazones
        self.corazones = []
        # Puntos
        self.puntos = 0
        # Lista de Migueles
        self.migueles = []
        # Velocidad de cada Miguel
        self.velocidades = []
        # Crear uno nuevo cada 2 segundos
        Clock.schedule_interval(self.crear_miguel, 1.2)
        # Disparar cada 0.35 segundos
        Clock.schedule_interval(self.disparar, 0.7)
        # Actualizar juego 60 veces por segundo
        Clock.schedule_interval(self.actualizar, 1/60)

        self.marcador = Label(
            text="Puntos: 0",
            font_size=28,
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "top": 1}
        )

        self.add_widget(self.marcador)

    def disparar(self, dt):

        corazon = Image(
            source="assets/corazon.png",
            size_hint=(None, None),
            size=(28, 28)
        )

        corazon.pos = (
            self.novia.center_x - corazon.width/2,
            self.novia.top
        )

        self.add_widget(corazon)
        self.corazones.append(corazon)

    def crear_miguel(self, dt):

        if len(self.migueles) >= 20:
            return

        enemigo = Image(
            source="assets/miguel.png",
            size_hint=(None, None),
            size=(80, 80)
        )

        enemigo.pos = (
            random.randint(0, Window.width - 80),
            Window.height
        )

        self.add_widget(enemigo)

        self.migueles.append(enemigo)

        self.velocidades.append(random.choice([-2, -1.5, 1.5, 2]))

    def actualizar(self, dt):

        # =========================
        # Mover corazones
        # =========================
        for corazon in self.corazones[:]:

            corazon.y += 5

            if corazon.y > Window.height:
                self.remove_widget(corazon)
                self.corazones.remove(corazon)
                continue

        # =========================
        # Colisiones
        # =========================
        for corazon in self.corazones[:]:

            for i, enemigo in enumerate(self.migueles[:]):

                if corazon.collide_widget(enemigo):

                    self.remove_widget(corazon)
                    self.remove_widget(enemigo)

                    self.corazones.remove(corazon)
                    self.migueles.remove(enemigo)
                    self.velocidades.pop(i)

                    self.puntos += 2
                    self.marcador.text = f"Puntos: {self.puntos}"

                    if self.puntos >= 100:
                        self.ganar()

                    break

        # =========================
        # Mover Migueles
        # =========================
        for i, enemigo in enumerate(self.migueles[:]):

            enemigo.x += self.velocidades[i]

            if enemigo.x <= 0 or enemigo.right >= Window.width:
                self.velocidades[i] *= -1

            enemigo.y -= 0.7

            if enemigo.y < -80:

                self.remove_widget(enemigo)
                self.velocidades.pop(i)
                self.migueles.remove(enemigo)

    def ganar(self):

        if self.juego_terminado:
            return

        self.juego_terminado = True

        Clock.unschedule(self.disparar)
        Clock.unschedule(self.crear_miguel)

        self.clear_widgets()

        self.canvas.before.clear()

        with self.canvas.before:
            Color(1, 0.75, 0.85, 1)
            self.rect = Rectangle(pos=(0, 0), size=Window.size)

        mensaje = Label(
            text="¡¡HAS GANADO!!\n\n¡HAS CONQUISTADO\nA MIGUEL!",
            font_size=52,
            color=(1,0,0,1),
            size_hint=(1,1),
            halign="center",
            valign="middle"
        )

        mensaje.bind(size=lambda instancia, valor: setattr(instancia, "text_size", valor))

        self.add_widget(mensaje)

    def actualizar_fondo(self, *args):
        self.fondo.size = self.size

    def on_touch_move(self, touch):

        nueva_x = touch.x - self.novia.width / 2

        # Limitar para que no salga de la pantalla
        if nueva_x < 0:
            nueva_x = 0

        if nueva_x > Window.width - self.novia.width:
            nueva_x = Window.width - self.novia.width

        self.novia.x = nueva_x

        return True

class ConquistaApp(App):
    def build(self):
        return Juego()


ConquistaApp().run()