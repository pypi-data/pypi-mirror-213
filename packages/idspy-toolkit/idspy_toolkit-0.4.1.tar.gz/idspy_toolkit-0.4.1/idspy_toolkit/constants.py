
IMAS_DEFAULT_INT = 999999999
IMAS_DEFAULT_FLOAT = 9e40
IMAS_DEFAULT_CPLX = complex(9e40, -9e40)
IMAS_DEFAULT_STR = ""

IMAS_CONVERT_TABLE = (("INT_0D", "{IMAS_NAMESPACE}int", IMAS_DEFAULT_INT),
                      ("INT_1D", "{IMAS_NAMESPACE}ndarray[(int,), int]", None),
                      ("INT_2D", "{IMAS_NAMESPACE}ndarray[(int, int), int]", None),
                      ("INT_3D", "{IMAS_NAMESPACE}ndarray[(int, int, int), int]", None),
                      ("FLT_0D", "{IMAS_NAMESPACE}float", IMAS_DEFAULT_FLOAT),
                      ("FLT_1D", "{IMAS_NAMESPACE}ndarray[(int,), float]", None),
                      ("FLT_2D", "{IMAS_NAMESPACE}ndarray[(int,int), float]", None),
                      ("FLT_3D", "{IMAS_NAMESPACE}ndarray[(int,int, int), float]", None),
                      ("FLT_4D", "{IMAS_NAMESPACE}ndarray[(int,int,int,int), float]", None),
                      ("FLT_5D", "{IMAS_NAMESPACE}ndarray[(int,int,int,int,int), float]", None),
                      ("FLT_6D", "{IMAS_NAMESPACE}ndarray[(int,int,int,int,int,int), float]", None),
                      ("FLT_7D", "{IMAS_NAMESPACE}ndarray[(int,int,int,int,int,int,int), float]", None),
                      ("STR_0D", "{IMAS_NAMESPACE}str", IMAS_DEFAULT_STR),
                      ("STR_1D", "{IMAS_NAMESPACE}list[str]", None),
                      ("STR_2D", "{IMAS_NAMESPACE}list[list[str]]", None),
                      ("CPX_0D", "{IMAS_NAMESPACE}complex", IMAS_DEFAULT_CPLX),
                      ("CPX_1D", "{IMAS_NAMESPACE}ndarray[(int,), complex]", None),
                      ("CPX_2D", "{IMAS_NAMESPACE}ndarray[(int, int), complex]", None),
                      ("CPX_3D", "{IMAS_NAMESPACE}ndarray[(int, int, int ), complex]", None),
                      ("CPX_4D", "{IMAS_NAMESPACE}ndarray[(int, int, int, int), complex]", None),
                      ("CPX_5D", "{IMAS_NAMESPACE}ndarray[(int, int, int, int, int), complex]", None),
                      ("CPX_6D", "{IMAS_NAMESPACE}ndarray[(int, int, int, int, int, int), complex]", None)
                      )

IMAS_CONVERT_DICT = {x[0]: (x[1], x[2]) for x in IMAS_CONVERT_TABLE}


