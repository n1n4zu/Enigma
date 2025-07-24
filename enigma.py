class Enigma:
    """
    A simulation of the Enigma machine used for encryption and decryption.
    The machine consists of rotors, a reflector, and a plugboard that work together
    to perform complex substitution ciphers.
    """

    # Dictionary mapping letters to their corresponding index (A=0, B=1, ..., Z=25)
    __indexes_alf = {
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7,
        'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14,
        'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21,
        'W': 22, 'X': 23, 'Y': 24, 'Z': 25
    }

    # Dictionary mapping indexes back to their corresponding letters (0=A, 1=B, ..., 25=Z)
    __indexes_num = {
        0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H',
        8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O',
        15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V',
        22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
    }

    def __init__(self, offset: str, ring_setting: str, notch: str) -> None:
        """
        Initializes the Enigma machine with rotor settings.

        :param offset: 3-character string representing initial rotor positions
        :param ring_setting: 3-character string representing ring settings
        :param notch: 3-character string representing notch positions
        """
        self.__offset_r1 = self.__indexes_alf[offset[0].upper()]
        self.__offset_r2 = self.__indexes_alf[offset[1].upper()]  # Fixed typo in __indexes_alf
        self.__offset_r3 = self.__indexes_alf[offset[2].upper()]

        self.__ring_setting_r1 = self.__indexes_alf[ring_setting[0].upper()]
        self.__ring_setting_r2 = self.__indexes_alf[ring_setting[1].upper()]
        self.__ring_setting_r3 = self.__indexes_alf[ring_setting[2].upper()]

        self.__notch_r1 = self.__indexes_alf[notch[0].upper()]
        self.__notch_r2 = self.__indexes_alf[notch[1].upper()]
        self.__notch_r3 = self.__indexes_alf[notch[2].upper()]

        # Plugboard connections (Steckerbrett) - fixed pair substitutions
        self.__plugboard = {
            'A': 'G', 'G': 'A', 'B': 'K', 'K': 'B', 'C': 'M', 'M': 'C',
            'D': 'Z', 'Z': 'D', 'E': 'L', 'L': 'E', 'F': 'T', 'T': 'F',
            'H': 'V', 'V': 'H', 'I': 'P', 'P': 'I', 'J': 'X', 'X': 'J',
            'N': 'Q', 'Q': 'N'
        }

        # Rotor I wiring (ETW - Eintrittswalze)
        self.__P_r1 = {
            'A': 'E', 'B': 'K', 'C': 'M', 'D': 'F', 'E': 'L', 'F': 'G',
            'G': 'D', 'H': 'Q', 'I': 'V', 'J': 'Z', 'K': 'N', 'L': 'T',
            'M': 'O', 'N': 'W', 'O': 'Y', 'P': 'H', 'Q': 'X', 'R': 'U',
            'S': 'S', 'T': 'P', 'U': 'A', 'V': 'I', 'W': 'B', 'X': 'R',
            'Y': 'C', 'Z': 'J'
        }

        # Rotor II wiring
        self.__P_r2 = {
            'A': 'K', 'B': 'T', 'C': 'S', 'D': 'B', 'E': 'P', 'F': 'O',
            'G': 'G', 'H': 'U', 'I': 'L', 'J': 'R', 'K': 'H', 'L': 'E',
            'M': 'F', 'N': 'M', 'O': 'D', 'P': 'W', 'Q': 'V', 'R': 'A',
            'S': 'N', 'T': 'Q', 'U': 'I', 'V': 'X', 'W': 'J', 'X': 'Y',
            'Y': 'C', 'Z': 'Z'
        }

        # Rotor III wiring
        self.__P_r3 = {
            'A': 'S', 'B': 'B', 'C': 'W', 'D': 'P', 'E': 'U', 'F': 'D',
            'G': 'H', 'H': 'T', 'I': 'G', 'J': 'F', 'K': 'C', 'L': 'N',
            'M': 'E', 'N': 'Y', 'O': 'A', 'P': 'R', 'Q': 'O', 'R': 'I',
            'S': 'L', 'T': 'X', 'U': 'K', 'V': 'J', 'W': 'Z', 'X': 'M',
            'Y': 'Q', 'Z': 'V'
        }

    def __plugboard_swap(self, letter: str) -> str:
        """
        Performs plugboard substitution.
        If the letter is connected in the plugboard, returns its pair.
        Otherwise returns the original letter.

        :param letter: Input character to be substituted
        :return: Substituted character according to plugboard wiring
        """
        return self.__plugboard.get(letter, letter)

    def __move_rotor(self) -> None:
        """
        Advances the rotors according to the Enigma stepping mechanism.
        Implements the double-step anomaly where the middle rotor can advance
        twice in consecutive steps under certain conditions.
        """
        # Right rotor always advances
        self.__offset_r1 = (self.__offset_r1 + 1) % 26

        # Middle rotor advances if right rotor is at notch position
        if self.__offset_r1 == self.__notch_r1:
            self.__offset_r2 = (self.__offset_r2 + 1) % 26

            # Left rotor advances if middle rotor is at notch position
            if self.__offset_r2 == self.__notch_r2:
                self.__offset_r3 = (self.__offset_r3 + 1) % 26

        # Double-step anomaly: Middle rotor also advances when right rotor
        # is one position before its notch
        elif (self.__offset_r1 + 1) % 26 == self.__notch_r1:
            self.__offset_r2 = (self.__offset_r2 + 1) % 26

    def __rotor_1(self, letter: str) -> str:
        """
        Passes a letter through the first rotor (rightmost) in forward direction.

        :param letter: Input character to be processed
        :return: Transformed character after passing through the rotor
        """
        input_r1 = (self.__indexes_alf[letter] + self.__offset_r1 - self.__ring_setting_r1) % 26
        wired_letter = self.__P_r1[self.__indexes_num[input_r1]]
        output = (self.__indexes_alf[wired_letter] - self.__offset_r1 + self.__ring_setting_r1) % 26
        return self.__indexes_num[output]

    def __rotor_2(self, letter: str) -> str:
        """
        Passes a letter through the second rotor (middle) in forward direction.

        :param letter: Input character to be processed
        :return: Transformed character after passing through the rotor
        """
        input_r2 = (self.__indexes_alf[letter] + self.__offset_r2 - self.__ring_setting_r2) % 26
        wired_letter = self.__P_r2[self.__indexes_num[input_r2]]
        output = (self.__indexes_alf[wired_letter] - self.__offset_r2 + self.__ring_setting_r2) % 26
        return self.__indexes_num[output]

    def __rotor_3(self, letter: str) -> str:
        """
        Passes a letter through the third rotor (leftmost) in forward direction.

        :param letter: Input character to be processed
        :return: Transformed character after passing through the rotor
        """
        input_r3 = (self.__indexes_alf[letter] + self.__offset_r3 - self.__ring_setting_r3) % 26
        wired_letter = self.__P_r3[self.__indexes_num[input_r3]]
        output = (self.__indexes_alf[wired_letter] - self.__offset_r3 + self.__ring_setting_r3) % 26
        return self.__indexes_num[output]

    def __rotor_1_rev(self, letter: str) -> str:
        """
        Passes a letter through the first rotor (rightmost) in reverse direction.

        :param letter: Input character to be processed
        :return: Transformed character after passing through the rotor
        """
        P_r1_rev = {value: key for key, value in self.__P_r1.items()}
        input_r1 = (self.__indexes_alf[letter] + self.__offset_r1 - self.__ring_setting_r1) % 26
        wired_letter = P_r1_rev[self.__indexes_num[input_r1]]
        output = (self.__indexes_alf[wired_letter] - self.__offset_r1 + self.__ring_setting_r1) % 26
        return self.__indexes_num[output]

    def __rotor_2_rev(self, letter: str) -> str:
        """
        Passes a letter through the second rotor (middle) in reverse direction.

        :param letter: Input character to be processed
        :return: Transformed character after passing through the rotor
        """
        P_r2_rev = {value: key for key, value in self.__P_r2.items()}
        input_r2 = (self.__indexes_alf[letter] + self.__offset_r2 - self.__ring_setting_r2) % 26
        wired_letter = P_r2_rev[self.__indexes_num[input_r2]]
        output = (self.__indexes_alf[wired_letter] - self.__offset_r2 + self.__ring_setting_r2) % 26
        return self.__indexes_num[output]

    def __rotor_3_rev(self, letter: str) -> str:
        """
        Passes a letter through the third rotor (leftmost) in reverse direction.

        :param letter: Input character to be processed
        :return: Transformed character after passing through the rotor
        """
        P_r3_rev = {value: key for key, value in self.__P_r3.items()}
        input_r3 = (self.__indexes_alf[letter] + self.__offset_r3 - self.__ring_setting_r3) % 26
        wired_letter = P_r3_rev[self.__indexes_num[input_r3]]
        output = (self.__indexes_alf[wired_letter] - self.__offset_r3 + self.__ring_setting_r3) % 26
        return self.__indexes_num[output]

    def __reflector(self, letter: str) -> str:
        """
        Passes a letter through the reflector (UKW), causing it to be redirected
        back through the rotors via a different path.

        :param letter: Input character to be processed
        :return: Reflected character according to reflector wiring
        """
        P_ref = {
            'A': 'R', 'R': 'A', 'B': 'Q', 'Q': 'B', 'C': 'P', 'P': 'C',
            'D': 'O', 'O': 'D', 'E': 'N', 'N': 'E', 'F': 'M', 'M': 'F',
            'G': 'L', 'L': 'G', 'H': 'K', 'K': 'H', 'I': 'J', 'J': 'I',
            'S': 'Z', 'Z': 'S', 'T': 'Y', 'Y': 'T', 'U': 'X', 'X': 'U',
            'V': 'W', 'W': 'V'
        }
        return P_ref[letter]

    def enigma(self, message: str) -> str:
        """
        Encrypts or decrypts a message using the Enigma machine.
        The process is symmetric - the same settings will decrypt an encrypted message.

        :param message: Input string to be processed
        :return: Processed string after passing through the Enigma machine
        """
        # Normalize the message (uppercase, remove spaces)
        message = message.upper().split()
        message = ''.join(message)

        encrypted = []
        for char in message:
            # Advance rotors before processing each character
            self.__move_rotor()

            # Full encryption path:
            # Plugboard → Rotors 1-3 → Reflector → Rotors 3-1 → Plugboard
            encrypted_char = self.__plugboard_swap(
                self.__rotor_1_rev(
                    self.__rotor_2_rev(
                        self.__rotor_3_rev(
                            self.__reflector(
                                self.__rotor_3(
                                    self.__rotor_2(
                                        self.__rotor_1(
                                            self.__plugboard_swap(char)
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
            encrypted.append(encrypted_char)

        return ''.join(encrypted)