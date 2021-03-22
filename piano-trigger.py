import pygame
import pygame.midi

#global game variables
debug = False
run = True
midi = None

def main():
    #processes
    init()
    loop()

def init():
    #variables
    global run
    global midi

    pygame.init()
    pygame.midi.init()

    i = 0
    good_list = []
    print('Detecting MIDI devices available ...')
    while True:
        info = pygame.midi.get_device_info(i)
        if info == None:
            break
        if info[2] == 0: # not an input device
            i += 1
            continue
        print("device: %d"%(i),info)
        good_list.append(i)
        i += 1

        if len(good_list) == 0:
            print('No MIDI devices found, exiting ...')
            run = False
        else:
            i_select = good_list[0]
            print('connecting to device %d ...'%(i_select))
            midi = pygame.midi.Input(i_select)

def loop():
    #variables
    global run
    global midi
    note_sequence = []
    #note_sequence_key = [4, 4, 4, 4, 2, 2, 4, 2, 0] #Mary Had a Little Lamb
    note_sequence_key = [0, 0, 2, 0, 7, 5] #Happy Birthday
    NOTE_SEQUENCE_MAX = 6

    print("running ...")

    while run:
        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #midi detection
        b_msg = midi.poll()
        if b_msg == True:
            data = midi.read(1)
            if len(data) == 0:
                break

            #read note data
            (unknown1, note_id, force, unknown2) = data[0][0]
            """
            unknown1    - always seems to be 144 (?)
            note_id     - integer value representing note
            force       - strength key is pushed in, 0 if released
            unknown2    - always seems to be 0 (?)
            """

            if force > 0:
                #add note to sequence
                note_sequence.append(note_id)
                if len(note_sequence) > NOTE_SEQUENCE_MAX:
                    note_sequence.pop(0)
                if debug:
                    print(note_sequence)

                #cull check - ignore sequences where first 4 keys are not equal
                if len(note_sequence) != NOTE_SEQUENCE_MAX:
                    continue
                #if note_sequence[0] != note_sequence[1] or note_sequence[0] != note_sequence[2] or note_sequence[0] != note_sequence[3]:
                #    continue

                #compare sequence
                diff = min(note_sequence)
                temp_sequence = list(map((lambda x: x - diff), note_sequence))

                if debug:
                    str = "Key:\t\t{}\nAdjusted:\t{}\n"
                    print(str.format(note_sequence_key, temp_sequence))

                if temp_sequence == note_sequence_key:
                    print("==============")
                    print("MATCH DETECTED")
                    print("==============")
                    note_sequence.clear()
main()
