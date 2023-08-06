import traceback

try:
    from vbaLogin import LoginFun
except:
    try:
        from .vbaLogin import LoginFun
    except:
        traceback.print_exc()
import sys
if __name__ == "__main__":
    # FunName = 'vbarongdatools001'
    FunName = sys.argv[1]
    LoginFun(FunName)