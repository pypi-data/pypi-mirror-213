import traceback
try:
    from getNumber import GetFunNum
except:
    traceback.print_exc()
import  sys
if __name__ == "__main__":
    functionName = sys.argv[1]
    token = sys.argv[2]
    # functionName = "vbarongdatools001"
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwiaXAiOiIxNzIuMTYuNzMuMSIsIm1hYyI6IjAwMmI2N2UyMmQ1OCJ9.nuphngVh-HEXUhQeiADFvvEOKMwASpCFxWb2VtC0AH4'

    GetFunNum(functionName, token)