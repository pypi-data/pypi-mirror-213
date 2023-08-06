
import logging  # imported  the library   (default library )
import time
from Mouritech_LoggingPerformance.LogPerformance import  PerformanceLogger
logger = PerformanceLogger(__name__)
@logger.log_performance
def my_function():
  num=int(input('Enter Num value:'))
  result=0
  power=1
  for x in str(num):
        y=int(x)

        '''logic to check the dis'''
        result= result + y**power
        power=power+1
  if num==result:
        print(f'The provide {num} is Disarum')
  else:
        print(f'The Provided {num} is Not a Disarum Number')
time.sleep(1) 
my_function()
























