class GXCmdParameter():
    """
    This class is used to save command line parameters.
    """
    def __init__(self):
        """
        Constructor.
        """
        # Command line parameter tag.
        self.tag = str
        # Command line parameter value.
        self.parameter = str
        # Parameter is missing.
        self.missing = None