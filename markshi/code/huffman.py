from bitstring import Bits

'''
Special codes
These codes are guaranteed not to collide with encoded image data. They are construted using 4.5 bytes of zeros followed
by a 4-bit code.
Why? The longest string of zeros we can encounter in a standard huffman code is 11. Furthermore, an escaped (run, level)
encoding might have 22 zeros. So we want to handle the case where we encode 22 + 11 = 33 zeros. In practice, we need
fewer zeros, but cutting down would afford little benefit.
'''

EOF = '00000000 00000000 00000000 00000000 0000 0001'.replace(' ', '')

'''
End special codes
'''

def read_raw_VLC():
    """
    Read raw huffman codes from our text file
    This is a CSV file with the format: run, level, VLC, #bits \n
    :return: list of codes, one set of VLC data per entry
    """
    try:
        with open('mpeg_huffman_codes.csv') as f:
            codes = f.read().split('\n')[1:-1]
    except:
        raise Exception("Missing required file mpeg_huffman_codes.csv.")

    return codes

# TODO: We might try making encoder tables incorporate the sign bit, to eliminate the need to test the polarity of the level during encoding. This would mean we make two entries like (1,2) and (1,-2) that map to the same binary code.

def make_encoder_table():
    """
    Make a dictionary. (O(1) lookups)
    Keys: tuple with (run, level)
    Data: Bits object with VLC
    :return: encoder table that can be used to quickly find a VLC given a run, level entry.
    NOTE: The sign bit must be appended to each VLC when encoding (except for EOB and ESC).
    """
    codes = read_raw_VLC()

    def get_rid_of_prefix_0(s):
        while s[0]=='0':
            #print(1)
            s=s[1:]
        return s

    # Add all VLCs to the table
    encoder_table = dict()
    for code in codes:
        x = code.split(',')
        key = tuple(map(int,(x[0], x[1])))
        s = get_rid_of_prefix_0(x[2])
        #print(x[2],s,type(x[2]))
        bits = Bits('0b' + s)
        encoder_table[key] = bits

    # Add special codes to the table
    encoder_table['EOM'] = Bits('0b001')
    encoder_table['EOB'] = Bits('0b10')
    encoder_table['ESC'] = Bits('0b000001')

    # Return the table
    return encoder_table

def make_decoder_table():
    """
    Again, we will use a dictionary so we have O(1) lookups
    Keys: Bits object with VLC
    Data: tuple with (run, level)
    :return: decoder dictionary. The idea is to perform successive lookups on a string of bits until we get a match.
    """
    codes = read_raw_VLC()

    decoder_table = dict()
    for code in codes:
        x = code.split(',')
        key = Bits('0b' + x[2])
        run_level = tuple(map(int, (x[0], x[1])))
        decoder_table[key] = run_level

    # Add special codes to the table
    decoder_table[Bits('0b10')] = 'EOB'
    decoder_table[Bits('0b000001')] = 'ESC'

    return decoder_table

def main():

    # Make encoder table, show how to access the bits for a given run, level tuple that we want to encode:
    table = make_encoder_table()
    print("To encode (0,3):", table[(0,3)], "+ sign bit")
    print("To encode EOB:", table['EOB'])

    # Make decoder table, show how to access the run_level tuple for a 4-bit code of '0100'
    table = make_decoder_table()
    if Bits('0b000000000010000') in table: # it is
        print("Found it:", table[Bits('0b000000000010000')])
    if Bits('0b0000000000100001') not in table: # it's not
        print("Code not in table.")


if __name__ == "__main__":
    main()