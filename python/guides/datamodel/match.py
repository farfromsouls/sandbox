class Robot:
    def handle_command(self, message):
        match message: # субьект

            # проверяется строка, а потом автоматом сопоставляются переменные
            case ['BEEPER', frequency, times]:
                self.beep(times, frequency)
            case ['NECK', angle]:
                self.rotate_neck(angle)
            case ['LED', ident, intensity]:
                self.leds[ident].set_brightness(ident, intensity)
            case ['LED', ident, red, green, blue]:
                self.leds[ident].set_color(red, green, blue)
            case _:
                raise ValueError(message)
            
areas = [
    ("1", "2", "3", (1, 2)),
    ("2", "2", "3", (2, 2)),
    ("3", "2", "3", (3, 2)),
    ("4", "2", "3", (4, 2))
]
print(f'{"":15} | {"lattitude":>9} | {"longitude":>9}')
for record in areas:
    match record:
        case [name, _, _, (lat, lon)] if lon >= 0: 
            print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')