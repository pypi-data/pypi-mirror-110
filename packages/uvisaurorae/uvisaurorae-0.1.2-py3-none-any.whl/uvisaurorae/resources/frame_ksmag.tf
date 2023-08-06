Kronocentric Solar Magnetic (KSMAG) frame

   The CASSINI_KSMAG frame implements the CASSINI mission KSMAG reference frame.

   It is defined as a dynamic frame as follows:

      -  +Z axis is along the Saturn north pole (+Z of the IAU_SATURN
         frame)
 
      -  +X axis is in the direction of the geometric position of the
         Sun as seen from Saturn
 
      -  +Y completes the right handed frame
 
      -  the center is at the center of mass of Saturn.

   The keywords below implement the CASSINI_KSMAG frame as a dynamic frame.

   \begindata

      FRAME_CASSINI_KSMAG          = 1900000
      FRAME_1900000_NAME            = 'CASSINI_KSMAG'
      FRAME_1900000_CLASS           = 5
      FRAME_1900000_CLASS_ID        = 1900000
      FRAME_1900000_CENTER          = 699
      FRAME_1900000_RELATIVE        = 'J2000'
      FRAME_1900000_DEF_STYLE       = 'PARAMETERIZED'
      FRAME_1900000_FAMILY          = 'TWO-VECTOR'
      FRAME_1900000_PRI_AXIS        = 'Z'
      FRAME_1900000_PRI_VECTOR_DEF  = 'CONSTANT'
      FRAME_1900000_PRI_FRAME       = 'IAU_SATURN'
      FRAME_1900000_PRI_SPEC        = 'RECTANGULAR'
      FRAME_1900000_PRI_VECTOR      =  ( 0, 0, 1 )
      FRAME_1900000_SEC_AXIS        = 'X'
      FRAME_1900000_SEC_VECTOR_DEF  = 'OBSERVER_TARGET_POSITION'
      FRAME_1900000_SEC_OBSERVER    = 'SATURN'
      FRAME_1900000_SEC_TARGET      = 'SUN'
      FRAME_1900000_SEC_ABCORR      = 'NONE'

   \begintext
   
   \begindata

      FRAME_CASSINI_KRTP           = 1900001
      FRAME_1900001_NAME            = 'CASSINI_KRTP'
      FRAME_1900001_CLASS           = 5
      FRAME_1900001_CLASS_ID        = 1900001
      FRAME_1900001_CENTER          = 'CASSINI'
      FRAME_1900001_RELATIVE        = 'J2000'
      FRAME_1900001_DEF_STYLE       = 'PARAMETERIZED'
      FRAME_1900001_FAMILY          = 'TWO-VECTOR'
      FRAME_1900001_PRI_AXIS        = 'X'
      FRAME_1900001_PRI_VECTOR_DEF  = 'OBSERVER_TARGET_POSITION'
      FRAME_1900001_PRI_OBSERVER    = 'SATURN'
      FRAME_1900001_PRI_TARGET      = 'CASSINI'
      FRAME_1900001_PRI_ABCORR      = 'NONE'
      FRAME_1900001_SEC_AXIS        = 'Y'
      FRAME_1900001_SEC_VECTOR_DEF  = 'CONSTANT'
      FRAME_1900001_SEC_FRAME       = 'IAU_SATURN'
      FRAME_1900001_SEC_SPEC        = 'RECTANGULAR'
      FRAME_1900001_SEC_VECTOR      = ( 0, 0, -1 )

   \begintext