import modi
import time
import datetime
#modi.update_module_firmware()

path = ['U', 'L', 'L', 'L']
bundle=modi.MODI()
ir0=bundle.irs[0]
ir1=bundle.irs[1]
motor1=bundle.motors[0]
motor2=bundle.motors[1]

def both_white():
    if ir0.proximity>50 and ir1.proximity>50: return True
    return False

def both_black():
    if ir0.proximity<50 and ir1.proximity<50: return True
    return False

def invalid():
    if ir0.proximity==0 or ir1.proximity==0: return True
    return False

def go_back():
    
    '''
    Goes back a bit for correction

    '''
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 0.125:
        go_forward(-25)

    


def test_ir_sensor():
    #time.sleep(5)
    start = datetime.datetime.now()
    while ir1==0:
        pass
    x = (datetime.datetime.now() - start)
    print(x)
    return
    print("IR0 "+str(ir0.proximity))
    print("IR1 "+str(ir1.proximity))
    start =  datetime.datetime.now()
    while ir0.proximity > 50 and ir1.proximity > 50:
        go_forward()
    end = datetime.datetime.now()

    print("ABABABABABABABABA    " + str((end-start).microseconds))
    stop_car()
    #time.sleep(0.5)


def go_forward(x=100):
    motor1.speed = -x, x
    motor2.speed = -x, x

def stop_car():
    '''
    Stop the car by making the speed 0
    '''
    motor1.speed = 0, 0
    motor2.speed = 0, 0

def rotate_right(x):
    '''
        -100, -100
        -100, -100
        For rotate right by some degree
    '''
    motor1.speed = -x, -x
    motor2.speed = -x, -x

def rotate_left(x):
    '''
        100, 100
        100, 100
        For rotate left by some degree
    '''
    motor1.speed = x, x 
    motor2.speed = x, x

def do_correction():
    '''
    Make the car directly look forward by slightly rotating the car
    '''
    while invalid(): pass
    print(f'ir0 {ir0.proximity} \t ir1 {ir1.proximity}')
    if ir0.proximity<50 and ir1.proximity<50: return 'WHITE'    # In White
    if ir0.proximity>50 and ir1.proximity>50: return 'BLACK'    # In Black
    if ir0.proximity < ir1.proximity :                   # While The left part (ir1) of the car is in white
        while ir1.proximity>50 and not both_white():                         # 
            rotate_right(25)
        stop_car()
        return 'Rotated Right'
    if ir0.proximity > ir1.proximity :                   # While The left part (ir1) of the car is in white
        while ir0.proximity>50 and not both_white():                         # 
            rotate_left(25)
        stop_car()
        return 'Rotated Left'
    
    
def move_up():
    '''
        Move to the front box
    '''
    while invalid():
        pass
    #First go till we hit the black line by either of the sensors
    start1 = datetime.datetime.now()
    while ir0.proximity > 50 and ir1.proximity > 50:
        go_forward(25)
    end1 = datetime.datetime.now()

    #start = datetime.datetime.now()
    #while (datetime.datetime.now() - start).seconds < 0.1:
    #    go_forward()
    #while ir0.proximity>50 and ir1.proximity>50:
    #    go_forward()
    
    #Correct the car
    while invalid(): pass

    stop_car()
    print('Correction ' + do_correction())
    stop_car()
    
    #Move to the next box in front
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 9.5*0.125:
        while both_white():
            go_forward(50)
    
    stop_car()
    go_back()
    # while ir0.proximity>50 and ir1.proximity>50:
    #    go_forward()
    #do_correction()
    stop_car()


def move_left():
    '''
    Move to the left box
    '''
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 0.7:
        rotate_left(50)
    move_up()
    stop_car()
    

def move_right():
    '''
    Move to the right box
    '''

    start = datetime.datetime.now()
    while (datetime.datetime.now() - start).seconds < 0.7:
        rotate_right(50)
    print("X     Y      Z")
    move_up()
    stop_car()
    

if __name__ == "__main__":
    time.sleep(1)
    for i in path:
        if i == 'U': move_up()
        if i == 'L': move_left()
        if i == 'R': move_right() 