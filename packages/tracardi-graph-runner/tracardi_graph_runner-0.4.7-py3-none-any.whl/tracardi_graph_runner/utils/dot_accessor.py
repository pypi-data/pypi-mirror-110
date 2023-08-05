from dotty_dict import dotty


class DotAccessor:

    def __init__(self, profile, session, payload: dict, event):
        self.event = dotty(event.dict())
        self.payload = dotty(payload)
        self.session = dotty(session.dict())
        self.profile = dotty(profile.dict())

    def __setitem__(self, key, value):
        if key.startswith('profile@'):
            key = key[len('profile@'):]
            self.profile[key] = self.__getitem__(value)
        elif key.startswith('session@'):
            key = key[len('session@'):]
            self.session[key] = self.__getitem__(value)
        elif key.startswith('payload@'):
            key = key[len('payload@'):]
            self.payload[key] = self.__getitem__(value)
        elif key.startswith('event@'):
            key = key[len('event@'):]
            self.event[key] = self.__getitem__(value)
        else:
            raise ValueError(
                "Invalid dot notation. Accessor not available. Please start dotted path with one of the accessors: [profile@, session@, payload@, event@] ")

    def __getitem__(self, dot_notation):
        if dot_notation.startswith('profile@'):
            value = dot_notation[len('profile@'):]
            try:
                return self.profile[value]
            except KeyError:
                raise KeyError("Could not find value for `{}` in profile".format(value))
        elif dot_notation.startswith('session@'):
            value = dot_notation[len('session@'):]
            try:
                return self.session[value]
            except KeyError:
                raise KeyError("Could not find value for `{}` in session".format(value))
        elif dot_notation.startswith('payload@'):
            value = dot_notation[len('payload@'):]
            try:
                return self.payload[value]
            except KeyError:
                raise KeyError("Could not find value for `{}` in payload".format(value))
        elif dot_notation.startswith('event@'):
            value = dot_notation[len('event@'):]
            try:
                return self.event[value]
            except KeyError:
                raise KeyError("Could not find value for `{}` in event".format(value))
        else:
            raise ValueError("Invalid dot notation. Accessor nor available")

    @staticmethod
    def get(dot_notation, payload, prefix):
        value = dot_notation[len(prefix + '@'):]
        try:
            return payload[value]
        except KeyError:
            raise KeyError("Could not find value for `{}` in {}".format(value, prefix))

    @staticmethod
    def set(key, value, payload, prefix):
        key = key[len(prefix+'@'):]
        payload[key] = value
