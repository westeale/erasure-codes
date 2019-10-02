import numpy as np

from app.polarcodes.polarcodes import Polarcodes

encoded_message = [1, 0, 1, 0, 1, 0, 1, 0]

polarcoder = Polarcodes(0.5, 8, 4)

erased_message = polarcoder.simulate_bec_channel(encoded_message)
print(erased_message)

erased_message = polarcoder.simulate_bec_channel(encoded_message)
print(erased_message)