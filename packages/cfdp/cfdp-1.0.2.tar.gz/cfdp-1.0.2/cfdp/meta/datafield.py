

class TypeLengthValue:

    def to_bytes(self):
        type = self.type
        length = len(self.value)
        value = self.value

        databytes = bytearray()
        databytes.append(type)
        databytes.append(length)
        databytes += value
        return databytes
