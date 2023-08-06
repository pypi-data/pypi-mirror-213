import traceback

try:
    from Vbalog import FunctionLog
    from minusFunction import minusFunction
except:
    try:
        from .Vbalog import FunctionLog
        from .minusFunction import minusFunction
    except:
        traceback.print_exc()
import sys, datetime
if __name__ == "__main__":
    FuncitonId = sys.argv[1]
    token = sys.argv[2]
    useNumber = sys.argv[3]
    details = sys.argv[4]
    functionName = sys.argv[5]
    # FuncitonId = 91
    # useNumber = 10
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwiaXAiOiIxNzIuMTYuNzMuMSIsIm1hYyI6IjAwMmI2N2UyMmQ1OCJ9.nuphngVh-HEXUhQeiADFvvEOKMwASpCFxWb2VtC0AH4'
    startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # details = ''
    # functionName = 'vbarongdatools001'
    minusFunction(functionName,token, useNumber)
    FunctionLog(FuncitonId, token, useNumber, startTime, endTime, details)