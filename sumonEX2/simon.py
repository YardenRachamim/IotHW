# Yarden Rachamim: 204623284
# Maya Kerem: 204818181

import RPi.GPIO as GPIO
from time import sleep
import random

# Green
greenBTN = 26
greenLED = 18
greenFreq = 659
# Red
redBTN = 19
redLED = 23
redFreq = 440
# Blue
blueBTN = 13
blueLED = 25
blueFreq = 784
# Yellow
yellowBTN = 6
yellowLED = 12
yellowFreq = 523
# List
ledPIN = [greenLED, redLED, blueLED, yellowLED]
btnPIN = [greenBTN, redBTN, blueBTN, yellowBTN]
reverse_ledPIN = [yellowLED, blueLED, redLED, greenLED]
# Sound
soundPIN = 21
sound_dic = {greenLED: greenFreq,
             redLED: redFreq,
             blueLED: blueFreq,
             yellowLED: yellowFreq}
sleep_tone = 0.3

# Game Global Variables
# Generate a random list
random_list = []
# User actual input
user_input = []
# User turn status
turn = 0
# User pressed the right buttons
next_round = True

sleep_time = 0.6


# Start of main
def main():
    global turn
    global user_input
    global next_round
    # User pressed the rigth button
    is_correct_btn =True
    # Initialize all events
    set()
    add_detection()

    # Game Logic
    while next_round:
        # Game Input
        get_random_value()
        print(random_list)
        light_leds()

        # User input
        while True == user_playing(turn):
              #
              turn += 1
              add_detection()
              print("turn is = " + (str) (turn))
              if turn == len(random_list):
                  print("Initialize - end of turn")
                  turn = 0
                  user_input = []
                  next_round = True
                  break

    print("Sorry game ended")
    end_game()
#END OF MAIN

#START OF HELPER
def user_playing(turn):
    global next_round
    # Get user push value
    while True:
        if GPIO.event_detected(greenBTN):
            green_pushed()
            user_input.append(greenLED)
            remove_detection()
            break
        elif GPIO.event_detected(redBTN):
            red_pushed()
            user_input.append(redLED)
            remove_detection()
            break
        elif GPIO.event_detected(blueBTN):
            blue_pushed()
            user_input.append(blueLED)
            remove_detection()
            break

        elif GPIO.event_detected(yellowBTN):
            yellow_pushed()
            user_input.append(yellowLED)
            remove_detection()
            break
        # Cmpare first user_input[0] and random_list[0]
    print((str) (user_input) + " = user")
    print((str) (random_list) + " = random")
    if user_input[turn] != random_list[turn]:
        print("Sorry wrong button!")
        next_round = False
        return False

    return True



# Remove detection from all buttons
def remove_detection():
    GPIO.remove_event_detect(greenBTN)
    GPIO.remove_event_detect(redBTN)
    GPIO.remove_event_detect(blueBTN)
    GPIO.remove_event_detect(yellowBTN)


# Add detection to all buttons
def add_detection():
    GPIO.add_event_detect(greenBTN, GPIO.RISING, bouncetime=200)
    GPIO.add_event_detect(redBTN, GPIO.RISING, bouncetime=200)
    GPIO.add_event_detect(blueBTN, GPIO.RISING, bouncetime=200)
    GPIO.add_event_detect(yellowBTN, GPIO.RISING, bouncetime=200)


# Light the leds according to random_value
def light_leds():
   for led in random_list:
       GPIO.output(led, GPIO.HIGH)
       led_sound(sound_dic[led])
       sleep(sleep_time)
       GPIO.output(led, GPIO.LOW)
       sleep(sleep_time)


# Generate random values
def get_random_value():
    random_list.append(ledPIN[random.randint(0,3)])


# On button pushed
def green_pushed():
    print("green was pushed")
    GPIO.output(greenLED, GPIO.HIGH)
    led_sound(greenFreq)
    sleep(sleep_time)
    GPIO.output(greenLED, GPIO.LOW)
    #sleep(sleep_time)


def red_pushed():
    print("red was pushed")
    GPIO.output(redLED, GPIO.HIGH)
    #sleep(sleep_time)
    led_sound(redFreq)
    sleep(sleep_time)
    GPIO.output(redLED, GPIO.LOW)
    #sleep(sleep_time)



def blue_pushed():
    print("blue was pushed")
    GPIO.output(blueLED, GPIO.HIGH)
    led_sound(blueFreq)
    sleep(sleep_time)
    GPIO.output(blueLED, GPIO.LOW)
    #sleep(sleep_time)

def yellow_pushed():
    print("Yellow was pushed")
    GPIO.output(yellowLED, GPIO.HIGH)
    led_sound(yellowFreq)
    sleep(sleep_time)
    GPIO.output(yellowLED, GPIO.LOW)
    #sleep(sleep_time)

# Excute sound for each led
def led_sound(freq):
    wiringpi.softToneWrite(soundPIN, freq)
    sleep(sleep_tone)
    wiringpi.softToneWrite(soundPIN, 0)


# Sound of a fauilere

# Set from the beginning after cleanup()
def set():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    wiringpi.wiringPiSetupGpio()
    wiringpi.softToneCreate(soundPIN)
    for pin in ledPIN:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    for pin in btnPIN:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# All lights on
def all_leds_sound():
    GPIO.output(greenLED, GPIO.HIGH)
    GPIO.output(redLED, GPIO.HIGH)
    GPIO.output(blueLED, GPIO.HIGH)
    GPIO.output(yellowLED, GPIO.HIGH)
    for freq in list(sound_dic.values()):
        wiringpi.softToneWrite(soundPIN, freq)
        sleep(0.1)
    GPIO.output(greenLED, GPIO.LOW)
    GPIO.output(redLED, GPIO.LOW)
    GPIO.output(blueLED, GPIO.LOW)
    GPIO.output(yellowLED, GPIO.LOW)
    wiringpi.softToneWrite(soundPIN,0)

# Light right to Left
def right_left_sound(led):
    GPIO.output(led, GPIO.HIGH)
    wiringpi.softToneWrite(soundPIN, sound_dic[led])
    sleep(0.3)
    GPIO.output(led, GPIO.LOW)
    wiringpi.softToneWrite(soundPIN, 0)


# End of game
def end_game():
    # all leds on, all sound on
    all_leds_sound()
    # right to left
    for led in ledPIN:
        right_left_sound(led)
    for led in reverse_ledPIN:
        right_left_sound(led)


#END OF HELPER




if __name__ == "__main__":
    main()
