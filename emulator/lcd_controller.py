



"""
what i care about for now
    clear display
    increment cursor

    
cpu: 0x6000
via: 0 (PORTB)
lcd: data

"""

class _LCD_STATE:
    

    # TODO this is actually a mix of lcd and via state
    # they should really be split


    # for now im merging via and lcd controller

    cursor_location = 0
    display:list[str] = [""]
    # also ignoring two lines

    # actually latched in porta of via
    RS = 0
    E = 0

    # actually latched in portb of via
    data = 0

def __write_control(RS_in, E_in):


    update_triggered = _LCD_STATE.E == 0 and E_in == 1

    if update_triggered and RS_in:

        __write_char(_LCD_STATE.data)
    elif update_triggered and not RS_in:
        __update_mode(_LCD_STATE.data)

    _LCD_STATE.RS = RS_in
    _LCD_STATE.E = E_in
    ...



def __update_mode(value):

    clear_display_code = 0b00000001

    increment_cursor_code = 0b00000110

    
    if value == clear_display_code:
        _LCD_STATE.display = [""]

    elif value == increment_cursor_code:
        _LCD_STATE.cursor_location += 1




def __write_char(value):

    location = _LCD_STATE.cursor_location

    n_in_display = len(_LCD_STATE.display)
    if location >= n_in_display:
        _LCD_STATE.display += [""]*(location-n_in_display+1)
        
    _LCD_STATE.display[location] = chr(value)

    _LCD_STATE.cursor_location += 1


def __get_bits(value):
    binary_string = bin(value)[2:].zfill(8)
    return map(int, binary_string)


    

def send_signal_to_via(address, value):
    # technically porta and portb are the stored state in the via
    # (the via latches the values)
    # but this is fine for now

    if address == 0:
        portb = value
        _LCD_STATE.data = portb
    elif address == 1:
        porta = value
        (E,_,RS,_,_,_,_,_) = __get_bits(porta)
        __write_control(RS, E)

def get_diplay():
    return "".join(_LCD_STATE.display)

