# Paste this script in an empty Python project
# Run once to install
# Warning: it can take a while to download and start. Be patient.
# Watch console output to check progress.
# After reboot DO NOT LET THE SOFTWARE UPDATE YOUR HUB
# Works with the LEGO SPIKE app and the LEGO MINDSTORMS app
#adapted from https://antonsmindstorms.com/


from ubinascii import hexlify, a2b_base64
from uhashlib import sha256
from os import mkdir
import hub, time
encoded = (('mindsensors.mpy', ('TQUCHyCLABhiAAcqLi4vbGliL21pbmRzZW5zb3JzLnB5gBgoKDAwMChwICQkJGQgYIvii6uLGoscjiqOUY4zjkuOlIsUjheOJo5TjiIAgFEbCnV0aW1lFgh0aW1lgFEbDnVzdHJ1Y3QWAYAQClRpbWVyKgEbDm1hY2hpbmUcAxYBWYAQAEgqARsAcxwASBYASFmAEApzbGVlcCoBGwkcAxYBWYBRGwZodWIWAYAQCHBvcnQqARsDHAMWAVmAFgRJToEWBk9VVIAWBkxPV4EWBEhJVDIAEBBTUElLRWkyYzQCFgFUMgEQDlRGVFBBQ0s0AhYBVDICEBBTVU1PRVlFUw==\n', 'NAIWAVQyAxASQUxUSU1FVEVSNAIWAVQyBBAIRElTVBEJNAMWA1QyBRAMRVYzRlBTEQU0AxYDVDIGEBBJUlRIRVJNTxEFNAMWA1QyBxAORVYzUkZJRBEFNAMWA1QyCBAMTlhUQ0FNEQU0AxYDVDIJEAhCTE9CNAIWAVQyChAMVE1QMjc1EQc0AxYDVDILEBJFVjNMSUdIVFMRBTQDFgNUMgwQDFBGTUFURREFNAMWA1QyDRAORVYzRkxPVxEFNAMWA1QyDhAUR09PR0xZRVlFUxEFNAMWA1FjAA+FPAhYAzeMLkRlZWVlixWFEoUThROFIYUQhQqFDYUHhQiFB4UHhQ==\n', 'B4UJZUBlQAARABcWABYQAxYAGn8WDmludF9jbGsyABYMX190aWNrMgEWGF9fR1BJT19zZXR1cDICFhpfX0dQSU9fb3V0cHV0MgMWGF9fR1BJT19pbnB1dCKAZCoBUzMEFgARMgUWDl9fU3RhcnQyBhYSX19SZWFkQWNrMgcWFF9fUmVhZE5hY2syCBYWX19Xcml0ZUJ5dGUyCRYMX19TdG9wMgoWEHJlYWRCeXRlMgsWEnJlYWRBcnJheTIMFhJ3cml0ZUJ5dGUyDRYUd3JpdGVBcnJheTIOFhRyZWFkU3RyaW5nMg8WFnJlYWRJbnRlZ2VyMhAWInJlYWRJbnRlZw==\n', 'ZXJTaWduZWQyERYQcmVhZExvbmcyEhYkR2V0RmlybXdhcmVWZXJzaW9uMhMWGkdldFZlbmRvck5hbWUyFBYWR2V0RGV2aWNlSWRRYwAVaCoOJy2AMQASCHRpbWUUCnNsZWVwsbATL/Q2AVlRYwAAAIkGYW56TCsOMQuANACxFBJkaXJlY3Rpb26yNgFZUWMAAACJCGxpbmUKc3RhdGVMKw43CYA3ALEUAKKyNgFZUWMAAACJBwCiQBoONwWAOgCxFACiNgBjAAAAiQWGQLAFMgARA4A9MCsoKC0tLS0lJiYoKSgpKCgoALEUCG1vZGUSBmh1YhMIcG9ydBMSTU9ERQ==\n', 'X0dQSU82AVkSHRQdIwQ2AVmxEwRwNbAYBlNDTLETBHA2sBgGU0RBsBMFFB8SBk9VVDYBWbATBxQFEgU2AVmwEwcUAKISBEhJNgFZsBMJFACiEgM2AVmysBgOYWRkcmVzc7OK2UQGgCMFsBgrsyKAZNlECYAjBrAYAUIxgLMigxDZRAmAIwewGAFCIICzIodo2UQIgIGwGAFCEICzIpkA2UQIgIGwGAFCAIBRYwQAAIkZFmkyY19hZGRyZXNzDmJpdHJhdGVmAzAuMWYHMi41ZS0wNWYHMi41ZS0wNmYINi4yNWUtMDeCVCEWDl9fU3RhcnQlgFkuLk5OALAUL7ATEw==\n', 'Ehc2AlmwFC2wEwUSFzYCWbAUBbATGRIFNgJZsBQFsBMHEgZMT1c2AlmwFAWwEwkSBTYCWVFjAAAAiYUgOSQSX19SZWFkQWNrEYBkLiImTjF3Li5OLk4AsBQRsBMNEgRJTjYCWYDBgEIxgFfCsBQPsBMPEhE2AlmxsBQzsBMLNgGH8LLx4MGwFAmwEwkSEzYCWYHlV4jXQ8l/WbAUD7ATCRIVNgJZsBQLsBMFEgk2AlmwFAWwEwsSDzYCWbAUBbATBRIHNgJZsBQFsBMJEgU2AlmxYwAAAImFIDkkFF9fUmVhZE5hY2sVgHcuIiZOMXcuLk4uTgCwFBGwEwkSFTYCWQ==\n', 'gMGAQjGAV8KwFA2wEw8SETYCWbGwFBWwEws2AYfwsvHgwbAUCbATCRITNgJZgeVXiNdDyX9ZsBQPsBMJEhU2AlmwFAuwEwUSDzYCWbAUBbATDRIFNgJZsBQFsBMFEg02AlmwFAWwEwkSBTYCWbFjAAAAiYZ4OiwWX19Xcml0ZUJ5dGUVgIooQi5GLi5OLnEuTncujggAsSKBf9hEAoB/Y7AUEbATCRIRNgJZgEJ3gFfCsbLwIoEA7yKBANlEO4CwFA2wEwUSETYCWbAUBbATERIFNgJZsBQFsBMFEhE2AlmwFAWwEwkSBTYCWUIqgLAUBbATBRIFNgJZsBQFsBMHEg==\n', 'CTYCWbAUBbATBRIHNgJZgeVXiNdDg39ZsBQNsBMLEhU2AlmwFAuwEwsSDTYCWbAUBbATBRINNgJZUWMAAACJCGJ5dGWCGCEUDF9fU3RvcBWAsU4uTgCwFBOwExMSFTYCWbAUEbATBRIPNgJZsBQFsBMREhM2AlmwFAWwEwkSBTYCWVFjAAAAiYI4MhwQcmVhZEJ5dGURgLsnKygnLScnALAUITYAWbAUG7ATKzYBWbAUA7E2AVmwFAU2AFmwFAOwEwWB7TYBWbAUITYAwrAUGzYAWbJjAAAAiQZyZWeDaFMiEnJlYWRBcnJheQ+AxSMnKygnLR8hLScAKwDDsBQPNg==\n', 'AFmwFA+wEw82AVmwFAOxNgFZsBQFNgBZsBQDsBMFge02AVmygfOAQhGAV8SzFAA8sBQnNgA2AVmB5Vha10Ppf1lZsxQAPLAUETYANgFZsBQRNgBZs2MAAACJEQBrgWArFhJ3cml0ZUJ5dGURgNInKygoALAUETYAWbAUEbATETYBWbAUA7E2AVmwFAGyNgFZsBQNNgBZUWMAAACJDQCigkRLGBR3cml0ZUFycmF5DYDZJysoHyEAsBQNNgBZsBQLsBMNNgFZsBQDsTYBWRIAa7I0AYBCDoBXw7AUAbKzVTYBWYHlWFrXQ+x/WVmwFA02AFlRYwAAAIkNBmFycoF4cw==\n', 'FhRyZWFkU3RyaW5nD4DhJCcfJQAQAAHDsoBCHoBXxBAAARQAaLMSAESwFBuxtPI2ATQBKwI2AcOB5Vha10Pcf1lZs2MAAACJCQxsZW5ndGiBGEIUFnJlYWRJbnRlZ2VyCYDoKComALAUCbE2AcKwFAGxgfI2AcOys4jw8sS0YwAAAIkJUCoQInJlYWRJbnRlZ2VyU2lnbmVkB4DvSACwFAmxNgHCsmMAAACJB4IQUhgQcmVhZExvbmcHgPYoKioqLgCwFAuxNgHCsBQBsYHyNgHDsBQBsYLyNgHEsBQBsYPyNgHFsrOI8PK0kPDytZjw8sa2YwAAAIkHVCkQJEdldA==\n', 'RmlybXdhcmVWZXJzaW9uB4D/KQCwFBGAiDYCwbFjAAAAiVQpEBpHZXRWZW5kb3JOYW1lBZAEKQCwFAWIiDYCwbFjAAAAiVQpEBZHZXREZXZpY2VJZAWQCSkAsBQFkIg2AsGxYwAAAImFdBBgDlRGVFBBQ0sFnA9nIIUJZSCFCIUQZSBlZUBlYGVgZUBlhQhlYI0HhQeFCWUgZYUNhQ2FEQARABcWABYQAxYAGoCAKwIWFFRvdWNoUG9pbnQyABYAETIBFhRyZ2JfaGV4NTY1MgIWAHsyAxYad3JpdGVfY29tbWFuZDIEFhpjbGVhcl9kaXNwbGF5MgUWEmJhY2tsaQ==\n', 'Z2h0MgYWEmdldF90b3VjaDIHFhBydW5fZGVtbzIIFhxpbnZlcnRfZGlzcGxheTIJFhhwcmludF9zdHJpbmcyChYYcHJpbnRfbnVtYmVyMgsWFnByaW50X2Zsb2F0MgwWGnNldF9jdXJzZXJfeHmAgIArAyoBUzMNFhJzZXRfY29sb3IyDhYac2V0X2ZvbnRfc2l6ZTIPFhhzZXRfcm90YXRpb24yEBYSZHJhd19saW5lMhEWFGRyYXdfcGl4ZWwyEhYWZHJhd19iaXRtYXAyExYWZHJhd19jaXJjbGUyFBYcZHJhd19yZWN0YW5nbGUyFRYaZHJhd190cmlhbmdsZQ==\n', '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\n', 'aW5jaGVzMgQWFmdldF92b2x0YWdlUWMABYEouwESABETkP8lJQCysBgYZGlzdF9hZGRyZXNzsbAYKRIQU1BJS0VpMmMUABGwsBMDsBMFNgNZUWMAAACJAwN4Mg4PCaAHALAUEndyaXRlQnl0ZbATGRIAXhIGY21kNAE2AllRYwAAAIkJUBkOFQugDACwFBZyZWFkSW50ZWdlcrATHTYBYwAAAIlYGRAZB6AQJwCwFAk2AMGxIwH3YwEAAIlmBDI0LjVQGQ4ZBaAVALAUC7ATHTYBYwAAAImFIAhIDEVWM0ZQUwesHEZGRkZGRkYmJmZAiwllQGVAZUBlIGUgZSBlIA==\n', 'ZUAAEQAXFgAWEAMWABoigGIWHEVWM2Zwc19BRERSRVNTIoBBFhcigEIWGkVWM2Zwc01hdGNoZWQigEMWGEVWM2Zwc1N0YXR1cyKARBYeRVYzZnBzUHJvZmlsZUlkIoBFFh5FVjNmcHNQcm9maWxlQ3QigEYWIEVWM2Zwc1Byb2ZpbGVDYXAigEQWGkVWM2Zwc19kZWxldGUigEUWGkVWM2Zwc19lbnJvbGwigFIWGkVWM2Zwc19yZW1vdmUREyoBUzMAFgARMgEWJTICFiRnZXRfRVYzZnBzX01hdGNoZWQyAxYiZ2V0X0VWM2Zwc19TdGF0dXMyBBYoZ2V0X0VWMw==\n', 'ZnBzX1Byb2ZpbGVJZDIFFihnZXRfRVYzZnBzX1Byb2ZpbGVDdDIGFipnZXRfRVYzZnBzX1Byb2ZpbGVDYXAyBxYiZ2V0X0VWM2Zwc19EZWxldGUyCBYiZ2V0X0VWM2Zwc19SZW1vdmUyCRYiZ2V0X0VWM2Zwc19FbnJvbGxRYwAKgUi7ARQAESmgMyUlJwCysBgcRVYzZnBzX2FkZHJlc3OxsBg/EgB7sTQBWRIQU1BJS0VpMmMUABGwsBMDsBMFNgNZUWMAAACJAwNcKg4ZCaA8ALAUP7ATL7E2AllRYwAAAIkHUBkOHQmgQACwFBByZWFkQnl0ZbATMTYBYwAAAA==\n', 'iVAZDiEHoEUAsBQHsBMxNgFjAAAAiVAZDiMHoEoAsBQHsBMxNgFjAAAAiVAZDiUHoE4AsBQHsBMxNgFjAAAAiVAZDicHoFIAsBQHsBMxNgFjAAAAiVAZDikHoFYAsBQbsBMxNgFjAAAAiYEEKhArB6BaLACwFCOwExexNgJZsBQLsBMvNgFjAAAAiRJQcm9maWxlSWSCUCkcLw2gXysnIycsMigAsBQJsBMzNgFZsBQlNgDBQh+AsBQBNgDBEgB7IwGxEAwgdGltZXM0A1kSCHRpbWUUEHNsZWVwX21zIoBkNgFZsYHYQ9t/EgB7IwI0AVmAYwIAAIlzInRvdWNoIA==\n', 'ZGVzaXJlZCBmaW5kZ2VyIGFnYWluIG9uIHBhZHMQIGRvbmUgcHJvZ3JhbWluZ4M4CDAQSVJUSEVSTU8PrG1ERkZGRmYgiwhlQGVAZUBlQAARABcWABYQAxYAGqoWIElSVEhFUk1PX0FERFJFU1MigEEWNSKAQhYQQU1CSUVOVEMigEQWDlRBUkdFVEMigEYWEEFNQklFTlRGIoBIFg5UQVJHRVRGEQsqAVMzABYAETIBFhsyAhYYZ2V0X0FtYmllbnRDMgMWGGdldF9BbWJpZW50RjIEFhZnZXRfVGFyZ2V0QzIFFhZnZXRfVGFyZ2V0RlFjAAaBKLsBEgARGaB9JQ==\n', 'JQCysBggaXJ0aGVybW9fYWRkcmVzc7GwGAhwb3J0EhBTUElLRWkyYxQAEbCwEwOwEwU2A1lRYwAAAIkDA3gyDhEJoIUAsBQzsBMfEgBeEgZjbWQ0ATYCWVFjAAAAiQlgGQ4XC6CKALAUFnJlYWRJbnRlZ2VysBMjNgEigGT3YwAAAIlgGQ4bB6CPALAUB7ATITYBIoBk92MAAACJYBkOHQeglACwFAewEyM2ASKAZPdjAAAAiWAZDh8HoJkAsBQHsBMjNgEigGT3YwAAAImCKAgmDkVWM1JGSUQHrJ5pYGVAhQiFCYUUhRAAEQAXFgAWEAMWABqiKgFTMwAWABEyAQ==\n', 'FhBjbGVhclVJRDICFhxSZWFkQmxvY2tBcnJheTIDFh5SZWFkQmxvY2tTdHJpbmcyBBYgV3JpdGVCbG9ja1N0cmluZzIFFh5Xcml0ZUJsb2NrQXJyYXkyBhYOcmVhZFVJRFFjAAeBKLsBEgARD6CfJSUAsrAYHmV2M3JmaWRfYWRkcmVzc7GwGC8SMRQAEbCwEwOwEwU2A1lRYwAAAIkDFmkyY19hZGRyZXNzYCEOFQugpQCwFDEigEEigEM2AllRYwAAAImBeDIUFwWgqjAtKgCwFAUigE8SAJexNAE2AlmwFAEigEEQAlI2AlkSPRQKc2xlZXCCNgFZsBQScmVhZA==\n', 'QXJyYXkigFCQNgJjAAAAiQ5CbG9ja0lEgXgyFCEPoLIwLSoAsBQPIoBPEgCXsTQBNgJZsBQBIoBBEA82AlkSDxQPgjYBWbAUFHJlYWRTdHJpbmcigFCQNgJjAAAAiQ+DUGsiIw+gu2IwJiYyJyMuSk0AgMOwFA8igE8SAJexNAE2AlmyX0sgAMSzkNdEFoCwFAEigFCz8hIAl7Q0ATYCWbOB8sNC3X9CEoCwFAEigFCz8iMDNgJZs4Hyw7OQ10Pof7AUASKAQRACVzYCWbNjAQAAiQkUZGF0YVN0cmluZ2ICeDCDUGsiJwugzyIwJiYyJyMuSk0AgMOwFAsigE8SAA==\n', 'l7E0ATYCWbJfSyAAxLOQ10QWgLAUASKAULPyEgCXtDQBNgJZs4Hyw0Ldf0ISgLAUASKAULPyIwM2AlmzgfLDs5DXQ+h/sBQBIoBBEAs2AlmzYwEAAIkLCGRhdGFiAngwgVw5FikLoN8qKioqALAUEHJlYWRCeXRlIoBENgHBsBQBIoBFNgHCsBQBIoBGNgHDsbKI8PKzkPDyxLRjAAAAiYcICGwMTlhUQ0FNBazrREZGRkZGRmZAiwdlIGVAZUBlQGVAZUBlQGVAZSBlIGVAZSBlQGVAZUBlQGVAhRUAEQAXFgAWEAMWABqCFhxOWFRDQU1fQUREUkVTUyKAQRYOQw==\n', 'T01NQU5EIoBCFhpOdW1iZXJPYmplY3RzIoBDFgpDb2xvciKARBYKWF9Ub3AigEUWCllfVG9wIoBGFhBYX0JvdHRvbSKARxYQWV9Cb3R0b20RDyoBUzMAFgARMgEWDmNvbW1hbmQyAhYQc29ydFNpemUyAxYWdHJhY2tPYmplY3QyBBYmd3JpdGVJbWFnZVJlZ2lzdGVyczIFFhhzdG9wVHJhY2tpbmcyBhYac3RhcnRUcmFja2luZzIHFhZnZXRDb2xvck1hcDIIFhxpbGx1bWluYXRpb25PbjIJFiRyZWFkSW1hZ2VSZWdpc3RlcnMyChYSdHJhY2tMaW5lMgsWCA==\n', 'cGluZzIMFgpyZXNldDINFhhzZW5kQ29sb3JNYXAyDhYeaWxsdW1pbmF0aW9uT2ZmMg8WEnNvcnRDb2xvcjIQFhBmaXJtd2FyZTIRFhBzb3J0Tm9uZTISFiBnZXROdW1iZXJPYmplY3RzgSoBUzMTFhBnZXRCbG9ic1FjABSBKLsBEgAROaD/JSUAsbAYCHBvcnSysBgcbnh0Y2FtX2FkZHJlc3MSEFNQSUtFaTJjFAARsLATBbATBTYDWVFjAAAAiQMDXCoOLQmwBgCwFBJ3cml0ZUJ5dGWwEz+xNgJZUWMAAACJB1QZDjEJsAoAsBQFIoBBNgFZUWMAAACJVBkOMQ==\n', 'BbAPALAUBSKAQjYBWVFjAAAAiVQZDjEFsBQAsBQFIoBDNgFZUWMAAACJVBkOMQWwGQCwFAUigEQ2AVlRYwAAAIlUGQ4xBbAeALAUBSKARTYBWVFjAAAAiVQZDjEFsCMAsBQFIoBHNgFZUWMAAACJVBkOMQWwKACwFAUigEk2AVlRYwAAAIlUGQ4xBbAtALAUBSKASDYBWVFjAAAAiVQZDjEFsDEAsBQFIoBMNgFZUWMAAACJVBkOMQWwNQCwFAUigFA2AVlRYwAAAIlUGQ4xBbA6ALAUBSKAUjYBWVFjAAAAiVQZDjEFsD4AsBQFIoBTNgFZUWMAAACJVBkOMQWwQw==\n', 'ALAUBSKAVDYBWVFjAAAAiVQZDjEFsEgAsBQFIoBVNgFZUWMAAACJVBkOMQWwTQCwFAUigFY2AVlRYwAAAIlUGQ4xBbBSALAUBSKAWDYBWVFjAAAAiVAZDjEFsFcAsBQQcmVhZEJ5dGWwExpOdW1iZXJPYmplY3RzNgFjAAAAiYUQ+gEkNQewbCgnJCYoYjMzMzMzAICAgICAKwXCsBQJNgDDsYHzxLGz2EQKgBIAeyMCNAFZgGOwFAmwEwpDb2xvcrSF9PI2AVeygFbFsBQDsBMKWF9Ub3C0hfTyNgFXsoFWxrAUA7ATCllfVG9wtIX08jYBV7KCVsewFAOwExBYXw==\n', 'Qm90dG9ttIX08jYBV7KDVsiwFAOwExBZX0JvdHRvbbSF9PI2AVeyhFbJEghCTE9Ctba3uLk0BWNRYwEAAIkOYmxvYk51bXMwYmxvYk51bSBpcyBncmVhdGVyIHRoYW4gYW1vdW50IG9mIGJsb2JzIHRyYWNrZWQucAAOAxO8hgARABcWABYQAxYAGjIAFgARUWMAAYEkugQWABEDsIclJSUlALGwGApjb2xvcrKwGAhsZWZ0s7AYBnRvcLSwGApyaWdodLWwGAxib3R0b21RYwAAAIkJCQkJCYFoCBgMVE1QMjc1DbyTRkRkiwgAEQAXFgAWEAMWABoigRgWHFRNUA==\n', 'Mjc1X0FERFJFU1OBFg5DT01NQU5EgBYUVE1QRVJBVFVSRREFKgFTMwAWABEyARYecmVhZFRlbXBlcmF0dXJlUWMAAoEouwESABELsJ0lJQCysBgcVE1QMjc1X2FkZHJlc3OxsBgIcG9ydBIQU1BJS0VpMmMUABGwsBMDsBMFNgNZUWMAAACJAwNQGQ4JCbCjALAUI7ATDzYBYwAAAImBWAgaEkVWM0xJR0hUUwe8qmQgiwmFCwARABcWABYQAxYAGqwWIkVWM0xpZ2h0c19BRERSRVNTEQEqAVMzABYAETIBFhBTZXRDb2xvcjICFhBTZXRQaXhlbFFjAAOBKLsBEg==\n', 'ABEJsLElJQCysBgiRVYzTGlnaHRzX2FkZHJlc3OxsBgVEhcUABGwsBMDsBMFNgNZUWMAAACJAwOCODIWCwmwuS0tLS0AsBQSd3JpdGVCeXRlIoBBIoBTNgJZsBQBIoBCsYBVNgJZsBQBIoBDsYFVNgJZsBQBIoBEsYJVNgJZsBQBIoBGgTYCWVFjAAAAiQZSR0KCaDsYDwewxC0tLS0rALAUByKAQSKASTYCWbAUASKAQrKAVTYCWbAUASKAQ7KBVTYCWbAUASKARLKCVTYCWbAUASKARbE2AlmwFAEigEaBNgJZUWMAAACJAFwHghgIIgxQRk1BVEUHvNBmQIsshQ==\n', 'CYUKhQcAEQAXFgAWEAMWABoigEgWHFBGTWF0ZV9BRERSRVNTEQEqAVMzABYAETIBFiJjb250cm9sQm90aE1vdG9yczICFhpjb250cm9sTW90b3JBMgMWGmNvbnRyb2xNb3RvckIyBBYOY29tbWFuZFFjAAWESLsBMAARDbDYJSVSRUVFRUVFRWVHR0dHR0cAsrAYHFBGTWF0ZV9hZGRyZXNzsbAYGxIdFAARsLATA7ATBTYDWYCwGBhQRk1BVEVfRkxPQVSBsBgcUEZNQVRFX0ZPUldBUkSCsBgcUEZNQVRFX1JFVkVSU0WDsBgYUEZNQVRFX0JSQUtFgbAYHlBGTQ==\n', 'QVRFX0NIQU5ORUwxgrAYHlBGTUFURV9DSEFOTkVMMoOwGB5QRk1BVEVfQ0hBTk5FTDOEsBgeUEZNQVRFX0NIQU5ORUw0IoBBsBgcUEZNQVRFX0NPTU1BTkQigEKwGBxQRk1BVEVfQ0hBTk5FTCKAQ7AYGlBGTUFURV9NT1RPUlMigESwGBpQRk1BVEVfT1BFUl9BIoBFsBgcUEZNQVRFX1NQRUVEX0EigEawGBpQRk1BVEVfT1BFUl9CIoBHsBgcUEZNQVRFX1NQRUVEX0JRYwAAAIkhDmFkZHJlc3OBNOIEEi8pwAIpLACxgLKztLUrBsawFBR3cml0ZUFycmF5sA==\n', 'ExW2NgJZsBQtIoBHNgFZUWMAAACJDmNoYW5uZWwUb3BlcmF0aW9uQQxzcGVlZEEUb3BlcmF0aW9uQgxzcGVlZEKBLMAEEjsTwAsnLACxgbKzKwTEsBQTsBMTtDYCWbAUEyKARzYBWVFjAAAAiRMTE4EswAQSOw/AFScsALGBsrMrBMSwFA+wEw+0NgJZsBQPIoBHNgFZUWMAAACJDxUVXCoOBw3AHACwFBJ3cml0ZUJ5dGWwEymxNgJZUWMAAACJBmNtZIJoCCYORVYzRkxPVwnMIkUmJiZmQIsIZSBlQAARABcWABYQAxYAGiI4Fh5FVjNGTE9XX0FERFJFU1MigA==\n', 'QRYOQ09NTUFORCKARhYIRkxPVyKAQhYGVk9MIoBDFgpDTEVBUhEJKgFTMwAWABEyARYQZ2V0X2Zsb3cyAhYARjIDFhRnZXRfdm9sdW1lUWMABIEouwESABERwC4lJQCysBgeRVYzRmxvd19hZGRyZXNzsbAYMxIQU1BJS0VpMmMUABGwsBMDsBMFNgNZUWMAAACJAzVYGQ4NC8A1ALAUFnJlYWRJbnRlZ2VysBMXNgGB92MAAACJgRAhEABGBcA5LQCwFCEigEEigEM2AlkSCHRpbWUUCnNsZWVwIwE2AVlRYwEAAIlmAzAuNWAZDhcJwD4AsBQQcmVhZExvbmewEw==\n', 'HzYBIodo92MAAACJgkgIKhRHT09HTFlFWUVTB8xFZECLD4ULZUBlIGUgZUAAEQAXFgAWEAMWABqsFiRHb29nbHlFeWVzX0FERFJFU1MRASoBUzMAFgARMgEWEmFsbF9waXhlbDICFgpwaXhlbDIDFgBGMgQWCmJsYW5rMgUWCHNob3cyBhY1UWMAB4IguwEYABEPwE0lJVJHRwCysBgkR29vZ2x5RXllc19hZGRyZXNzsbAYJxIrFAARsLATA7ATBTYDWSKAQrAYHEdvb2dseUV5ZXNfUGl4IoBBsBgkR29vZ2x5RXllc19DT01NQU5EsBMHFAZwd20igGQ2AVlRYw==\n', 'AAAAiQMvglg6GBkRwFomKiozKwCAQiKAV8KxFAA8sYBVNgFZsRQAPLGBVTYBWbEUADyxglU2AVmB5VeP10PYf1mwFBR3cml0ZUFycmF5IoBCsTYCWbAUK7ATDyKAVTYCWVFjAAAAiQZSR0KBJDsQHwvAZS8AsBQLIoBCg7H08rI2AlmwFAuwEwsigFU2AllRYwAAAIkGcGl4DWQhDgBGC8BqALAUCbATCSKAQzYCWVFjAAAAiWQhDiEHwG4AsBQHsBMHIoBCNgJZUWMAAACJZCEOIQfAcgCwFAewEwcigFU2AllRYwAAAIlcKg4hB8B3ALAUB7ATB7E2AllRYwAAAA==\n', 'iQZjbWQ=\n'), '446fba92312f3bfc57dbd947a18b5cb8d53f34aecf25c222c803584134fc0c28'), ('__init__.mpy', ('TQUCHyBMCAoAByQuLi9saWIvX19pbml0X18ucHkAgRAABSoBGxZtaW5kc2Vuc29yc2lRYwAA\n',), '1614e0dd5f433a7d4a888570ea33c8d6ce1eab01b6b93d4ae79c8f894c3d03a5'))


def calc_hash(b):
    return hexlify(sha256(b).digest()).decode()


error = False
try:
    mkdir('/projects/lib')
except:
    pass

for file, code, hash_gen in encoded:
    print('Writing file ', file)
    target_loc = '/projects/lib/' + file

    print('writing ' + file + ' to folder /projects/lib')
    with open(target_loc, 'wb') as f:
        for chunk in code:
            f.write(a2b_base64(chunk))
    del code

    try:
        print('Finished writing ' + file + ', Checking hash.')
        result = open(target_loc, 'rb').read()
        hash_check = calc_hash(result)

        print('Hash generated: ', hash_gen)

        if hash_check != hash_gen:
            print('Failed hash of .mpy on the robot: ' + hash_check)
            error = True
    except Exception as e:
        print(e)

if not error:
    print('Library written successfully. Resetting  hub, please wait.')
    time.sleep(5)
    hub.reset()
else:
    print('Failure in writing library!')
