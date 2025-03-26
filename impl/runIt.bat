REM Run Blender, passing in the all ".py" files that are required
REM (optionally passing along additional arguments)

blender.exe -P blender_conversions.py -P blender_utilities.py -P io_utilities.py -P roundtrip.py -P roundtrip_runner.py -P roundtrip_utilities.py -- %1 %2 %3 %4 %5 %6 %7 %8 %9