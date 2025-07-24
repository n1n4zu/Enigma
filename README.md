# Enigma Machine Simulator

A Python implementation of the famous Enigma machine used by Germany during World War II, with historical accuracy in its encryption mechanism.

## Features

- **3 Rotor System**: Simulates the standard 3-rotor Enigma I configuration
- **Plugboard (Steckerbrett)**: Implements letter pair substitutions
- **Reflector (UKW)**: Correctly models the fixed reflector wiring
- **Double-Step Anomaly**: Accurately replicates the middle rotor's double-stepping behavior
- **Ring Settings & Notches**: Configurable rotor ring settings and turnover positions

## Installation

```bash
git clone https://github.com/n1n4zu/Enigma.git
cd Enigma
```

## Usage

### Basic Operation

```python
from enigma import Enigma

# Initialize with rotor positions, ring settings, and notch positions
enigma = Enigma(offset='ABC', ring_setting='WHZ', notch='QFR')

# Encrypt a message
encrypted = enigma.enigma("SECRETMESSAGE")

# Decrypt (using same settings)
decrypted = enigma.enigma(encrypted)
```

### Running Tests

```bash
python enigma_test.py
```

## Class documentation

### `Enigma` Class

#### Constructor

```python
def __init__(self, offset: str, ring_setting: str, notch: str) -> None
```

- **`offset`**: 3-character initial rotor positions (e.g., 'ABC')
- **`ring_setting`**: 3-character ring settings (e.g., 'WHZ')
- **`notch`**: 3-character notch positions (e.g., 'QFR')

#### Public Methods
| **Method**                        | **Description**             |
|-----------------------------------|-----------------------------|
| **`enigma(message: str) -> str`** | Encrypts/decrypts a message |

#### Private Methods

| **Method**                              | **Description**                                                                   |
|-----------------------------------------|-----------------------------------------------------------------------------------|
| **`__move_rotor() -> None`**            | Advances rotors according to Enigma stepping rules, including double-step anomaly |
| **`__rotor_1(letter: str) -> str`**     | Processes letter through right rotor (forward direction)                          |
| **`__rotor_2(letter: str) -> str`**     | Processes letter through middle rotor (forward direction)                         |
| **`__rotor_3(letter: str) -> str`**     | Processes letter through left rotor (forward direction)                           |
| **`__rotor_1_rev(letter: str) -> str`** | Processes letter through right rotor (reverse direction)                          |
| **`__rotor_2_rev(letter: str) -> str`** | Processes letter through middle rotor (reverse direction)                         |
| **`__rotor_3_rev(letter: str) -> str`** | Processes letter through left rotor (reverse direction)                           |

#### Substitution Components

| **Method**                                 | **Description**                                |
|--------------------------------------------|------------------------------------------------|
| **`__plugboard_swap(letter: str) -> str`** | Performs plugboard substitution (Steckerbrett) |
| **`__reflector(letter: str) -> str`**      | Processes letter through the reflector (UKW)   |

## Technical Details

### Encryption Process

1. Plugboard substitution
2. Forward pass through rotors (right to left)
3. Reflection via UKW reflector
4. Reverse pass through rotors (left to right)
5. Final plugboard substitution

### Rotor Wiring

- **Rotor I**: ETW (Eintrittswalze) wiring
- **Rotor II**: Standard military wiring
- **Rotor III**: Standard military wiring
- **Reflector**: UKW-B wiring

### Example

```python
# Initialize two machines with same settings
encryptor = Enigma('ABC', 'WHZ', 'QFR')
decryptor = Enigma('ABC', 'WHZ', 'QFR')

message = "ATTACKATDAWN"
ciphertext = encryptor.enigma(message)  # Returns encrypted text
plaintext = decryptor.enigma(ciphertext)  # Returns original message
```

## Historical Notes

This implementation accurately models:
- The double-stepping anomaly of the middle rotor
- Correct plugboard behavior
- Proper rotor advancement mechanics
- Period-accurate wiring configurations

## License

MIT License - See [LICENSE](LICENSE) for details