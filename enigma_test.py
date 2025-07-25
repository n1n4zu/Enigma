from enigma import Enigma
import unittest


class TestEnigma(unittest.TestCase):
    def test_enigma(self):
        initial_settings = 'NFC'
        ring_settings = 'GYZ'
        notch_settings = 'DFR'
        test_message = 'TEST MESSAGE - 123,!342'
        test_message = test_message.split()
        test_message = ''.join(test_message)

        print("\n=== Starting Enigma Test ===")
        print(f"Initial settings: {initial_settings}")
        print(f"Ring settings: {ring_settings}")
        print(f"Notch positions: {notch_settings}")
        print(f"Test message: {test_message}")

        print("\nCreating Enigma machines for encryption and decryption...")
        enigma_encrypt = Enigma(initial_settings, ring_settings, notch_settings)
        enigma_decrypt = Enigma(initial_settings, ring_settings, notch_settings)

        print("\nStarting encryption...")
        encrypted = enigma_encrypt.enigma(test_message)
        print(f"Encrypted message: {encrypted}")

        print("\nStarting decryption...")
        decrypted = enigma_decrypt.enigma(encrypted)
        print(f"Decrypted message: {decrypted}")

        print("\nVerifying result...")
        try:
            self.assertEqual(test_message, decrypted,
                             f"TEST FAILED: Original message '{test_message}' "
                             f"does not match decrypted '{decrypted}'")

            print("=== TEST PASSED ===")
            print("Enigma works correctly - encryption and decryption functional")

        except AssertionError as e:
            print("\n=== TEST FAILED ===")
            print(str(e))
            print("\nPossible causes of issues:")
            print("1. Incorrect rotor implementations (forward/backward)")
            print("2. Errors in rotor stepping logic")
            print("3. Problem with plugboard or reflector")
            print("4. Incorrect handling of ring settings")
            print("5. Error in modulo 26 calculations")

            raise


if __name__ == '__main__':
    unittest.main()
