def upload_image(instance, filename):
  import os
  from random import randint
  from django.utils.timezone import now
  filename_base, filename_ext = os.path.splitext(filename)
  print(filename_base, filename_ext)  
  return '%s' % (
      #instance.id,
    #   now().strftime('%Y%m%d')+'_'+str(randint(10000000,99999999))
    now().strftime('%Y%m%d')+"_"+filename
  )