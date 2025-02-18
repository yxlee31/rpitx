import time
import numpy as np
import os

def bit_to_qpsk(bitstream):
    """Convert a bitstream into QPSK symbols."""
    symbols = []
    for i in range(0, len(bitstream), 2):
        bits = bitstream[i:i+2]
        if bits == "00":
            symbols.append(1 + 1j)  # 45° phase
        elif bits == "01":
            symbols.append(-1 + 1j)  # 135° phase
        elif bits == "10":
            symbols.append(1 - 1j)  # -45° phase
        elif bits == "11":
            symbols.append(-1 - 1j)  # -135° phase
    return np.array(symbols)

def read_bitstream(file_path="bitstream.bin", chunk_size=1024):
    """Continuously read the bitstream from a file."""
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break  # End of file
            bitstream = ''.join(format(byte, '08b') for byte in chunk)  # Convert to binary string
            qpsk_symbols = bit_to_qpsk(bitstream)  # Convert to QPSK symbols
            qpsk_symbols.tofile("qpsk_data.bin")  # Save QPSK data for transmission
            print("QPSK symbols ready for transmission.")
            yield qpsk_symbols  # Yield for transmission or further processing

def transmit_qpsk():
    """Transmit the QPSK-modulated bitstream using rpitx."""
    os.system("./rpitx -f 87000000 -m QPSK -b qpsk_data.bin")

# Main loop
def main():
    file_path = "bitstream.bin"  # Path to your file containing the bitstream
    for qpsk_symbols in read_bitstream(file_path):
        # Transmit the QPSK symbols
        transmit_qpsk()
        time.sleep(0.1)  # Sleep to prevent too high CPU usage

# Only runs if code is executed directly from command line
if __name__ == "__main__":
    main()
