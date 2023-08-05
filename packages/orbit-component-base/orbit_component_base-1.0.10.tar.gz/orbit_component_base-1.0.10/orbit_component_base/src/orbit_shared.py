class Global:

    _sio = None
    _api = None
    _conf = None
    _args = None

    @property
    def sio (self):
        return self._sio

    @property
    def api (self):
        return self._api

    @property
    def conf (self):
        return self._conf

    @property
    def args (self):
        return self._args

    @api.setter
    def api (self, value):
        self._api = value

    @sio.setter
    def sio (self, value):
        self._sio = value

    @conf.setter
    def conf (self, value):
        self._conf = value

    @args.setter
    def args (self, value):
        self._args = value

world = Global()
