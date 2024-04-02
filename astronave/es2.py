class CentralPc:
    _istanza = None

    def __new__(cls):
        if cls._istanza is None:
            cls._istanza = super().__new__(cls)
            cls._istanza.stato = 'in Attesa'
            cls._istanza.motori = 'Spenti'
        return cls._istanza
    
    def status(cls):
        cls.motori= 'Spenti'
        cls.stato= "in Attesa"
        print("CentralPc: ", cls.motori, cls.stato)

    def start(cls):
        cls.motori= 'Accesi'
        cls.stato= "in Movimento"
        print("CentralPc: ", cls.motori, cls.stato)

    def stop(cls):
        cls.motori= 'Spenti'
        cls.stato= "in Attesa"
        print("CentralPc: ", cls.motori, cls.stato)

ist = CentralPc()
ist2 = CentralPc()

ist.status()
ist2.status()

ist.start()
ist2.start()

ist.stop()
ist2.stop()