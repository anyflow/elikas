import k8s_operator
import tcn
from config import COLOR_OFF, MODE, TEXT_RED

match MODE:
    case "k8s_operator":
        k8s_operator.run()
    case "tcn":
        tcn.create()
    case _:
        print(f"{TEXT_RED}ERROR : {MODE} mode is not supported.{COLOR_OFF}")
        exit(1)
